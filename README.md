# Delfos — Quant Strategy Backtester & Dashboard v0.3

> *"Conectando al Oráculo..."*

![Version](https://img.shields.io/badge/version-0.3-blueviolet)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Este proyecto es un laboratorio interactivo de análisis cuantitativo (Backtesting) construido para simular estrategias de trading sobre **+30 años de historia** en **27 activos** (US + Europa + Oro + Volatilidad).

Combina un motor de cálculo de alta velocidad escrito en **Python** con un **Dashboard Interactivo en Vanilla JS/HTML**, operando bajo una arquitectura Cliente-Servidor local.

---

## ✨ Características Principales (v0.3)

| Característica | Descripción |
|---|---|
| 🖥️ **Motor 30 Años** | Descarga y cachea historia completa via `yfinance` para 27 activos |
| 🧠 **20 Estrategias** | 11 Simples (SS) + 9 IA (AIS): TimesFM, IBM TSPulse, MiniRocket, XGBoost |
| 🛡️ **Stop Loss Dinámico** | SL por % aplicado a cada estrategia individualmente |
| 🏆 **Mejor por Activo** | Ranking automático de la estrategia óptima para cada ticker |
| 🇪🇺 **Índices Europeos** | **NUEVO**: DE40 (EWG), IBEX35 (EWP), CAC40 (EWQ), FTSE100 (EWU), VGK, IEUR, EWL |
| 🇺🇸 **Índices USA** | SPY, QQQ, DIA, IWM + Volatilidad (^VIX) y Bonos (TLT) |
| 📊 **Análisis en Tiempo Real** | **NUEVO**: Panel de precios en vivo con 9 tickers clave en la sidebar |
| 🔔 **Alertas Inteligentes** | **NUEVO**: Alertas de precio (superior/inferior), persistidas en localStorage |
| ⚡ **Live Analysis API** | **NUEVO**: Endpoint `/api/live-analysis` con RSI, SMAs, tendencia y spikes |
| 💹 **Cálculo Dinámico de Comisiones** | Ajusta comisiones y recálculo instantáneo en milisegundos |
| 📜 **Exportación Pine Script v5** | Cada estrategia genera su código Pine Script listo para TradingView |

## 🚀 Requisitos de Instalación

```bash
# Opción 1: Instalador automático Windows
install_windows_nvidia.bat

# Opción 2: Manual con uv
uv sync
```

*Para aprovechar todas las estrategias de IA (AIS01-AIS09) se requiere aceleración por hardware (NVIDIA GPU).*

## 💻 ¿Cómo ejecutar el Dashboard?

```bash
# 1. Pre-calcular predicciones IA (diario/semanal)
./actualizar_ia.bat

# 2. Lanzar servidor web + dashboard (carga datos automáticamente)
uv run python web/server.py

# 3. Abrir navegador en:
#    http://localhost:8000
```

## 📊 Datasets Admitidos (27 activos)

### 🇺🇸 US Core & Megacaps
| Ticker | Nombre | Tipo |
|--------|--------|------|
| SPY | S&P 500 ETF | Índice US |
| QQQ | Nasdaq 100 ETF | Índice US |
| DIA | Dow Jones ETF | Índice US |
| IWM | Russell 2000 ETF | Small Cap US |
| MSFT | Microsoft | Mega Cap |
| GOOG | Alphabet | Mega Cap |
| V | Visa | Financial |
| BRK-B | Berkshire Hathaway | Conglomerado |

### 🇺🇸 US Dividend & Financial
| Ticker | Nombre | Tipo |
|--------|--------|------|
| MCD | McDonald's | Dividend Aristocrat |
| KO | Coca-Cola | Dividend Aristocrat |
| O | Realty Income | REIT |
| XOM | Exxon Mobil | Energy |
| C | Citigroup | Financial |

### 🌎 Emerging & Commodities
| Ticker | Nombre | Tipo |
|--------|--------|------|
| NU | Nubank | Fintech LatAm |
| EWZ | iShares MSCI Brazil | Emerging |
| PBR | Petrobras | Oil & Gas |
| GLD | SPDR Gold Trust | Commodity |
| IVE | S&P 500 Value ETF | Factor |

### 🇪🇺 **NUEVO** — European Indices (v0.3)
| Ticker | Nombre | Proxy de |
|--------|--------|----------|
| **EWG** | iShares MSCI Germany | **DE40** (DAX) |
| **EWP** | iShares MSCI Spain | **IBEX35** |
| **EWQ** | iShares MSCI France | CAC40 |
| **EWU** | iShares MSCI UK | FTSE100 |
| **VGK** | Vanguard FTSE Europe | Europa Total |
| **IEUR** | iShares Core MSCI Europe | Europa Desarrollada |
| **EWL** | iShares MSCI Switzerland | Suiza |

### 📉 **NUEVO** — Volatilidad y Bonos (v0.3)
| Ticker | Nombre | Tipo |
|--------|--------|------|
| **^VIX** | CBOE Volatility Index | Volatilidad |
| **TLT** | iShares 20+ Year Treasury | Bonos Largos |

## 📈 Estrategias Incluidas (20)

### Simple Strategies (SS01-SS11)
- **SS01**: Macro + Extremo Volumen & Momentum (ROC 3d > 10% + Vol 2x)
- **SS02**: Macro + Volatilidad de Precio 5D (ROC 5d > 15% + Vol 2x)
- **SS03**: Macro + Despegue Agresivo (ROC 5d > 10%)
- **SS04**: Macro + Spike Volumen x3
- **SS05**: Macro + ROC Extremo 15%
- **SS06**: Macro + Momentum Puro 3 Días (SL -15%)
- **SS07**: Macro + Anomalía de Volumen Alcista
- **SS08**: Macro + Donchian Channel Breakout (SL -25%)
- **SS09**: Macro + Exhaustion Flow Index (SL -10%)
- **SS10**: Macro + Bollinger Ultra Estirado (SL -15%)
- **SS11**: Macro Base Pura (Buy & Hold con Seguro Anti-Crash, SL -15%)

### AI Strategies (AIS01-AIS09)
- **AIS01**: TimesFM 200M AI Oracle — Predicción Pura
- **AIS02**: TimesFM Smart Hold
- **AIS03**: TimesFM Adaptive Volatility
- **AIS04**: IBM TSPulse AI Univariada
- **AIS05**: IBM TSPulse AI Híbrida (MFI & BB)
- **AIS06**: IBM TSPulse AI Híbrida (Momentum)
- **AIS07**: MiniRocket AI Binary Classification
- **AIS08**: MiniRocket+ GPU Probabilities
- **AIS09**: MiniRocket + XGBoost Stack

## 🆕 Novedades de v0.3

### 🇪🇺 9 Nuevos Activos Europeos
Se han añadido ETFs que replican los principales índices europeos:
- **EWG** → Proxy del DAX 40 alemán (DE40)
- **EWP** → Proxy del IBEX 35 español
- **EWQ** → Proxy del CAC 40 francés
- **EWU** → Proxy del FTSE 100 británico
- **VGK / IEUR** → Exposición amplia a Europa
- Además: **^VIX** (Volatilidad) y **TLT** (Bonos USA largos)

### 📊 Análisis en Tiempo Real
Nuevo widget en la sidebar que muestra los precios en vivo de los 9 tickers clave con:
- Cambio porcentual respecto a la última lectura
- Código de colores (verde = subida, roja = bajada)
- Actualización automática cada 30 segundos via `/api/live-prices`
- Nuevo endpoint `/api/live-analysis` con RSI, SMAs y tendencia

### 🔔 Sistema de Alertas
Crea alertas personalizadas directamente desde el dashboard:
- **Alertas de precio**: Te notifica cuando un activo supera o cae por debajo de un umbral
- Persistencia en localStorage del navegador
- Notificaciones toast visuales cuando se disparan

### 🐛 Correcciones
- Corregido el script tag de Chart.js (usaba `href` en vez de `src`)
- Arreglada codificación Unicode en descripción de MiniRocket (`estǭ` -> `está`)
- Server API mejorada con headers CORS y caché de precios en vivo (30s)
- Mejor manejo de errores en descarga de precios multi-ticker (yfinance multi-index)

### 📚 Documentación
- Añadidos docstrings completos en `backtester.py` para todas las funciones principales
- README actualizado con secciones documentadas para cada activo y endpoint
- CHANGELOG.md actualizado

## 📐 Arquitectura del Proyecto

```
IABacktesterTrading/
├── backtester.py          # Motor principal (v0.3: 27 tickers, docstrings)
├── web/
│   ├── server.py          # API Server (v0.3: +live-analysis, +cache 30s, +CORS)
│   ├── index.html         # Dashboard UI (v0.3: +alertas, +precios vivo, +27 tickers)
│   ├── app.js             # Frontend logic (v0.3: +live prices, +alertas)
│   └── styles.css         # Styles (v0.3: +widget precios, +alert items)
├── models/
│   ├── scripts/           # Scripts de optimización y tests
│   └── train_*.py         # Entrenamiento de modelos IA (TimesFM, TSPulse, MiniRocket)
├── utils/                 # Utilidades de backtesting y búsqueda
├── data/                  # Resultados cacheados (results.json)
│   └── results.json       # Último resultado de backtesting
├── .data_cache/           # Caché de CSVs de precios (gitignored)
├── CHANGELOG.md           # Historial de versiones
└── README.md              # Este archivo
```

## 🔌 Endpoints API

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/status` | GET | Estado del servidor (loading/completo) |
| `/api/recalculate` | GET | Recálculo completo con comisiones ajustables (`?commission=0.4&start_date=...`) |
| `/api/live-prices` | GET | Precios en tiempo real de los 27 activos (caché 30s) |
| `/api/live-analysis` | GET | Análisis técnico en vivo: RSI, SMAs, tendencia, volumen (v0.3) |
