from skimage.filters import sobel
import cv2
import time
import numpy as np


def read_image(filename):
    image = cv2.imread(filename)
    return image


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def edge_detecting(image):
    edge_sobel = sobel(image)
    return edge_sobel


if __name__ == "__main__":
    start_time = time.time()

    for i in range(100):
        image = read_image("output{}.png".format(i+1))
        image_gray = rgb2gray(image)
        image_processed = edge_detecting(image_gray)
        cv2.imwrite("D:\\pythoncode\\ParallelComputing\\Edge_detecting\\output{}.png".format(i+1), image_processed)

    end_time = time.time()
    print("边缘检测耗时：{:.2f}秒".format(end_time - start_time))