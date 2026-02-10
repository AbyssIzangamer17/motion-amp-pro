# Real-Time Motion Magnification Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement a real-time motion amplification system using Eulerian Video Magnification (EVM) to visualize subtle movements (e.g., pulse, mechanical vibrations) from a camera feed.

**Architecture:** A producer-consumer model using `asyncio` for the main loop and `cv2` for high-performance capture. The processing pipeline uses a Laplacian pyramid for spatial decomposition and a recursive IIR bandpass filter for temporal filtering to achieve near-zero latency.

**Tech Stack:** Python 3.12+, OpenCV, NumPy, `asyncio`.

---

### Task 1: Research & Algorithm Specification
**Files:** 
- Create: `src/motion_amp/algorithm.md`

**Description:** Document the mathematical derivation of the Eulerian Motion Magnification using IIR filters for real-time performance.
**Step 1:** Define the temporal IIR filter transfer function.
**Step 2:** Define the spatial decomposition strategy (Laplacian Pyramid levels).
**Step 3:** Establish the $\alpha$ (amplification) vs frequency limits to prevent artifacts.

### Task 2: Core Processing Engine (EVM)
**Files:**
- Create: `src/motion_amp/engine.py`
- Test: `tests/test_engine.py`

**Step 1: Write failing test for pyramid decomposition**
```python
import numpy as np
from src.motion_amp.engine import EVMEngine

def test_pyramid_reconstruction():
    engine = EVMEngine()
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    pyramid = engine.build_laplacian_pyramid(frame)
    reconstructed = engine.reconstruct_from_pyramid(pyramid)
    assert np.allclose(frame, reconstructed, atol=1)
```
**Step 2: Implement Laplacian Pyramid and Reconstruction**
**Step 3: Implement IIR Temporal Filter**
**Step 4: Verify filtering logic with synthetic oscillating signal**

### Task 3: Async Video Pipeline
**Files:**
- Create: `src/motion_amp/pipeline.py`
- Modify: `src/motion_amp/main.py`

**Step 1: Create AsyncCamera class** using a threadpool to avoid blocking the event loop on `cap.read()`.
**Step 2: Implement ProcessingLoop** that consumes frames from a queue, processes them using `EVMEngine`, and pushes to a display queue.
**Step 3: Implement graceful shutdown and resource management.**

### Task 4: Performance Optimization & Tuning
**Files:**
- Modify: `src/motion_amp/engine.py`

**Step 1: Vectorize IIR filter operations** using NumPy to process all pixels in a level simultaneously.
**Step 2: Implement Spatial ROI** (optional) or downsampling to increase FPS.
**Step 3: Optimize memory usage** by pre-allocating buffers for the pyramid levels and filter states.

### Task 5: User Interface & HUD
**Files:**
- Create: `src/motion_amp/ui.py`

**Step 1: Implement a "Premium HUD" overlay** showing current FPS, amplification factor $\alpha$, and frequency band.
**Step 2: Add keyboard controls** to adjust $\alpha$ and frequency band in real-time.
