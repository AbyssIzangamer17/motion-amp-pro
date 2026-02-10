import cv2
import numpy as np
from typing import List, Tuple, Optional

class EVMEngine:
    def __init__(self, levels: int = 4, low_freq: float = 0.4, high_freq: float = 3.0, fps: float = 30.0):
        self.levels = levels
        self.low_freq = low_freq
        self.high_freq = high_freq
        self.fps = fps
        self._filter_state_low = [None] * (levels + 1)
        self._filter_state_high = [None] * (levels + 1)
        self.r_low = 1.0 - np.exp(-2.0 * np.pi * low_freq / fps)
        self.r_high = 1.0 - np.exp(-2.0 * np.pi * high_freq / fps)

    def build_laplacian_pyramid(self, frame: np.ndarray) -> List[np.ndarray]:
        pyramid = []
        current = frame.astype(np.float32)
        for i in range(self.levels):
            down = cv2.pyrDown(current)
            up = cv2.pyrUp(down, dstsize=(current.shape[1], current.shape[0]))
            laplacian = current - up
            pyramid.append(laplacian)
            current = down
        pyramid.append(current)
        return pyramid

    def reconstruct_from_pyramid(self, pyramid: List[np.ndarray]) -> np.ndarray:
        current = pyramid[-1]
        for i in reversed(range(len(pyramid) - 1)):
            up = cv2.pyrUp(current, dstsize=(pyramid[i].shape[1], pyramid[i].shape[0]))
            current = up + pyramid[i]
        return current

    def _iir_filter_step(self, x: np.ndarray, last_low: Optional[np.ndarray], 
                        last_high: Optional[np.ndarray], r_low: float, r_high: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if last_low is None:
            new_low = x.copy()
            new_high = x.copy()
        else:
            new_low = (1.0 - r_low) * last_low + r_low * x
            new_high = (1.0 - r_high) * last_high + r_high * x
        bandpass = new_high - new_low
        return bandpass, new_low, new_high

    def process_frame(self, frame: np.ndarray, alpha: float = 50.0) -> np.ndarray:
        pyramid = self.build_laplacian_pyramid(frame)
        magnified_pyramid = []
        for i, level in enumerate(pyramid):
            bandpassed, new_low, new_high = self._iir_filter_step(
                level, self._filter_state_low[i], self._filter_state_high[i],
                self.r_low, self.r_high
            )
            self._filter_state_low[i] = new_low
            self._filter_state_high[i] = new_high
            level_alpha = alpha * (1.0 - i / (self.levels + 1))
            magnified_level = level + level_alpha * bandpassed
            magnified_pyramid.append(magnified_level)
        reconstructed = self.reconstruct_from_pyramid(magnified_pyramid)
        return np.clip(reconstructed, 0, 255).astype(np.uint8)

    def update_frequencies(self, low_freq: Optional[float] = None, high_freq: Optional[float] = None):
        """Updates the filter constants in real-time."""
        if low_freq is not None:
            self.low_freq = max(0.1, low_freq)
            self.r_low = 1.0 - np.exp(-2.0 * np.pi * self.low_freq / self.fps)
        if high_freq is not None:
            self.high_freq = max(self.low_freq + 0.1, high_freq)
            self.r_high = 1.0 - np.exp(-2.0 * np.pi * self.high_freq / self.fps)
        # We don't reset filters here to avoid flickering, but the constants change
    def reset_filters(self):
        self._filter_state_low = [None] * (self.levels + 1)
        self._filter_state_high = [None] * (self.levels + 1)
