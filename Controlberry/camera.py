import logging
from io import BytesIO
from time import sleep
from picamera import PiCamera
from picamera.exc import PiCameraMMALError, PiCameraError


logging.basicConfig(level=logging.INFO,  format = '%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def get_image_as_bytes():
    '''
    returns image as bytes from Pi Camera
    '''
    stream = BytesIO()
    try:
        camera = PiCamera()
        camera.start_preview()
        sleep(1.3)
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        camera.close()
        return stream.getvalue()
    except (PiCameraMMALError, PiCameraError):
        logger.error('Enable Camera in raspi-cnfig or check if camera is connected')
        pass
