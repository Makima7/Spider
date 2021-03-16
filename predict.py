from keras.preprocessing.image import img_to_array
from keras.models import load_model
from sklearn import preprocessing
import numpy as np
import argparse
import imutils
import cv2
import os


norm_size = 350


def args_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True,
                    help="path to trained model")
    ap.add_argument("-i", "--image", required=True,
                    help="path to trained model")
    ap.add_argument("-s", "--show", action="store_true",
                    help="show predicted image", default=False)
    args = vars(ap.parse_args())
    return args


def predict(args):
    print(("loading network\n----------------------"))
    model = load_model(args["model"])

    image = cv2.imread(args["image"])
    orig = image.copy()

    image = cv2.resize(image, (norm_size, norm_size))
    image = image.astype("float")/255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    result = model.predict(image)[0]
    print(result)
    proba = np.max(result)

    le = preprocessing.LabelEncoder()
    le = le.fit(os.listdir("./train"))

    label = str(le.inverse_transform(np.where(result == proba)[0]))
    
    label = "{}:{:.2f}%".format(label, proba*100)
    print(label)


if __name__ == '__main__':
    args = args_parse()
    predict(args)
