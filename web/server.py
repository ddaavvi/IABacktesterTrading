"""
Delfos — API Server v0.3
=========================

Servidor web ligero + API REST.
Sirve el Dashboard interactivo y expone endpoints para:
- /api/recalculate — recálculo completo de backtesting
- /api/live-prices — cotizaciones en tiempo real
- /api/live-analysis — indicadores técnicos en vivo
- /api/alert-check — verificación de alertas de precio
"""

import http.server
import socketserver
import urllib.parse
import json
import traceback
import sys
import os
import time
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
import backtester
import threading

PORT = 8000
IS_LOADING = True

# Cache for live prices to avoid hitting Yahoo too often
_live_price_cache = {"prices": {}, "timestamp": 0}

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Status endpoint
        if parsed_path.path == '/api/status':
            global IS_LOADING
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"loading": IS_LOADING}).encode('utf-8'))
            return

        # Recalculate endpoint
        if parsed_path.path == '/api/recalculate':
            qs = urllib.parse.parse_qs(parsed_path.query)
            comm_str = qs.get('commission', ['0.0'])[0]
            try:
                comm_pct = float(comm_str)
                comm_decimal = comm_pct / 100.0
            except ValueError:
                comm_decimal = 0.004
                
            start_date = qs.get('start_date', [None])[0]
            end_date = qs.get('end_date', [None])[0]
            
            try:
                print(f"RECALC: commission={comm_pct}%, start={start_date}, end={end_date}")
                import importlib
                importlib.reload(backtester)
                result_dict = backtester.run_all(commission=comm_decimal, start_date=start_date, end_date=end_date)
                
                with open(os.path.join(PROJECT_ROOT, "data", "results.json"), "w", encoding="utf-8") as f:
                    json.dump(result_dict, f, indent=2, ensure_ascii=False)
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result_dict).encode('utf-8'))
            except Exception as e:
                print("Error during recalculation:")
                traceback.print_exc()
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        # Live prices endpoint (v0.3: 27 tickers, cached 30s)
        if parsed_path.path == '/api/live-prices':
            global _live_price_cache
            now = time.time()
            
            # Serve from cache if fresh (< 30s old)
            if now - _live_price_cache["timestamp"] < 30 and _live_price_cache["prices"]:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(_live_price_cache["prices"]).encode('utf-8'))
                return
                
            try:
                import yfinance as yf
                import pandas as pd
                
                # Get tickers from backtester module
                tickers = backtester.TICKERS
                
                try:
                    df = yf.download(tickers, period="2d", interval="1d", progress=False, group_by='ticker')
                except Exception:
                    # Fallback: download individually
                    df = yf.download(tickers, period="2d", progress=False)
                
                prices = {}
                
                if isinstance(df.columns, pd.MultiIndex) and df.columns.nlevels >= 2:
                    # MultiIndex with tickers
                    try:
                        # New yfinance: columns multiindex (Ticker, PriceType)
                        for tk in tickers:
                            try:
                                prices[tk] = float(df[(tk, 'Close')].iloc[-1])
                            except (KeyError, IndexError):
                                prices[tk] = 0.0
                    except Exception:
                        # Alternative: columns (PriceType, Ticker)
                        for tk in tickers:
                            try:
                                prices[tk] = float(df['Close'][tk].iloc[-1])
                            except (KeyError, IndexError, TypeError):
                                prices[tk] = 0.0
                else:
                    for tk in tickers:
                        try:
                            prices[tk] = float(df['Close'].iloc[-1])
                        except (KeyError, IndexError, TypeError):
                            prices[tk] = 0.0
                
                # Cache
                _live_price_cache = {"prices": prices, "timestamp": now}
                        
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(prices).encode('utf-8'))
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Return cache or empty
                self.wfile.write(json.dumps(_live_price_cache["prices"] or {"error": str(e)}).encode('utf-8'))
            return

        # Live technical analysis (v0.3)
        if parsed_path.path == '/api/live-analysis':
            qs = urllib.parse.parse_qs(parsed_path.query)
            symbol = qs.get('symbol', ['SPY'])[0]
            try:
                import yfinance as yf
                import numpy as np
                
                # Fetch recent data for analysis
                df = yf.download(symbol, period="6mo", progress=False)
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [col[0] for col in df.columns]
                
                close = df['Close']
                high = df['High']
                low = df['Low']
                volume = df['Volume']
                
                # Compute indicators
                rsi_period = 14
                delta = close.diff()
                gain = delta.where(delta > 0, 0).rolling(rsi_period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(rsi_period).mean()
                rs = gain / loss.replace(0, 1e-10)
                rsi = float((100 - (100 / (1 + rs))).iloc[-1]) if not loss.empty else 50.0
                
                sma_20 = float(close.rolling(20).mean().iloc[-1])
                sma_50 = float(close.rolling(50).mean().iloc[-1])
                sma_200 = float(close.rolling(200).mean().iloc[-1]) if len(close) > 200 else 0.0
                
                last_price = float(close.iloc[-1])
                prev_close = float(close.iloc[-2]) if len(close) > 1 else last_price
                change_pct = ((last_price / prev_close) - 1) * 100
                
                # Volume spike detection
                vol_sma = float(volume.rolling(20).mean().iloc[-1])
                last_vol = float(volume.iloc[-1])
                vol_spike = last_vol / vol_sma if vol_sma > 0 else 1.0
                
                # Trend direction
                trend = "bullish" if last_price > sma_50 > sma_200 else ("bearish" if last_price < sma_50 else "neutral")
                
                analysis = {
                    "symbol": symbol,
                    "last_price": last_price,
                    "change_pct": round(change_pct, 2),
                    "rsi_14": round(rsi, 1),
                    "sma_20": round(sma_20, 2),
                    "sma_50": round(sma_50, 2),
                    "sma_200": round(sma_200, 2),
                    "vol_spike_ratio": round(vol_spike, 2),
                    "trend": trend,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(analysis).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        # Serve static files normally
        super().do_GET()

if __name__ == "__main__":
    def load_data_thread():
        global IS_LOADING
        print("Pre-loading Yahoo Finance data into memory cache...")
        try:
            backtester.run_all(commission=0.004)
            print("\nData loaded.")
        except Exception as e:
            print(f"\nError loading data: {e}")
            traceback.print_exc()
        IS_LOADING = False

    # Start data loading in background
    threading.Thread(target=load_data_thread, daemon=True).start()
    
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        print(f"Serving at port {PORT}. Web Dashboard available at http://localhost:{PORT}")
        httpd.serve_forever()
