import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer

# Define the custom L1Dist layer
class L1Dist(Layer):
    def __init__(self, **kwargs):
        super(L1Dist, self).__init__(**kwargs)

    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)
    

SIZE = 200
def preprocess(file_path):

    byte_img = tf.io.read_file(file_path)
    img = tf.io.decode_jpeg(byte_img)

    img = tf.image.resize(img, (SIZE,SIZE))
    img = img / 255.0

    return img

input_path = 'database/input_img'
validation_path = 'database/dataset'

def verify(model,img_name, detection_threshold):
    results = {}
    for image in os.listdir(os.path.join(validation_path)):
        input_img = preprocess(os.path.join(input_path, img_name))
        validation_img = preprocess(os.path.join(validation_path, image))
        tree_name = os.path.splitext(os.path.basename(image))[0]
        result = model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
        if result > detection_threshold:
            results[tree_name] = result

    # print(results)


    if len(results)==1:
      end_result = f"This tree is {list(results.keys())[0]}"
    elif len(results)>1:
      end_result = f"This tree is {max(results, key=results.get)}"
    else:
      end_result = "This tree is not in the database"


    return end_result

# def verify(model, img_name, detection_threshold, verification_threshold):
#     results = []
#     for image in os.listdir(os.path.join('database/verification')):
#         input_img = preprocess(os.path.join('database/input/', img_name))
#         validation_img = preprocess(os.path.join('database/verification', image))
#         print(image)

#         result = model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
#         results.append(result)

#     detection = np.sum(np.array(results) > detection_threshold)

#     verification = detection / len(os.listdir(os.path.join('database/verification')))
#     verified = verification > verification_threshold

#     return results, verified

# verified1 = verify(loaded_model,'input_clay.jpg', 0.5)
# verified2 = verify(loaded_model,'input_pine3.jpg', 0.5)
# verified3 = verify(loaded_model,'input_pine4.jpg', 0.5)
# verified4 = verify(loaded_model,'input_pine2.jpg', 0.5)
# print(verified1,'\n',verified2,'\n',verified3,'\n',verified4)
