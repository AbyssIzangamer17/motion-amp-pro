import numpy as np
from src.motion_amp.engine import EVMEngine

def test_pyramid_reconstruction():
    engine = EVMEngine(levels=2)
    frame = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    pyramid = engine.build_laplacian_pyramid(frame.astype(np.float32))
    reconstructed = engine.reconstruct_from_pyramid(pyramid)
    reconstructed_uint8 = np.clip(reconstructed, 0, 255).astype(np.uint8)
    assert np.allclose(frame, reconstructed_uint8, atol=2)

def test_iir_filter():
    engine = EVMEngine()
    x = np.ones((10, 10))
    band, low, high = engine._iir_filter_step(x, None, None, 0.1, 0.2)
    assert band.shape == (10, 10)
    assert np.all(band == 0) # First step is zero
