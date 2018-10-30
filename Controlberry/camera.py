'''
short snippet 
to take photos 
to disable red light
add this line :
disable_camera_led=1

to this file

sudo nano /boot/config.txt
'''
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
    there few options how to process it
    one is to get stored image (which is stored as bytes) as string
    for example by function
    from bson.json_util import dumps
    
    def get_picture():
        picture = Pictures.find_one().get('PICTURE')
        return dumps(picture).replace('{"$binary": ','').replace("}",'').replace('"','')
    
    Returned string can be directly used for example as src for image if you add this:
    .src = "data:image/jpeg;base64," + your string
    
    In python you can get image with this short code from string:
    
    import base64
    import io
    from PIL import Image
    # to show it in Jupyter notebook
    from IPython.display import display
    # code below is important
    msg = base64.b64decode(pict)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    # to show it in jupyter notebook inline
    display(img)
    
    Directly from binary field:
    
    picture_bytes = Pictures.find().skip(40).limit(1).next().get('PICTURE')
    buf = io.BytesIO(picture_bytes)
    img = Image.open(buf)
    
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
