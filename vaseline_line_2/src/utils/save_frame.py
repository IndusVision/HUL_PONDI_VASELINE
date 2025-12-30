import os
import cv2
import logging
import numpy as np
from datetime import datetime

class SaveFrame:
    def __init__(self, output_dir, machine_id, department, plant_id, department_id, product_id, defect_id):
        self.output_dir = output_dir
        self.machine_id = machine_id
        self.department = department
        self.plant_id = plant_id
        self.department_id = department_id
        self.product_id = product_id
        self.defect_id = defect_id  # default defect id

    def save_defect_frame(self, frame, defect_id=None):
        """
        Save a frame to disk. If `defect_id` is provided, it overrides the default.
        """
        use_defect_id = self.defect_id if defect_id is None else defect_id
        os.makedirs(self.output_dir, exist_ok=True)
        uuid_int = np.random.randint(100000000, 999999999)
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        fname = f"{self.plant_id}_{self.machine_id}_{self.department_id}_{self.product_id}_{use_defect_id}_{timestamp}_{uuid_int}.png"
        path = os.path.join(self.output_dir, fname)
        cv2.imwrite(path, frame)
        logging.info("Defect image saved: %s", path)
