from net import LeNet, GoogleNet, Inceptionv3
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

EPOCHS = 200
INIT_LR = 0.0001
BS = 16
CLASS_NUM = 33
norm_size = 128

# 路径保存
train_dataset_path = "./train"
test_dataset_path = "./test"
model_path = "./model"
plot_path = "./plot"

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

# 读取图片，转化为数据集、打标签


def load__data(path):
    print("loading images........")
    data = []
    labels = []
    imagePaths = sorted(list(paths.list_images(path)))
    # 对数据集随机排序
    random.seed(42)
    random.shuffle(imagePaths)

    # 处理数据集 打标签
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)
        label = imagePath.split(os.sep)[-2]
        labels.append(label)

    # 对汉字标签编码
    data = np.array(data, dtype="float")/255.0
    le = preprocessing.LabelEncoder()
    le = le.fit(os.listdir("./train"))
    labels = le.transform(labels)
    labels = to_categorical(labels, num_classes=CLASS_NUM)
    return data, labels

# 训练模型


def train(aug, trainX, trainY, testX, testY):
    # 创建模型
    print("compileing model\n---------------------")

    # 使用LeNet
    # model = LeNet.build(width=norm_size, height=norm_size,
    #                      depth=3, classes=CLASS_NUM)

    # 使用一个小型的googleNet
    # model = GoogleNet.build(
    #    width=norm_size, height=norm_size, depth=3, classes=CLASS_NUM)

    # 使用keras内置的inceptionv3
    model = Inceptionv3.build(
        width=norm_size, height=norm_size, depth=3, classes=CLASS_NUM)

    # 使用adam优化学习率
    opt = Adam(lr=INIT_LR, decay=INIT_LR/EPOCHS)

    # 使用adadelta优化学习率
    # from keras.optimizers import Adadelta
    # opt = Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=INIT_LR/EPOCHS)

    # 添加损失函数
    model.compile(loss="categorical_crossentropy",
                  optimizer=opt, metrics=["accuracy"])

    # 训练模型
    print("training network\n----------------------")
    H = model.fit(aug.flow(trainX, trainY, batch_size=BS), validation_data=(
        testX, testY), steps_per_epoch=len(trainX)//BS, epochs=EPOCHS, verbose=1)

    print("serializing network\n---------------------")
    model.save("./steam.model")

    # 输出损失函数图
    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.title("Training Loss plot")
    plt.xlabel("EPOCH")
    plt.ylabel("LOSS")
    plt.legend(loc="lower left")
    plt.savefig("./plot/loss.png")

    # 输出ACC图
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, N), H.history["accuracy"], label="acc")
    plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Accuracy plot")
    plt.xlabel("EPOCH")
    plt.ylabel("ACCURACY")
    plt.legend(loc="lower left")
    plt.savefig("./plot/acc.png")


if __name__ == "__main__":
    #args = args_parse()
    train_file_path = "./train"
    test_file_path = "./test"
    trainX, trainY = load__data(train_file_path)
    testX, testY = load__data(test_file_path)

    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1, height_shift_range=0.1,
                             shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")

    train(aug, trainX, trainY, testX, testY)
    print('resloved')
