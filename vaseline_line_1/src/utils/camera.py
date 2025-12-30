# Standard Library
import os
import base64
import json
import logging
import platform
import sys

# Third-Party Libraries
import cv2
import numpy as np

# Local Module
from . import mvsdk


class Camera:
    """
    A class to manage camera initialization and frame capture
    using the MvSDK camera library.
    """

    def __init__(self, camera_serial_number, 
                 camera_config,
                 gui_image_label,
                 gui_image_write_path):
        """
        Initialize the Camera class.

        Args:
            camera_serial_number (str): Serial number of the camera.
            camera_config (str): Path to camera configuration file.
            gui_image_write_path (str): Path to save base64 image JSON.
        """
        self.camera_serial_number = camera_serial_number
        self.camera_config = camera_config
        self.gui_image_label = gui_image_label
        self.gui_image_write_path = gui_image_write_path

    def initialize_camera(self):
        """
        Initializes the camera with the specified serial number.

        Returns:
            tuple: (hCamera, pFrameBuffer) if successful,
                   (None, None) otherwise.
        """
        mvsdk.CameraSetSysOption("ReconnTimeLimit", "disable")

        dev_list = mvsdk.CameraEnumerateDevice()
        if not dev_list:
            logging.error("No camera found!")
            return None, None

        selected_cam_index = -1

        # Search for camera by serial number
        for i, dev_info in enumerate(dev_list):
            logging.info(
                f"{i}: {dev_info.GetFriendlyName()} {dev_info.GetPortType()}"
            )
            if self.camera_serial_number == dev_info.GetSn():
                selected_cam_index = i

        if selected_cam_index == -1:
            logging.error("Desired camera not found! exiting program.program exiting")
            sys.exit(1)
            return None, None

        dev_info = dev_list[selected_cam_index]
        logging.info(dev_info)

        try:
            h_camera = mvsdk.CameraInit(dev_info, -1, -1)
            mvsdk.CameraReadParameterFromFile(h_camera, self.camera_config)
        except mvsdk.CameraException as e:
            logging.error(f"CameraInit Failed({e.error_code}): {e.message}")
            sys.exit(1)
            return None, None

        # Determine camera capabilities and output format
        cap = mvsdk.CameraGetCapability(h_camera)
        mono_camera = (cap.sIspCapacity.bMonoSensor != 0)

        out_format = (
            mvsdk.CAMERA_MEDIA_TYPE_MONO8
            if mono_camera else mvsdk.CAMERA_MEDIA_TYPE_BGR8
        )

        mvsdk.CameraSetIspOutFormat(h_camera, out_format)
        mvsdk.CameraSetAeState(h_camera, 0)
        mvsdk.CameraPlay(h_camera)

        frame_buffer_size = (
            cap.sResolutionRange.iWidthMax *
            cap.sResolutionRange.iHeightMax *
            (1 if mono_camera else 3)
        )

        p_frame_buffer = mvsdk.CameraAlignMalloc(frame_buffer_size, 16)
        return h_camera, p_frame_buffer

    def capture_frame(self, h_camera, p_frame_buffer):
        """
        Captures a single frame and optionally writes it
        as base64 into a JSON file.

        Args:
            h_camera: Camera handle.
            p_frame_buffer: Pointer to frame buffer.

        Returns:
            np.ndarray: Captured image frame or None if failed.
        """
        try:
            p_raw_data, frame_head = mvsdk.CameraGetImageBuffer(h_camera, 200)
            mvsdk.CameraImageProcess(
                h_camera, p_raw_data, p_frame_buffer, frame_head
            )
            mvsdk.CameraReleaseImageBuffer(h_camera, p_raw_data)

            if platform.system() == "Windows":
                mvsdk.CameraFlipFrameBuffer(p_frame_buffer, frame_head, 1)

            frame_data = (
                mvsdk.c_ubyte * frame_head.uBytes
            ).from_address(p_frame_buffer)

            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape((
                frame_head.iHeight,
                frame_head.iWidth,
                1 if frame_head.uiMediaType ==
                mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3
            ))

            # Resize and encode frame to JPEG
            resized = cv2.resize(frame, (640, 480))
            ret, buffer = cv2.imencode('.jpg', resized)

            if ret:
                encoded_string = base64.b64encode(buffer).decode('utf-8')
                config = {}
                if os.path.exists(self.gui_image_write_path):
                    try:
                        with open(self.gui_image_write_path, 'r') as jf:
                            config = json.load(jf)
                    except json.JSONDecodeError:
                        pass
                config.setdefault("cameraImage", {})[self.gui_image_label] = encoded_string

                with open(self.gui_image_write_path, 'w') as jf:
                    json.dump(config, jf, indent=4)
            else:
                logging.error("Failed to encode frame to JPEG format")

            return frame

        except mvsdk.CameraException:
            return None
