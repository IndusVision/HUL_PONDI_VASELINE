import os
import csv
import numpy as np

def calculate_difference(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Compute the PSNR between two images.
    """
    epsilon = 1e-6
    mse = np.mean((image1.astype(np.float32) - image2.astype(np.float32)) ** 2)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse + epsilon))
    return psnr

def log_difference_to_csv(csv_path: str, sku: str, value: float):
    """
    Append a row [sku, value] to a CSV at csv_path, creating it (with header) if needed.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['sku', 'value'])
        writer.writerow([sku, f"{value:.4f}"])
