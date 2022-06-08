import cv2
from pyodm import Node, exceptions
import os
import sys
import extract_photos_Cython as cython
# run with: docker run -ti -p 3000:3000 opendronemap/nodeodm
# pip install openCV-python 
sys.path.append('..')

def produce_images(address:str, frameRate:float, count:int, cam):
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')

    sec = 0
    success = cython.getFrame(sec, cam, count) 
    while success: 
        count += 1
        sec = sec + frameRate 
        sec = round(sec, 2) 
        success = cython.getFrame(sec, cam, count) 

    cam.release()
    cv2.destroyAllWindows()

def consume_images(start:int , end:int):
    list_img = []
    for index in range(start, end):
        list_img.append("data/frame"+str(index)+".jpg")
    node = Node("localhost", 3000)
    try:
        # Start a task
        print("Uploading images...")
        task = node.create_task(list_img,
                                {'dsm': True, 'orthophoto-resolution': 4})
        print(task.info())
        try:
            # This will block until the task is finished
            # or will raise an exception
            task.wait_for_completion()
            print("Task completed, downloading results...")
            # Retrieve results
            task.download_assets("./results")
            print("Assets saved in ./results (%s)" % os.listdir("./results"))
            # Restart task and this time compute dtm

            """second time - possibly not necessary"""
            # task.restart({'dtm': True})
            # task.wait_for_completion()
            # print("Task completed, downloading results...")
            # task.download_assets("./results_with_dtm")
            # print("Assets saved in ./results_with_dtm (%s)" % os.listdir("./results_with_dtm"))
        except exceptions.TaskFailedError as e:
            print("\n".join(task.output()))
    except exceptions.NodeConnectionError as e:
        print("Cannot connect: %s" % e)
    except exceptions.NodeResponseError as e:
        print("Error: %s" % e)

if __name__ == "__main__":

    # constants
    address = dir_path = os.path.dirname(os.path.realpath(__file__)) +"\\video.mp4"
    cam = cv2.VideoCapture(address)
    
    # calculations
    fps = cam.get(cv2.CAP_PROP_FPS)
    frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    duration, chunk = frame_count/fps, 25
    myframerate = duration / (duration * chunk)

    produce_images(address, 0.5, 0, cam)
    consume_images(0,12)