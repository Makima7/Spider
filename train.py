from net import LeNet
import sys
import os
import cv2
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt
from imutils import paths
from keras.utils import to_categorical
from keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
import matplotlib
from sklearn import preprocessing
matplotlib.use("Agg")

# import the necessary packages
sys.path.append('..') 

EPOCHS = 40
INIT_LR = 1e-3
BS = 32
CLASS_NUM = 33
norm_size = 350

# 路径保存
train_dataset_path="./train"
test_dataset_path="./test"
model_path="./model"
plot_path="./plot"

# def args_parse():
#     ap = argparse.ArgumentParser()
#     ap.add_argument("-dtest", "--dataset_test", default="./train",
#                     help="path to input dataset_test")
#     ap.add_argument("-dtrain", "--dataset_train", default="./test",
#                     help="path to input dataset_train")
#     ap.add_argument("-m", "--model", default="./",
#                     help="path to output model")
#     ap.add_argument("-p", "--plot", type=str, default="plot.png",
#                     help="path to output accuracy/loss plot")
#     args = vars(ap.parse_args())
#     return args


def load__data(path):
    print("loading images........")
    data = []
    labels = []
    imagePaths = sorted(list(paths.list_images(path)))
    random.seed(42)
    random.shuffle(imagePaths)

    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)
        label = imagePath.split(os.sep)[-2]
        labels.append(label)

    data = np.array(data, dtype="float")/255.0
    le=preprocessing.LabelEncoder()
    le=le.fit(os.listdir("./train"))
    labels=le.transform(labels)
    labels = to_categorical(labels, num_classes=CLASS_NUM)
    return data,labels

def train(aug, trainX, trainY, testX, testY):
    print("compileing model\n---------------------")
    model = LeNet.build(width=norm_size, height=norm_size,
                        depth=3, classes=CLASS_NUM)

    opt = Adam(lr=INIT_LR, decay=INIT_LR/EPOCHS)
    model.compile(loss="categorical_crossentropy",
                    optimizer=opt, metrics=["accuracy"])

    print("training network\n----------------------")
    H = model.fit(aug.flow(trainX, trainY, batch_size=BS), validation_data=(
        testX, testY), steps_per_epoch=len(trainX)//BS, epochs=EPOCHS, verbose=1)

    print("serializing network\n---------------------")
    model.save("./steam.model")

    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["accuracy"], label="acc")
    plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy on traffic-sign classifier")
    plt.xlabel("EPOCH")
    plt.ylabel("LOSS / ACCURACY")
    plt.legend(loc="lower left")
    plt.savefig("./plot/learn.png")






if __name__ == "__main__":
    #args = args_parse()
    train_file_path = "./train"
    test_file_path = "./test"
    trainX, trainY = load__data(train_file_path)
    testX, testY = load__data(test_file_path)

    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1, height_shift_range=0.1,
                             shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")
    
    train(aug,trainX,trainY,testX,testY)
    print('resloved')
