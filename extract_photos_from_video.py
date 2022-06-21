from typing import List
import cv2
from pyodm import Node, exceptions
import os
import sys
import extract_photos_Cython as cython
# run with: docker run -ti -p 3000:3000 opendronemap/nodeodm
# pip install openCV-python 
sys.path.append('..')

def produce_images_from_video(frameRate:float, count:int, cam,images_dir_path:str=None):
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')

    sec = 0
    success = cython.getFrame(sec, cam, count,images_dir_path) 
    while success: 
        count += 1
        sec = sec + frameRate 
        sec = round(sec, 2) 
        success = cython.getFrame(sec, cam, count,images_dir_path) 

    cam.release()
    cv2.destroyAllWindows()
    return count

def create_point_clouds(photo_amount,photos_per_cloud:int=50,overlap:int=20):
    ### type check
    photos_per_cloud=int(photos_per_cloud)
    overlap=int(overlap)
    if (photos_per_cloud<=0) :
        raise "numbers of photos must be positive"
    if (overlap>=photos_per_cloud):
        raise "number of overlap photos must be smaller than numbers of photos per cloud"
    if(photo_amount<photos_per_cloud):
        photos_per_cloud=photo_amount
        overlap=0
    counter=0
    list_img = []
    img_to_remove=photos_per_cloud-overlap

    node = Node("localhost", 3000)

    is_last_round=False
    while (not is_last_round):
        #add new images, while keeping overlap images
        for index in range(counter, photos_per_cloud):
            if (counter==photo_amount):#
                is_last_round=True
                break
            list_img.append("data/frame"+str(index)+".jpg")
            counter+=1
        create_point_cloud_from_range(list_img,node)
        #remove first images
        for index in range(0, img_to_remove):
            list_img.pop()

      

    

def create_point_cloud_from_range(list_img,node):

    try:
        # Start a task
        print("Uploading images...")
        task = node.create_task(list_img,
                                {'feature-quality':'medium','gps-accuracy': 1,'matcher-neighbors':1,'mesh-octree-depth':8,'pc-las':True,'pc-quality':'low','end-with':'mvs_texturing' })
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
    address = os.path.dirname(os.path.realpath(__file__)) +"\\video.mp4"
    cam = cv2.VideoCapture(address)
    
    # calculations
    fps = cam.get(cv2.CAP_PROP_FPS)
    frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    duration, chunk = frame_count/fps, 25
    myframerate = duration / (duration * chunk)

    photo_amount=produce_images_from_video(0.5, 0, cam)
    print("photo_amount: "+str(photo_amount))
    create_point_clouds(photo_amount)
