import asyncio
import cv2
import time
import numpy as np
from typing import Optional, Callable
from concurrent.futures import ThreadPoolExecutor

class AsyncCamera:
    def __init__(self, device_id: int = 0, width: int = 640, height: int = 480):
        self.device_id = device_id
        self.width = width
        self.height = height
        self.cap = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self.running = False

    async def start(self):
        self.cap = cv2.VideoCapture(self.device_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera {self.device_id}")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.running = True

    async def get_frame(self) -> Optional[np.ndarray]:
        if not self.running: return None
        loop = asyncio.get_running_loop()
        success, frame = await loop.run_in_executor(self._executor, self.cap.read)
        if not success: return None
        return frame

    def set_brightness(self, value: float):
        if self.cap:
            # OpenCV brightness is typically 0-255 or 0-1 depending on driver
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self) -> float:
        if self.cap:
            return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        return 0.0

    def stop(self):
        self.running = False
        if self.cap: self.cap.release()
        self._executor.shutdown()

class ProcessingPipeline:
    def __init__(self, engine, camera: AsyncCamera):
        self.engine = engine
        self.camera = camera
        self.alpha = 50.0
        self.is_running = False
        self._fps_internal = 0.0
        self._frame_count = 0
        self._start_time = 0

    async def run(self, on_frame: Callable[[np.ndarray, float], None]):
        self.is_running = True
        self._start_time = time.time()
        try:
            while self.is_running:
                frame = await self.camera.get_frame()
                if frame is None:
                    await asyncio.sleep(0.01)
                    continue
                processed = self.engine.process_frame(frame, alpha=self.alpha)
                self._frame_count += 1
                elapsed = time.time() - self._start_time
                if elapsed > 1.0:
                    self._fps_internal = self._frame_count / elapsed
                    self._frame_count = 0
                    self._start_time = time.time()
                on_frame(processed, self._fps_internal)
                await asyncio.sleep(0)
        finally:
            self.stop()

    def stop(self):
        self.is_running = False
        self.camera.stop()
