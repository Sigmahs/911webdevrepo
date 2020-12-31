import numpy as np
import cv2
from modules.combine import deep_convert
from modules.webimg import url_to_image
import json
import requests

# Convert a single image
def convert_single_img(input_img):
    try:
        temp_outs = deep_convert(input_img, pic_id = 0, return_rectangle = True, save_img=False)

        for temp_out in temp_outs[1]:
            width = temp_out[1] - temp_out[0]
            height = temp_out[3] - temp_out[2]
            temp_out[0] += round(width * 0.12)
            temp_out[1] -= round(width * 0.12)
            temp_out[2] += round(height * 0.12)
            temp_out[3] -= round(height * 0.12)

    except:
        print("fail to find the front face")

    return temp_outs

# Image_displayed
def image_shown(img_url, repeat):
    """
    CV2 package use BGR, matplotlib use RGB
    """
    try:
        temp_out = convert_single_img(img_url)
    except:
        None
    green = (0, 255, 0)
    #img = url_to_image(img_url)
    img = np.asarray(bytearray(img_url))
    img = cv2.imdecode(img,cv2.IMREAD_COLOR)
    height, width, channels = img.shape
    face_num = 0
    for temp in temp_out[1]:
        left, right, up, down = temp[0:4]
        linethick = round(min(height/200,width/200))
        cv2.rectangle(img, (left, up), (right, down), green, thickness=linethick)
        face_num += 1
#        cv2.putText(img, "Person" + str(face_num), (left, up - 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, "Person" + str(face_num), (left, up - 4*linethick),
                cv2.FONT_HERSHEY_SIMPLEX, linethick/4, (0, 255, 0), 2)
        #    cv2.imwrite("images/outputimage"+str(repeat)+".jpg", img)
    return img


def image_shown_tracker(img_url, repeat):
    """
    CV2 package use BGR, matplotlib use RGB
    """
    try:
        temp_out = convert_single_img(img_url)
    except:
        None
    green = (0, 255, 0)
    #img = url_to_image(img_url)
    img = np.asarray(bytearray(img_url))
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    height, width, channels = img.shape
    face_num = 0
    for temp in temp_out[1]:
        left, right, up, down = temp[0:4]
        linethick = round(min(height/200,width/200))
        cv2.rectangle(img, (left, up), (right, down), green, thickness=linethick)
        face_num += 1
#        cv2.putText(img, "Person" + str(face_num), (left, up - 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, "Person" + str(face_num), (left, up - 4*linethick),
                cv2.FONT_HERSHEY_SIMPLEX, linethick/4, (0, 255, 0), 2)
        #    cv2.imwrite("images/outputimage"+str(repeat)+".jpg", img)
    
    return left, up, (right - left), (down - up)



def video_analyzer(img_url, repeat, major_value):
    """
    CV2 package use BGR, matplotlib use RGB
    """
    
    temp_out = convert_single_img(img_url)
    
    green = (0, 255, 0)
    #img = url_to_image(img_url)
    img = np.asarray(bytearray(img_url))
    img = cv2.imdecode(img,cv2.IMREAD_COLOR)
    height, width, channels = img.shape

    if repeat == 0:

        faces = []
        test_img_data = temp_out[0] #remove one [0] and should replace by a for loop
        all_data = []
        for i in test_img_data:
                faces.append(i.reshape(200,200))
        for each_face in faces:
            push_data = []
            each_face = each_face/255
            for i in each_face:
                row = []
                for j in i:
                    row.append([j])
                push_data.append(row)
            all_data.append(push_data)

        posted={}
        labels = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        for i in range(0, len(all_data)):
            # convert data into json
            data = {"instances":[all_data[i]]}
            push_data_json = json.dumps(data, sort_keys=True, separators=(',', ': '))
            r1 = requests.post("http://35.224.178.33:8501/v1/models/model1:predict", data=push_data_json)
            prediction_1 = json.loads(r1.text)['predictions'][0]
            ensemble_prob = prediction_1  
            
            """locals()['res' + str(i)] = dict([[x,  "{:4.4f}".format(y)] for x, y in zip(labels, ensemble_prob)])
            posted['res' + str(i)] = locals()['res' + str(i)]"""
        pos = ensemble_prob.index(max(ensemble_prob))
        major_value = labels[pos] +":  " +str(max(ensemble_prob))
        print(major_value)
    


    
    face_num=0
    for temp in temp_out[1]:
        left, right, up, down = temp[0:4]
        linethick = round(min(height/200,width/200))
        cv2.rectangle(img, (left, up), (right, down), green, thickness=linethick)
        face_num += 1
#        cv2.putText(img, "Person" + str(face_num), (left, up - 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, "Person" + str(face_num), (left, up - 4*linethick),
                cv2.FONT_HERSHEY_SIMPLEX, linethick/4, (0, 255, 0), 2)
        cv2.putText(img, major_value, (0,100),cv2.FONT_HERSHEY_SIMPLEX,linethick/4, (0, 255, 0), 2)
        #    cv2.imwrite("images/outputimage"+str(repeat)+".jpg", img)
    return img, major_value
