# import numpy as np
# import tensorflow as tf

# def draw_rect(image, box):
#     y_min = int(max(1, (box[0] * image.height)))
#     x_min = int(max(1, (box[1] * image.width)))
#     y_max = int(min(image.height, (box[2] * image.height)))
#     x_max = int(min(image.width, (box[3] * image.width)))
    
#     # draw a rectangle on the image
#     cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 255, 255), 2)

# def read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255):
#     file_reader = tf.read_file(file_name, "file_reader")
    
#     if file_name.endswith(".png"):
#         image_reader = tf.image.decode_png(file_reader, channels=3, name="png_reader")
#     elif file_name.endswith(".gif"):
#         image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name="gif_reader"))
#     elif file_name.endswith(".bmp"):
#         image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
#     else:
#         image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
    
#     float_caster = tf.cast(image_reader, tf.float32)
#     dims_expander = tf.expand_dims(float_caster, 0)
#     resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
#     normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
#     sess = tf.Session()
#     result = sess.run(normalized)

#     return result

# file_name = "data/dog.jpg"
# input_height = 224
# input_width = 320
# image_tensor = read_tensor_from_image_file(file_name, input_height, input_width)

# # Load TFLite model and allocate tensors.
# interpreter = tf.lite.Interpreter(model_path="mobile_yolo.tflite")
# interpreter.allocate_tensors()

# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()

# print(output_details)
# # Test model
# input_shape = input_details[0]['shape']
# interpreter.set_tensor(input_details[0]['index'], image_tensor)

# interpreter.invoke()
# # print(output_data)

# rects = interpreter.get_tensor(
#     output_details[0]['index'])

# scores = interpreter.get_tensor(
#     output_details[1]['index'])

# for index, score in enumerate(scores[0]):
#    # if score > 0.5:
#         draw_rect(new_img,rects[0][index])
        
# cv2.imshow("image", new_img)
# cv2.waitKey(0)

# # for file in pathlib.Path('data').iterdir():

# #     if file.suffix != '.jpg' and file.suffix != '.png':
# #         continue
    
# #     img = cv2.imread(r"{}".format(file.resolve()))
# #     new_img = cv2.resize(img, (320, 224))
# #     interpreter.set_tensor(input_details[0]['index'], [new_img])

# #     interpreter.invoke()
# #     rects = interpreter.get_tensor(
# #         output_details[0]['index'])

# #     scores = interpreter.get_tensor(
# #         output_details[2]['index
    
# #     for index, score in enumerate(scores[0]):
# #         if score > 0.5:
# #           draw_rect(new_img,rects[0][index])
          
# #     cv2.imshow("image", new_img)
# #     cv2.waitKey(0)

import tensorflow as tf
import numpy as np
import cv2
import pathlib

interpreter = tf.contrib.lite.Interpreter(model_path="object_detection.tflite")

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)
print(output_details)

interpreter.allocate_tensors()

for file in pathlib.Path('images').iterdir():

    img = cv2.imread(r"{}".format(file.resolve()))
    new_img = cv2.resize(img, (512, 512))

    interpreter.set_tensor(input_details[0]['index'], [new_img])

    interpreter.invoke()
    rects = interpreter.get_tensor(
        output_details[0]['index'])
    scores = interpreter.get_tensor(
        output_details[2]['index'])
    
    for index, score in enumerate(scores[0]):
        if score > 0.5:
            print("For file {}".format(file.stem))
            print("Rectangles are: {}".format(rects[index]))