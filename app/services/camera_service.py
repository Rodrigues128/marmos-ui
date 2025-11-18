import cv2
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import BooleanProperty

from app.services.qr_decoder import QRDecoder

class CameraService(Image):
    """
    A Kivy Widget that displays a camera feed and performs QR code scanning.
    It uses OpenCV to capture video and pyzbar (via QRDecoder) to scan for codes.
    """
    is_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        self.qr_decoder = QRDecoder()
        self.event = None
        self.register_event_type('on_qr_decoded')

    def on_is_active(self, instance, value):
        """Start or stop the camera feed based on the 'is_active' property."""
        if value:
            self.start()
        else:
            self.stop()

    def start(self):
        """Initializes and starts the camera capture."""
        if self.capture is None:
            # Try to find a working camera index, starting with 0
            # On Raspberry Pi, it might be 0 or higher depending on the setup.
            for i in range(5):
                self.capture = cv2.VideoCapture(i)
                if self.capture.isOpened():
                    break
            else:
                self.capture = None
                print("CameraService: Failed to open camera.")
                return

        if self.event is None:
            # Schedule the update method to be called periodically
            self.event = Clock.schedule_interval(self.update, 1.0 / 30.0) # 30 FPS

    def stop(self):
        """Stops the camera capture and releases resources."""
        if self.event:
            self.event.cancel()
            self.event = None
        
        if self.capture:
            self.capture.release()
            self.capture = None
        
        # Clear the image
        self.texture = None

    def update(self, dt):
        """
        Called by the Clock to update the camera texture and scan for QR codes.
        """
        if not self.capture:
            return

        ret, frame = self.capture.read()
        if ret:
            # Scan for QR codes in the frame
            decoded_data = self.qr_decoder.decode(frame)
            if decoded_data:
                # Dispatch the event with the first decoded data
                self.dispatch('on_qr_decoded', decoded_data[0])

            # Convert the frame to a Kivy texture
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

    def on_qr_decoded(self, *args):
        """Default event handler for when a QR code is decoded."""
        pass
