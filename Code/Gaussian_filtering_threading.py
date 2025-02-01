import threading
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


def process_image(index):
    image = read_image(f"output{index}.png")
    image_processed = gaussian_filtering(image)
    cv2.imwrite(f"D:\\pythoncode\\ParallelComputing\\Edge_detecting\\output{index}.png", image_processed)


if __name__ == "__main__":
    start_time = time.time()

    # 创建线程列表
    threads = []

    for i in range(1, 101):  # 处理 40 张图像
        t = threading.Thread(target=process_image, args=(i,))
        threads.append(t)
        t.start()  # 启动线程

    # 等待所有线程完成
    for t in threads:
        t.join()

    end_time = time.time()
    print("高斯滤波耗时：{:.2f}秒".format(end_time - start_time))