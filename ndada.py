import cv2 as cv2
import os
from pyodm import Node, exceptions
import os
import sys
import extract_photos_Cython as cython
import multiprocessing
import threading 

# run with: docker run -ti -p 3000:3000 opendronemap/nodeconsume_images
# pip install openCV-python 

sys.path.append('..')

class elp:
    def __init__(self):
        self._count =0
    def increase(self):
        self._count += 1
    def get_counter(self):
        return self._count


def produce_images(address:str, frameRate:int, cam , count, thread_count):
    print("producer started ")
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')
    last, sec, threads = 0, 0, 0
    success = cython.getFrame(sec, cam, melp.get_counter()) 
    melp.increase()
    while success:
        if melp.get_counter() % 25 == 0:
            if threads < thread_count:
                threading.Thread(target = consume_images(last, melp.get_counter(), threads))
                threads += 1
                last = melp.get_counter()
        else:
            pass
        sec = sec + frameRate 
        sec = round(sec, 2) 
        melp.increase()
        success = cython.getFrame(sec, cam, melp.get_counter())
    cam.release()
    cv2.destroyAllWindows()


def consume_images(start:int, end:int, threads:int ):
    for index in range(start,end):
        self._list_img.append("data/frame"+str(index))
    node = Node("localhost", 3000)
    try:
        # Start a task
        print("Uploading images...")
        task = node.create_task(self._list_img, {'dsm': True, 'orthophoto-resolution': 4})
        print(task.info())
        try:
            # This will block until the task is finished
            # or will raise an exception
            task.wait_for_completion()
            print("Task completed, downloading results...")
            # Retrieve results
            task.download_assets("./results")
            print("Assets saved in ./results (%s)" % os.listdir("./results"))
            threading.current_thread().join()
            threads -= 1
        except exceptions.TaskFailedError as e:
            print("\n".join(task.output()))
    except exceptions.NodeConnectionError as e:
        print("Cannot connect: %s" % e)
    except exceptions.NodeResponseError as e:
        print("Error: %s" % e)


if __name__ == "__main__":

    # constants
    # robot = Robots(multiprocessing.cpu_count())
    address = dir_path = os.path.dirname(os.path.realpath(__file__)) +"\\video.mp4"
    cam = cv2.VideoCapture(address)
    
    # calculations
    fps = cam.get(cv2.CAP_PROP_FPS)
    frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    duration, chunk = frame_count/fps, 25
    myframerate = duration / (duration * chunk)
    
    melp = elp()
    thread_count = multiprocessing.cpu_count()
    t = threading.Thread(target=produce_images(address, myframerate, cam, melp, thread_count))
    t.start()
    # for _ in range(thread_count):
    #     temporary.append()
    # with concurrent.futures.ThreadPoolExecutor(max_workers= thread_count - 1) as executor:
    #     for index in range(5):
    #         executor.submit(database.locked_update, index)
    t.join()
