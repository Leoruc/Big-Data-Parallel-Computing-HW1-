import threading
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


def process_image(index):
    image = read_image(f"output{index}.png")
    image_gray = rgb2gray(image)
    image_processed = edge_detecting(image_gray)
    cv2.imwrite(f"D:\\pythoncode\\ParallelComputing\\Gaussian_filtering\\output{index}.png", image_processed)


if __name__ == "__main__":
    start_time = time.time()

    # 创建线程列表
    threads = []

    for i in range(1, 101):  # 处理 20 张图像
        t = threading.Thread(target=process_image, args=(i,))
        threads.append(t)
        t.start()  # 启动线程

    # 等待所有线程完成
    for t in threads:
        t.join()

    end_time = time.time()
    print("边缘检测耗时：{:.2f}秒".format(end_time - start_time))
