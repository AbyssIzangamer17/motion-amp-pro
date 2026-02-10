# Motion Amp Pro

![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.12%2B-blue) ![Status](https://img.shields.io/badge/status-stable-success)

> **Visualiza lo invisible.**  
> Un sistema de amplificación de movimiento Euleriano en tiempo real diseñado para detectar y visualizar micro-movimientos imperceptibles para el ojo humano, como el pulso sanguíneo o vibraciones mecánicas.

---

## 🚀 Características Principales

- **Real-Time Eulerian Magnification:** Utiliza filtrado temporal IIR sobre una pirámide Laplaciana.
- **Latencia Cero:** Pipeline asíncrono con `asyncio` y `ThreadPoolExecutor` para captura y procesado paralelo.
- **HUD Interactivo:** Control total de parámetros en tiempo real.
- **Ajuste Dinámico:** Modifica el rango de frecuencias (Banda Pasante), Amplificación ($\alpha$) y Brillo sin detener el video.

## 📦 Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/AbyssIzangamer17/motion-amp-pro.git
   cd motion-amp-pro
   ```

2. **Instalar dependencias:**
   ```bash
   pip install opencv-python numpy
   ```

3. **Ejecutar:**
   ```bash
   python -m src.motion_amp.main
   ```

## 🎮 Controles

| Tecla | Acción | Descripción |
| :--- | :--- | :--- |
| **W / S** | Alpha $\pm$ | Aumenta o disminuye la fuerza de la amplificación. |
| **I / K** | Frec. Baja $\pm$ | Ajusta el límite inferior del filtro (Hz). |
| **O / L** | Frec. Alta $\pm$ | Ajusta el límite superior del filtro (Hz). |
| **U / J** | Brillo $\pm$ | Controla la exposición de la cámara. |
| **Q** | Salir | Cierra la aplicación de forma segura. |

## 🧠 ¿Cómo Funciona?

Este proyecto implementa una versión optimizada del algoritmo de *Eulerian Video Magnification* (Wu et al., 2012). En lugar de usar FFT costosas computacionalmente sobre buffers grandes, utilizamos:

1.  **Descomposición Espacial:** Cada frame se descompone en una Pirámide Laplaciana de 4 niveles.
2.  **Filtrado Temporal IIR:** Cada píxel de cada nivel pasa por un filtro IIR pasa-banda recursivo.
    $$y(t) = (1-r)y(t-1) + r x(t)$$
3.  **Reconstrucción:** La señal filtrada se multiplica por $\alpha$ y se suma a la señal original, colapsando la pirámide de nuevo.

## 📂 Estructura del Proyecto

```
motion-amp-pro/
├── src/
│   ├── motion_amp/
│   │   ├── engine.py       # Núcleo EVM (Filtros + Pirámides)
│   │   ├── pipeline.py     # Gestión asíncrona de cámara
│   │   └── main.py         # Entry point y UI/HUD
├── docs/                   # Documentación y Página Web
│   ├── index.html
│   └── plans/
├── tests/                  # Tests unitarios
└── BITACORA.md             # Registro de desarrollo
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Siéntete libre de usarlo, modificarlo y compartirlo.
