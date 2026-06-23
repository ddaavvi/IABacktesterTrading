# Changelog

Todas las actualizaciones notables de este proyecto estarán documentadas en este archivo.

## [0.3.0] - 2026-06-22
### Añadido
- **9 Nuevos Activos Europeos:** EWG (DE40/Germany), EWP (IBEX35/Spain), EWQ (CAC40/France), EWU (FTSE100/UK),
  VGK (FTSE Europe), IEUR (MSCI Europe), EWL (Switzerland), ^VIX (Volatility), TLT (Treasuries).
  Total: de 18 a 27 activos.
- **Panel de Precios en Tiempo Real:** Widget en la sidebar con los 9 tickers clave, cambio % y colores.
- **Sistema de Alertas:** Alertas de precio (superior/inferior) con persistencia en localStorage y notificaciones toast.
- **Live Analysis API:** Nuevo endpoint `/api/live-analysis` que devuelve RSI, SMAs, tendencia y detección de spikes de volumen.
- **Caché de Precios en Vivo:** Server-side cache de 30s para evitar rate-limiting de Yahoo Finance.
- **Documentación Completa:** Docstrings en todas las funciones principales de `backtester.py`.

### Modificado
- **TICKERS expandido:** De 18 a 27 activos en `backtester.py`. Incluye `TICKER_DESCRIPTIONS` para los nuevos.
- **README.md actualizado:** Documentación completa con tablas de activos, endpoints API y novedades v0.3.
- **Filtro de tickers en Sidebar:** Ahora incluye las nuevas opciones europeas y de volatilidad.
- **Server API:** Headers CORS añadidos, caché de 30s en `/api/live-prices`, mejor manejo de errores con yfinance multi-index.

### Corregido
- **Chart.js script tag:** Usaba `href` en lugar de `src` — corregido.
- **MiniRocket Unicode:** `estǭ` corregido a `está` en la descripción de Pine Script.
- **Manejo de errores multi-ticker:** Server ahora tolera fallos parciales en descarga de precios.

## [0.2.0] - 2026-06-19
### Añadido
- **20 Estrategias Oficiales:** Reorganización del set de estrategias. Ahora se dividen en Simple Strategies (`SS01` a `SS11`) y Artificial Intelligence Strategies (`AIS01` a `AIS09`).
- **Soporte IA Extendido:** Implementación de pipelines de inferencia local para Google TimesFM, IBM TSPulse y MiniRocket con ensamblados en XGBoost.
- **Módulo de Stop Loss:** Implementación nativa en `backtester.py` para soportar `stop_loss_pct` dinámico por operación. Aplicado el punto dulce óptimo en las estrategias que lo requerían (-10% a -15%).
- **Pestaña "Mejor por Activo":** Nueva funcionalidad en el Dashboard web que ranquea dinámicamente y expone la estrategia de mayor retorno total para cada ticket específico (ej: MSFT, GOOG, GLD).

### Modificado
- **Refactor del Nomenclador:** Se eliminó la nomenclatura antigua "V9/V10/V11" de las descripciones y del frontend en favor de "SS" y "AIS".
- **Limpieza de Hardware Hardcodeado:** Se abstrajeron referencias estáticas a GPUs particulares y se actualizaron los paths absolutos para mejorar la portabilidad del código hacia GitHub.
- **Generación de PineScript:** Ahora las salidas inyectan automáticamente el bloque de `strategy.exit()` si la estrategia requiere Stop Loss.

## [0.1.0] - Versión Inicial
- Arquitectura inicial cliente-servidor con motor en Python y frontend interactivo.
- Carga de historial a 30 años vía Yahoo Finance.
- Polling en tiempo real para cotizaciones.
- Soporte inicial de estrategias puras (Momentum, Volatilidad, ROC).
