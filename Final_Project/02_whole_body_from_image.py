# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
from imutils import translate, rotate, resize

import time
import numpy as np
np.random.seed(1337)

sys.path.append(dir_path + '/../../python/openpose/Release');
os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
import pyopenpose as op


    
import keras
# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"

print("OpenPose start")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

tposer = keras.models.load_model('dab-tpose-other.h5')

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Process Image
datum = op.Datum()

np.set_printoptions(precision=4)

fps_time = 0

DAB = 1
TPOSE = 2
OTHER = 0

bounced = time.time()
debounce = 3 # wait 3 seconds before allowing another command


while cap.isOpened():
    ret_val, frame = cap.read()

    datum.cvInputData = frame
    opWrapper.emplaceAndPop([datum])

    # need to be able to see what's going on
    image = datum.cvOutputData
    cv2.putText(image,
               "FPS: %f" % (1.0 / (time.time() - fps_time)),
                (10, 20),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 2)
    
    cv2.imshow("Openpose", image)

    if datum.poseKeypoints.any():
        first_input = datum.poseKeypoints
        try:
            first_input[:,:,0] = first_input[:,:,0] / 720
            first_input[:,:,1] = first_input[:,:,1] / 1280
            first_input = first_input[:,:,1:]
            first_input = first_input.reshape(len(datum.poseKeypoints), 50)
        except:
            continue

        output = tposer.predict_classes(first_input)
        for j in output:
            if j == 1:
                if (time.time() - bounced) < debounce:
                    continue
                print("dab detected")
                bounced = time.time()
            elif j == 2:
                if (time.time() - bounced) < debounce:
                    continue                   
                print("tpose detected")
                bounced = time.time()
                
    fps_time = time.time()
    
    # quit with a q keypress, b or m to save data
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# clean up after yourself
cap.release()
cv2.destroyAllWindows()  
except Exception as e:
    print(e)
    sys.exit(-1)
