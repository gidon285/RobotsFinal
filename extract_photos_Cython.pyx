import cv2 as cv2

cpdef getFrame(sec, cam, count): 
    cam.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
    hasFrames,image = cam.read() 
    if hasFrames: 
        image = cv2.resize(image, (640, 480))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        name = './data/frame' + str(count) + '.jpg'
        cv2.imwrite(name, image)     # save frame as JPG file 
    return hasFrames 