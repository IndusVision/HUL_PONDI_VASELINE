# Standard Library
import json
import base64
import logging
import os
import sys
import psutil
import platform
import threading
from datetime import datetime
import time

# Third-Party Libraries
import cv2
import torch
import numpy as np
import snap7
import snap7.util
from ultralytics import YOLO
import torchvision.ops as ops
import utils.movement_detector as md

# Local Modules
from utils import mvsdk
from utils.camera import Camera
from utils.crqs import params
# Custom logging setup
from utils.logger_configuration import setup_logger  
from utils.plc import PLC
from utils.save_frame import SaveFrame
from utils.global_dashboard import Dashboard

ROOT_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
print("ROOT DIR",ROOT_DIR)

LOG_DIR = os.path.join(ROOT_DIR, "vaseline_line_2","logs","L2_ocr_log_files")
os.makedirs(LOG_DIR, exist_ok=True)

setup_logger(LOG_DIR)


class CameraProcess:
    """
    Handles the end-to-end process of defect detection using camera feed,
    object detection, and PLC communication, with PSNR logging.
    """

    def __init__(self, json_content, defect_config, parent_id):
        # Load config values
        self.camera_config = os.path.join(ROOT_DIR, json_content['camera_config_ocr'])
        self.camera_serial_no = json_content['camera_serial_number']
        self.ocr_weights = json_content[ "ocr_weights"]
        self.output_dir = r'\\wsl.localhost\Ubuntu-22.04\home\hul\vin_images\images'
        self.default_conf = 0.4
        self.iou_thersh = json_content['iou_thersh']
        self.ocr_count = json_content['ocr_count']
        self.plc_ip = '192.168.21.10'
        # # self.data_collection = (
        # #     r"Z:\Data_collection\ocr_line_2"
        # )
        self.rack = 0
        self.slot = 1
        self.db_number = 1
        self.start_offset = json_content['start_offset']
        self.bit_offset = json_content['bit_offset']
        self.recipe_start_offset = json_content["recipe_start_offset"]
        self.recipe_bit_offset = json_content["recipe_bit_offset"]
        self.ocr_save_frame = defect_config['defects']['Coding_Error']  # bool toggle
        self.value = 1
        self.dashboard_url = 'http://localhost:8000/api/dashboard/'
        self.params_url = 'http://localhost:8000/api/params_graph/'
        self.image_write_path = os.path.join(
            ROOT_DIR, "gui_python_config","camera_all_line_feed.json"
        )

        # Defect IDs
        self.defect_id = 85               # default defect id
        self.clamp_defect_id = 88         # used when class_clamp_count == 0
        self.params_sender = params(self.params_url)

        # Asset metadata
        self.department_id = 22
        self.plant_id = 10
        self.machine_id = 32
        self.product_id = json_content["product_id"]
        self.frame_count = 0
        self.valid_product_count=0
        self.prev_frame = None 


        # Ensure data dirs exist
        # os.makedirs(self.output_dir, exist_ok=True)
        # os.makedirs(self.data_collection, exist_ok=True)

        # Initialize interfaces
        self.plc = PLC(
             self.plc_ip,
            self.rack, self.slot,
            self.db_number,
            self.start_offset,
            self.bit_offset,
            self.recipe_start_offset,
            self.recipe_bit_offset,
            value=False
        )
        self.camera = Camera(
            self.camera_serial_no,
            self.camera_config,
            "Line_2_OCR",
            self.image_write_path
        )
        self.save_frame = SaveFrame(
            output_dir=self.output_dir,
            machine_id=self.machine_id,
            department=self.department_id,
            plant_id=self.plant_id,
            department_id=self.department_id,
            product_id=self.product_id,
            defect_id=self.defect_id  # default; can be overridden per call
        )

        self.h_camera = None
        self.p_frame_buffer = None
        self.plc_conn = None
        self.parent_id = parent_id

    def detect_defects(self, model, frame):
        """
        Detects defects using a YOLO model on a given frame.
        Applies NMS and decides whether to save the frame.
        Returns:
            save_frame_flag (bool), annotated_frame (np.ndarray), class_clamp_count (int)
        """
        class_clamp_count = 0
        save_frame_flag = False
        total_class_detected = 0

        results = model(
            frame,
            conf=self.default_conf,
            iou=self.iou_thersh,
            verbose=False,
            save=False
        )

        if not results or not results[0].boxes:
            logging.info("No detections found.")
            return True, frame, class_clamp_count

        boxes, scores, classes = [], [], []

        for detection in results[0].boxes:
            cls = int(detection.cls.cpu().item())
            box = detection.xyxy[0].cpu()

            x1, y1, x2, y2 = map(int, box.tolist())

            if cls == 1:
                class_clamp_count += 1
            boxes.append(box)
            scores.append(detection.conf.cpu())
            classes.append(cls)

        if not boxes:
            save_frame_flag = self.ocr_save_frame
            return save_frame_flag, frame, class_clamp_count

        boxes = torch.stack(boxes)
        scores = torch.tensor(scores)
        keep = ops.nms(boxes, scores, iou_threshold=self.iou_thersh)
        kept_boxes = boxes[keep]

        for box in kept_boxes:
            total_class_detected += 1
            x1, y1, x2, y2 = map(int, box.tolist())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

        logging.info("Total detected items (after NMS): %d", total_class_detected)

        if total_class_detected < self.ocr_count or class_clamp_count == 0:
            logging.info("Defect detected: %d", total_class_detected)
            save_frame_flag = self.ocr_save_frame

        return save_frame_flag, frame, class_clamp_count

    def run(self):
        """
        Main loop to start camera, detect defects, and talk to PLC.
        """
        self.h_camera, self.p_frame_buffer = self.camera.initialize_camera()
        self.plc_conn = self.plc.initialize_plc_connection()
        model = YOLO(self.ocr_weights)
        model.to("cuda" if torch.cuda.is_available() else "cpu")
        total_inference_time = 0

        try:
            frame_counter = 0

            while (cv2.waitKey(1) & 0xFF) != ord('q'):
                #------------------------------
                if __name__ != "__main__":
                    if not psutil.pid_exists(self.parent_id):
                        print("Parent died — exiting child.")
                        sys.exit(0)
                #------------------------------
                
            
                total_inference_time = 0
                start_time = time.time()
                frame = self.camera.capture_frame(self.h_camera, self.p_frame_buffer)
                end_time = time.time()
                inference_time = (end_time-start_time)*1000
                total_inference_time += inference_time
                logging.info(f"Time taken to capture frame is {inference_time}")
                if frame is None:
                    continue

                frame_counter += 1
                if frame_counter >= self.frame_count:
                    frame_counter = 0

                start_time = time.time()
                has_defect, annotated_frame, class_clamp_count = self.detect_defects(model, frame)
                end_time = time.time()
                inference_time = (end_time-start_time)*1000
                total_inference_time += inference_time
                logging.info(f"Time taken to detect defect is {inference_time}")


                resized_frame = cv2.resize(annotated_frame, (360, 480))
                cv2.imshow("ocr_l2", resized_frame)

      # Increment count for every product (defect or no defect)
                self.valid_product_count += 1

                # Send count every 500 products
                if self.valid_product_count >= 500:
                    try:
                        self.params_sender.send_params(self.valid_product_count)
                    except:
                        logging.exception("Failed to send params")

                    # Reset counter
                    self.valid_product_count = 0      

                if has_defect:
                    # Trigger PLC only when a defect is detected
                    start_time = time.time()
                    self.plc.value=True
                    self.plc.trigger_both(self.plc_conn)
                    end_time = time.time()
                    inference_time = (end_time-start_time)*1000
                    total_inference_time += inference_time
                    logging.info(f"Time taken to trigger plc is {inference_time}")


                    # Choose defect id: if no clamp found, use clamp_defect_id
                    chosen_defect_id = self.clamp_defect_id if class_clamp_count == 0 else self.defect_id

                    # Save with chosen defect id (overrides default)
                    self.save_frame.save_defect_frame(annotated_frame, defect_id=chosen_defect_id)

                    #logging.info(f"Inference time for one iteration is {total_inference_time}")

                else:
                    self.plc.value=False
                    self.plc.trigger_both(self.plc_conn)


                #     self.valid_product_count += 1
                #     if self.valid_product_count >= 500:
                #         try:
                #             self.params_sender.send_params(self.valid_product_count)
                #         except:

                #              logging.exception("Failed to send params")
                #         self.valid_product_count = 0  # reset after sending

               
        finally:
            if self.h_camera:
                mvsdk.CameraUnInit(self.h_camera)
                mvsdk.CameraAlignFree(self.p_frame_buffer)
                cv2.destroyAllWindows()

            if self.plc_conn:
                self.plc_conn.disconnect()
                logging.info("PLC connection closed")

def load_config(config_path):
    """
    Loads and parses JSON configuration file.
    """
    with open(config_path,"r") as f:
        return json.load(f)


if __name__ == "__main__":
    PARENT_ID = int(sys.argv[1])

    ocr_config_path = os.path.join(
        ROOT_DIR, "gui_python_config", "Line_2_Code_Config.json"
    )
    defect_config_path = os.path.join(
        ROOT_DIR,"gui_python_config","Defect_Toggle.json"
    )

    json_content = load_config(ocr_config_path)
    defect_config = load_config(defect_config_path)

    camera_process = CameraProcess(json_content, defect_config, PARENT_ID)
    camera_process.run()




