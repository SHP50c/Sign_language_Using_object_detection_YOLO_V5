import os
import cv2
import time
import uuid

IMAGE_PATH = "CollectedImages"

labels = ['Hello','Yes','No','Thanks','I love You','Please','Namaste']

number_of_images = 500

for label in labels:
    img_path = os.path.join(IMAGE_PATH,label)
    os.makedirs(img_path,exist_ok=True)

    #open camera
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    print(f"Collecting images for {label}")
    time.sleep(5)

    for imgnum in range(number_of_images):
        print(imgnum)
        ret,frame = cap.read()
        cv2.imshow('frame',frame)
        imagename=os.path.join(IMAGE_PATH,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imagename,frame)
        time.sleep(3)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

    cap.release()