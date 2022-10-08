import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import math_ops
from tensorflow.python.keras import backend as K


#自定义损失
def ReprojectionLoss(y_true, y_pred):
    y_pred = ops.convert_to_tensor_v2(y_pred)
    y_true = math_ops.cast(y_true, y_pred.dtype)
    y_pred = K.reshape(y_pred,(-1,27,2))
    y_true = K.reshape(y_true, (-1, 27, 2))
    return K.sqrt(K.mean(K.sum(math_ops.squared_difference(y_pred, y_true),axis=-1),axis=-1))

def ReprojectionMetrics(y_true,y_pred):

    return ReprojectionLoss(y_true, y_pred)

if __name__ == "__main__":
    # 将h5模型转化为tflite模型方法1
    modelparh = r'D:\github\face_classification-master\trained_models\emotion_models\fer2013_mini_XCEPTION.64-0.65.hdf5'
    model = tf.keras.models.load_model(modelparh, custom_objects = {'ReprojectionLoss': ReprojectionLoss, 'ReprojectionMetrics': ReprojectionMetrics})

    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    tflite_model = converter.convert()
    savepath = r'D:\github\face_classification-master\trained_models\emotion_models\model.tflite'
    open(savepath, "wb").write(tflite_model)
