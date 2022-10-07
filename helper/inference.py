from argparse import ArgumentParser

import cv2
from cv2 import imread, IMREAD_GRAYSCALE
import numpy as np
# from PIL import Image
import tensorflow as tf


def inferencing(input_path, output_path, threshold):
    model_path = "../model/v1.1.tflite"

    h, w = 80, 80
    min, max = 0, 255
    norm_min, norm_max = 0, 1
    norm = max/2

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # img = Image.open(input_path).convert('l')  # .resize((80,80))
    img_arr = imread(input_path, IMREAD_GRAYSCALE)
    # img_arr = np.array(img)
    input_data = img_arr.reshape(1, img_arr.shape[0], img_arr.shape[1], 1)

    ## uint8 to float32 + normalize(-1 to 1)
    if input_data.dtype != 'float32':
        input_data = (np.float32(input_data)-norm)/norm  # norm -1 to 1
        # input_data = np.float32(input_data)/max # norm 0 to 1

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    # function `get_tensor()` returns copy of tensor data. Use `tensor()`  to get pointer to tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])  # accuacy
    output_data1 = interpreter.get_tensor(output_details[1]['index'])  # location
    output_data2 = interpreter.get_tensor(output_details[2]['index'])  # detection cnt

    ## change output from float32 to uint8
    output_data4 = output_data1*79
    output_data4 = np.around(output_data4, decimals=0).astype(int).tolist()
    output_data4 = output_data4[0]

    # print(f"ACCURACY: {output_data}")
    # print(f"LOCATION_F: {output_data1}")
    # print(f"COUNT: {output_data2}")
    # print(f"CLASS: {output_data3}")
    # print(f"LOCATION_8: {output_data4}")
    flag = 0
    output = []
    for outs in output_data:
        for i, out in enumerate(outs):
            if out > threshold:
                for corner in output_data4[i]:
                    if corner < 0 or corner > h:
                        flag = 1
                        break
                if flag == 0: output.append(output_data4[i])
                flag = 0

    with open(output_path, 'w') as w:
        w.write(str(len(output)))
        for i in output:
            w.write(f',{i[1]}x{i[0]}x{i[3]}x{i[2]}')

    window_name = "out"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    for i in output:
        image = cv2.rectangle(image, (i[1], i[0]), (i[3], i[2]), (255, 0, 0), 1)
    cv2.imshow(window_name, image)
    key = cv2.waitKey()
    if key == 27:
        cv2.destroyAllWindows()

input_path = f"../data/000.png"
output_path = f"data/000.txt"
threshold = 0.5
inferencing(input_path, output_path, threshold)

