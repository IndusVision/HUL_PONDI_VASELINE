# utils/movement_detector.py

import joblib
import numpy as np
from queue import Queue

# shared queue and flag
movement_data_queue = Queue()
raise_flag = False

def load_movement_model(path: str):
    """
    Load and return the pre-trained SVM movement detector.
    """
    return joblib.load(path)

def calculate_value(ref_image: np.ndarray, actual_image: np.ndarray):
    """
    Compute PSNR between ref_image and actual_image, 
    then enqueue the PSNR value for the background consumer.
    """
    epsilon = 1e-6

    # resize if shapes differ
    if ref_image.shape != actual_image.shape:
        from cv2 import resize, INTER_AREA
        actual_image = resize(actual_image, (ref_image.shape[1], ref_image.shape[0]), interpolation=INTER_AREA)

    mse = np.mean((ref_image.astype(np.float32) - actual_image.astype(np.float32)) ** 2)
    if mse == 0:
        psnr = 100.0
    else:
        PIXEL_MAX = 255.0
        psnr = 20 * np.log10(PIXEL_MAX / np.sqrt(mse + epsilon))

    movement_data_queue.put(psnr)

def camera_movement(model, window_size: int = 10, threshold_trigger: int = 3):
    """
    Background loop: consumes PSNR values, maintains a sliding window,
    forms a feature vector [window + mean + std], runs the SVM,
    and sets raise_flag = True after threshold_trigger consecutive 1’s.
    """
    global raise_flag
    buffer = []
    consec = 0

    while True:
        psnr = movement_data_queue.get()
        buffer.append(psnr)
        if len(buffer) > window_size:
            buffer.pop(0)

        if len(buffer) == window_size:
            mean = float(np.mean(buffer))
            std  = float(np.std(buffer))
            features = buffer + [mean, std]              # length = window_size + 2
            pred     = model.predict([features])[0]      # 1=> movement, 0=> no movement

            if pred == 1:
                consec += 1
                if consec >= threshold_trigger:
                    raise_flag = True
            else:
                consec = 0

        movement_data_queue.task_done()
