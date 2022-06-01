import cv2
import os
from pyodm import Node, exceptions
import os
import sys

# run with: docker run -ti -p 3000:3000 opendronemap/nodeodm
 # pip install openCV-python 
sys.path.append('..')
  
def getFrame(sec, cam, count): 
    cam.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
    hasFrames,image = cam.read() 
    if hasFrames: 
        name = './data/frame' + str(count) + '.jpg'
        cv2.imwrite(name, image)     # save frame as JPG file 
    return hasFrames 

def get_images_from_vedio(address:str, frameRate:int):
    cam = cv2.VideoCapture(address)
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')

    sec ,c = 0, 0
    success = getFrame(sec, cam, c) 
    while success: 
        c += 1
        sec = sec + frameRate 
        sec = round(sec, 2) 
        success = getFrame(sec, cam, c) 
        

    cam.release()
    cv2.destroyAllWindows()





def odm():   
    tmp=os.listdir("data")
    list_img=[]
    for img_name in tmp:
        list_img.append("data/"+img_name)
    print(list_img)
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
            task.restart({'dtm': True})
            task.wait_for_completion()

            print("Task completed, downloading results...")

            task.download_assets("./results_with_dtm")

            print("Assets saved in ./results_with_dtm (%s)" % os.listdir("./results_with_dtm"))
        except exceptions.TaskFailedError as e:
            print("\n".join(task.output()))

    except exceptions.NodeConnectionError as e:
        print("Cannot connect: %s" % e)
    except exceptions.NodeResponseError as e:
        print("Error: %s" % e)

if __name__ == "__main__":
    address = dir_path = os.path.dirname(os.path.realpath(__file__)) +"\\video.mp4"
    # frameRate=  0.25
    # get_images_from_vedio(address, frameRate)
    odm()