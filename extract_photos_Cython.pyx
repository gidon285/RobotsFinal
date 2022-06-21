import cv2 as cv2

cpdef getFrame(sec, cam, count,images_dir):
    if images_dir==None:
        images_dir='./data'
    cam.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
    hasFrames,image = cam.read() 
    if hasFrames: 
        name = images_dir+'/frame' + str(count) + '.jpg'
        cv2.imwrite(name, image)     # save frame as JPG file 
    return hasFrames 