# Bitácora de Desarrollo: Motion Amp Pro

**Proyecto:** Real-Time Eulerian Video Magnification  
**Fecha de Inicio:** 04/02/2026  
**Autor:** Antigravity (IA Assistant) & Izan

## Registro de Sesión

### [04/02/2026 - 20:17] Inicio del Proyecto
**Objetivo:** Implementar la técnica de Motion Amplification en tiempo real usando Python.
- **Acción:** Definición del algoritmo basado en *Eulerian Video Magnification (EVM)* con filtrado temporal IIR (Infinite Impulse Response) para minimizar latencia.
- **Decisión Técnica:** Se optó por un filtro IIR en lugar de FFT para evitar buffers temporales grandes y procesar flujo de video continuo.
- **Estructura:** Creación del entorno `motion-amp-pro` con `uv` (y fallback a pip), estructura de carpetas `src/`, `tests/` y `docs/`.

### [04/02/2026 - 20:25] Implementación del Motor (Engine)
**Objetivo:** Crear el núcleo de procesamiento matemático.
- **Componente:** `EVMEngine`.
- **Lógica:** Implementación de Pirámide Laplaciana para descomposición espacial (4 niveles) y filtros temporales pasabanda.
- **Pruebas:** Tests unitarios para la reconstrucción de pirámides y respuesta del filtro IIR.

### [04/02/2026 - 20:30] Pipeline Asíncrono
**Objetivo:** Desacoplar la captura de video del procesamiento.
- **Componente:** `AsyncCamera` y `ProcessingPipeline`.
- **Implementación:** Uso de `asyncio` y `ThreadPoolExecutor` para la lectura de frames (`cv2.VideoCapture`), evitando el bloqueo del bucle de eventos principal.
- **Resultado:** Captura fluida a ~30 FPS estables.

### [04/02/2026 - 20:35] Interfaz de Usuario (HUD)
**Objetivo:** Visualización de parámetros en tiempo real.
- **Diseño:** Overlay "Premium" con OpenCV (`cv2.putText`, `cv2.rectangle`).
- **Datos Mostrados:** FPS, Factor Alpha, Banda de Frecuencia.
- **Controles Iniciales:** `W/S` para Alpha, `Q` para salir.

### [04/02/2026 - 20:38] Ajuste Dinámico de Frecuencias
**Solicitud:** Permitir cambiar el rango de frecuencias (0.5 - 4 Hz) en tiempo real.
- **Cambio:** Modificación de `EVMEngine` para actualizar coeficientes del filtro IIR al vuelo.
- **Nuevos Controles:** `I/K` (Frec. Baja) y `O/L` (Frec. Alta).
- **Mejora UX:** Actualización del HUD para reflejar el estado actual del filtro.

### [04/02/2026 - 20:41] Control de Exposición/Brillo
**Solicitud:** Ajuste de brillo de la cámara.
- **Implementación:** Método `set_brightness` en `AsyncCamera` usando `cv2.CAP_PROP_BRIGHTNESS`.
- **Controles:** `U/J` para aumentar/disminuir brillo.
- **Feedback:** Visualización del valor de brillo en el HUD.

### [04/02/2026 - 20:45] Refinamiento de UX
**Corrección:** Las teclas de frecuencia eran contraintuitivas.
- **Cambio:** Reasignación de teclas para coincidir con la posición espacial (Izquierda=Baja, Derecha=Alta).
- **Estado Final:** Sistema funcional con control total sobre la amplificación, filtrado y captura.
