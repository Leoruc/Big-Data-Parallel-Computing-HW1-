from skimage.filters import gaussian
import cv2
import time
import numpy as np


def read_image(filename):
    image = cv2.imread(filename)
    return image


def gaussian_filtering(image):
    gaussian_image = gaussian(image, channel_axis=2)
    gaussian_image_uint8 = (gaussian_image * 255).astype(np.uint8)  # 将浮点图像转换回uint8格式，符合imwrite函数的要求
    return gaussian_image_uint8


if __name__ == "__main__":
    start_time = time.time()

    for i in range(100):
        image = read_image("output{}.png".format(i+1))
        image_processed = gaussian_filtering(image)
        cv2.imwrite("D:\\pythoncode\\ParallelComputing\\Gaussian_filtering\\output{}.png".format(i+1), image_processed)

    end_time = time.time()
    print("高斯滤波耗时：{:.2f}秒".format(end_time - start_time))


