# Standard Library
import json
import logging
from datetime import datetime
import base64
import os
import platform
import sys
import psutil

# Third-Party Libraries
import cv2
import torch
import numpy as np
import snap7
import snap7.util
from ultralytics import YOLO
import torchvision.ops as ops

# Local Modules
from utils import mvsdk
from utils.camera import Camera
from utils.plc import PLC
from utils.save_frame import SaveFrame
from utils.global_dashboard import Dashboard

ROOT_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
print("ROOT DIR",ROOT_DIR)

LOG_DIR = os.path.join(ROOT_DIR, "vaseline_line_2", "logs","L2_bf_log_files")
os.makedirs(LOG_DIR, exist_ok=True)




class CameraProcess:
    """
    Handles camera initialization, defect detection before filling,
    and PLC communication.
    """

    def __init__(self, json_content, defect_config, parent_id):
        """
        Initialize the camera process and related configuration.

        Args:
            json_content (dict): Configuration from JSON file.
            defect_config (dict): Defect toggle settings.
        """
        self.camera_config = json_content['camera_config_before_filling']
        self.camera_serial_no = '054121020060'
        self.model_weights = os.path.join( ROOT_DIR ,"Models", "empty_jar_best.pt"
        )
        self.output_dir = (
            r'\\wsl.localhost\Ubuntu-22.04\home\hul\vin_images\images'
        )
        self.default_conf = 0.8
        self.iou_thersh = json_content['iou_thersh']
        self.plc_ip = '192.168.21.10'
        self.save_defect_foreign = defect_config['defects'][
            'Foreign_particals_after_filling'
        ]
        # self.data_collection = (
        #    r"Z:\Data_collection\before_filling_line_2"
        # )
        self.rack = 0
        self.slot = 1
        self.db_number = 1
        self.start_offset = 8
        self.bit_offset = 0
        self.recipe_start_offset = json_content["recipe_start_offset"]
        self.recipe_bit_offset = json_content["recipe_bit_offset"]
        self.value = 1
        self.dashboard_url = 'http://localhost:8000/api/dashboard/'
        self.params_url = 'http://localhost:8000/api/params_graph/'
        self.image_write_path = os.path.join(
            ROOT_DIR, "gui_python_config","camera_all_line_feed.json"
        )
        self.defect_id = 87
        self.department_id = 22
        self.plant_id = 10
        self.machine_id = 32
        self.product_id = json_content["product_id"]
        self.frame_count = 0

        # Initialize interfaces
        self.plc = PLC(
            self.plc_ip, self.rack, self.slot,
            self.db_number, self.start_offset, self.bit_offset,self.recipe_start_offset,self.recipe_bit_offset
        )
        self.camera = Camera(
            self.camera_serial_no,
            self.camera_config,
            "Line_2_Before_Filling",
            self.image_write_path
        )
        self.save_frame = SaveFrame(
            output_dir=self.output_dir,
            machine_id=self.machine_id,
            department=self.department_id,
            plant_id=self.plant_id,
            department_id=self.department_id,
            product_id=self.product_id,
            defect_id=self.defect_id
        )

        self.h_camera = None
        self.p_frame_buffer = None

        self.parent_id = parent_id

    def initialize_model(self):
        """
        Initialize YOLO model on CUDA.

        Returns:
            YOLO: Loaded model.
        """
        device = torch.device('cuda')
        logging.info(f"Using device: {device}")
        model = YOLO(self.model_weights)
        return model

    def detect_defects(self, model, frame):
        """
        Detect defects in the given frame using YOLO.

        Args:
            model (YOLO): The trained YOLO model.
            frame (np.ndarray): Image frame.

        Returns:
            tuple: (bool, np.ndarray) whether defect found, and annotated frame.
        """
        save_frame = False
        results = model(
            frame,
            conf=self.default_conf,
            verbose=False,
            save=False
        )

        if not results or not results[0].boxes:
            return save_frame, frame

        annotated_frame = frame.copy()

        for detection in results[0].boxes:
            cls = int(detection.cls.cpu().item())
            x1, y1, x2, y2 = map(int, detection.xyxy[0].cpu().tolist())

            if cls == 1:
                cv2.rectangle(
                    annotated_frame,
                    (x1, y1), (x2, y2),
                    (0, 0, 255), 1
                )
                save_frame = self.save_defect_foreign

        return save_frame, annotated_frame
    
    # #   # #To save the all the images captured by the camera
    # def save_raw_frame(self, frame):
    #     timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
    #     filename = os.path.join(self.data_collection, f"raw_frame_{timestamp}.jpg")
    #     cv2.imwrite(filename, frame)
    #     logging.info(f"Raw frame saved: {filename}")

    def run(self):
        """
        Main processing loop to capture, detect, and handle defects.
        """
        self.h_camera, self.p_frame_buffer = self.camera.initialize_camera()
        self.plc_conn = self.plc.initialize_plc_connection()
        model = self.initialize_model()

        try:
            frame_counter = 0

            while (cv2.waitKey(1) & 0xFF) != ord('q'):

                #------------------------------
                if __name__ != "__main__":
                    if not psutil.pid_exists(self.parent_id):
                        print("Parent died — exiting child.")
                        sys.exit(0)
                #------------------------------

                frame = self.camera.capture_frame(
                    self.h_camera, self.p_frame_buffer
                )

                if frame is None:
                    continue

                frame_counter += 1
                if frame_counter >= 1:
                    # Placeholder for PLC write if needed
                    frame_counter = 0

                has_defect, annotated_frame = self.detect_defects(
                    model, frame
                )

                resized_frame = cv2.resize(annotated_frame, (360, 480))
                cv2.imshow("before filling", resized_frame)

                # self.save_raw_frame(frame)

                if has_defect:
                    self.save_frame.save_defect_frame(annotated_frame)
                    self.plc.trigger_plc(self.plc_conn)
                    print("Defect detected")

        finally:
            # Release resources
            if self.h_camera:
                mvsdk.CameraUnInit(self.h_camera)
                mvsdk.CameraAlignFree(self.p_frame_buffer)

            cv2.destroyAllWindows()

            if self.plc_conn:
                self.plc_conn.disconnect()
                logging.info("PLC connection closed")


def load_config(config_path):
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): Path to config file.

    Returns:
        dict: Parsed configuration.
    """
    with open(config_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    
    PARENT_ID = int(sys.argv[1])
    ocr_config_path = os.path.join(
        ROOT_DIR, "gui_python_config", "Line_2_Code_config.json")
    
    defect_config_path = defect_config_path = os.path.join(
        ROOT_DIR,"gui_python_config","Defect_Toggle.json"
    )
    json_content = load_config(ocr_config_path)
    defect_config = load_config(defect_config_path)

    camera_process = CameraProcess(json_content, defect_config, PARENT_ID)
    camera_process.run()
