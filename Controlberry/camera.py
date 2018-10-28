from io import BytesIO
from time import sleep
from picamera import PiCamera

camera_running = {}

def get_image_as_bytes():
'''
returns image as bytes from Pi Camera
'''
  stream = BytesIO()
  if not camera_running.get('camera'):
    camera = PiCamera()
    running['camera'] = camera
    camera.start_preview()
    sleep(2)
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    return stream.getvalue()  
  if camera_running.get('camera'):
    running.get('camera').capture(stream, format='jpeg')
    stream.seek(0)
    return stream.getvalue() 
    

def close_camera():
  '''
  if camera is running it will close the camera
  '''
  if camera_running.get('camera'):
    camera_running.get('camera').close()
    del camera_running['camera']
