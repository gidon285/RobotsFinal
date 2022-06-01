import cv2
import os
  
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

if __name__ == "__main__":
    address = dir_path = os.path.dirname(os.path.realpath(__file__)) +"\\video.mp4"
    frameRate=  0.25
    get_images_from_vedio(address, frameRate)