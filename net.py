from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.convolutional import AveragePooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.models import Model
from keras.layers import Input
from keras.layers import concatenate
from keras import backend as K

# 定义网络结构


# LeNet
class LeNet:
    @staticmethod
    def build(width, height, depth, classes):
        model = Sequential()
        inputShape = (height, width, depth)
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
        model.add(Conv2D(20, (5, 5), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Flatten())
        # softmax
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        return model

# GoogleNet


class GoogleNet:
    @staticmethod
    def conv_module(x, K, kX, kY, stride, chanDim, padding="same"):
        x = Conv2D(K, (kX, kY), strides=stride, padding=padding)(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = Activation("relu")(x)
        return x

    @staticmethod
    def inception_module(x, numK1_1, numK3_3, chanDim):
        conv1_1 = GoogleNet.conv_module(x, numK1_1, 1, 1, (1, 1), chanDim)
        conv3_3 = GoogleNet.conv_module(x, numK3_3, 3, 3, (1, 1), chanDim)
        x = concatenate([conv1_1, conv3_3], axis=chanDim)
        return x

    @staticmethod
    def downsample_module(x, K, chanDim):
        conv3_3 = GoogleNet.conv_module(
            x, K, 3, 3, (2, 2), chanDim, padding='valid')
        pool = MaxPooling2D((3, 3), strides=(2, 2))(x)
        x = concatenate([conv3_3, pool], axis=chanDim)
        return x

    @staticmethod
    def build(width, height, depth, classes):
        inputShape = (height, width, depth)
        chanDim = -1
        if K.image_data_format()=="channels_first":
            inputShape=(depth,width,depth)
            chanDim=-1
        
        inputs=Input(shape=inputShape)

        x=GoogleNet.conv_module(inputs,96,3,3,(1,1),chanDim)

        x=GoogleNet.inception_module(x,32,32,chanDim)
        x=GoogleNet.inception_module(x,32,48,chanDim)
        x=GoogleNet.downsample_module(x,80,chanDim)

        x=GoogleNet.inception_module(x,112,48,chanDim)
        x=GoogleNet.inception_module(x,96,64,chanDim)
        x=GoogleNet.inception_module(x,80,80,chanDim)
        x=GoogleNet.inception_module(x,48,96,chanDim)
        x=GoogleNet.downsample_module(x,96,chanDim)

        x=GoogleNet.inception_module(x,176,160,chanDim)
        x=GoogleNet.inception_module(x,176,160,chanDim)
        x=AveragePooling2D((7,7))(x)
        x=Dropout(0.5)(x)

        x=Flatten()(x)
        x=Dense(classes)(x)
        x=Activation("softmax")(x)

        model=Model(inputs,x,name="googlenet")

        
        return model
