from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("extract_photos_Cython.pyx")
)


# To compile, run the following command:
#      python setup.py build_ext --inplace

#### original version:  ####
# cpdef getFrame(sec, cam, count): 
#     cam.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
#     hasFrames,image = cam.read() 
#     if hasFrames: 
#         image = cv2.resize(image, (640, 480))
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         name = './data/frame' + str(count) + '.jpg'
#         cv2.imwrite(name, image)     # save frame as JPG file 
#     return hasFrames 
