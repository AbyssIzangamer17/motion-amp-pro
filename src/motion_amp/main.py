import asyncio
import cv2
import numpy as np
import sys
from .engine import EVMEngine
from .pipeline import AsyncCamera, ProcessingPipeline

def draw_hud(frame, alpha, fps, low_f, high_f, brightness):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (280, 150), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 255, 100)
    cv2.putText(frame, "MOTION AMP PRO v1.0", (20, 35), font, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 65), font, 0.5, color, 1)
    cv2.putText(frame, f"ALPHA: {alpha:.1f} (W/S)", (20, 85), font, 0.5, color, 1)
    cv2.putText(frame, f"BAND: {low_f:.1f}-{high_f:.1f} Hz (I/K-O/L)", (20, 105), font, 0.5, color, 1)
    cv2.putText(frame, f"BRIGHTNESS: {brightness:.1f} (U/J)", (20, 125), font, 0.5, color, 1)
    cv2.putText(frame, "PRESS 'Q' TO EXIT", (20, 145), font, 0.4, (100, 100, 255), 1)
    cv2.rectangle(frame, (10, 10), (280, 150), color, 1)

async def main():
    WIDTH, HEIGHT = 640, 480
    TARGET_FPS = 30.0
    engine = EVMEngine(levels=4, low_freq=0.5, high_freq=4.0, fps=TARGET_FPS)
    camera = AsyncCamera(device_id=0, width=WIDTH, height=HEIGHT)
    pipeline = ProcessingPipeline(engine, camera)
    await camera.start()
    print("Starting Motion Amplification...")
    def handle_frame(processed_frame, fps):
        brightness = camera.get_brightness()
        draw_hud(processed_frame, pipeline.alpha, fps, engine.low_freq, engine.high_freq, brightness)
        cv2.imshow("Motion Amp Pro", processed_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): pipeline.is_running = False
        elif key == ord('w'): pipeline.alpha += 10.0
        elif key == ord('s'): pipeline.alpha = max(0.0, pipeline.alpha - 10.0)
        elif key == ord('i'): engine.update_frequencies(low_freq=engine.low_freq + 0.1)
        elif key == ord('k'): engine.update_frequencies(low_freq=engine.low_freq - 0.1)
        elif key == ord('o'): engine.update_frequencies(high_freq=engine.high_freq + 0.1)
        elif key == ord('l'): engine.update_frequencies(high_freq=engine.high_freq - 0.1)
        elif key == ord('u'): camera.set_brightness(brightness + 0.05)
        elif key == ord('j'): camera.set_brightness(brightness - 0.05)
    print("Starting pipeline loop...")
    try:
        await pipeline.run(on_frame=handle_frame)
    except Exception as e:
        print(f"Error in pipeline: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Cleaning up...")
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
