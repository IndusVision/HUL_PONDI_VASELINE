# Standard Library
import base64
from datetime import datetime

# Third-Party Libraries
import requests
import cv2  

class Dashboard:
    """
    Handles communication with the dashboard API to send
    defective images.
    """

    def __init__(self, url, defect_id):
        """
        Initialize the Dashboard instance.

        Args:
            url (str): API endpoint to send image data.
            defect_id (int): Id for the defect type.
        """
        self.url = url
        self.defect_id = defect_id

    def send_image(self, image_path):
        """
        Reads and encodes the image as base64 and sends it along with
        metadata to the dashboard API.

        Args:
            image_path (str): Path to the image file.

        Returns:
            None
        """
        try:
            # Read the image file in binary mode
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            # Encode the image in base64 format
            image_b64 = base64.b64encode(image_data).decode()

            # Get the current timestamp in ISO format
            recorded_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            # Construct the request payload
            payload = {
                "base64_image": image_b64,
                "machines_id": 31,
                "department_id": 22,
                "product_id": 37,
                "defects_id": self.defect_id,
                "plant_id": 10,
                "recorded_date_time": recorded_date_time,
                "rca": None,
                "ocr": None
            }

            # Send the POST request
            response = requests.post(self.url, json=payload)

            # Handle response status
            if response.status_code in (200, 201):
                print("Image sent successfully.")
            else:
                print(
                    "Failed to send image. "
                    f"Status code: {response.status_code}"
                )

        except Exception as e:
            print(f"Error sending image: {str(e)}")
