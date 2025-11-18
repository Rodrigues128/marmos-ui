import cv2
from pyzbar import pyzbar

class QRDecoder:
    """
    A service to decode QR codes from image frames.
    """

    def decode(self, frame):
        """
        Decodes QR codes from a given camera frame.

        Args:
            frame: The image frame (from OpenCV).

        Returns:
            A list of decoded QR code data strings. Returns an empty list if no QR code is found.
        """
        if frame is None:
            return []

        # Convert the image to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find barcodes and QR codes
        decoded_objects = pyzbar.decode(gray_frame)

        if not decoded_objects:
            return []

        # Extract data from decoded objects
        data_list = [obj.data.decode('utf-8') for obj in decoded_objects]
        
        return data_list

    def parse_wifi_qr(self, qr_data: str):
        """
        Parses a Wi-Fi QR code string.
        Format: WIFI:S:<SSID>;T:<AUTH>;P:<PASSWORD>;;

        Args:
            qr_data: The full string from the QR code.

        Returns:
            A dictionary with 'ssid' and 'password' or None if parsing fails.
        """
        if not qr_data or not qr_data.startswith("WIFI:"):
            return None

        try:
            parts = qr_data.replace("WIFI:", "").split(';')
            data = {}
            for part in parts:
                if part.startswith('S:'):
                    data['ssid'] = part[2:]
                elif part.startswith('P:'):
                    data['password'] = part[2:]
            
            if 'ssid' in data and 'password' in data:
                return data
        except Exception:
            # In case of any parsing error, return None
            return None
        
        return None
