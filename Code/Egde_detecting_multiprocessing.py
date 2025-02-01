from skimage.filters import sobel
import cv2
import time
import numpy as np
from multiprocessing import Pool


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
    cv2.imwrite(f"D:\\pythoncode\\ParallelComputing\\Edge_detecting\\output{index}.png", image_processed)


if __name__ == "__main__":
    start_time = time.time()

    # 创建进程池，允许同时运行的进程数
    with Pool(processes=24) as pool:
        # 使用进程池并行处理图像
        pool.map(process_image, range(1, 101))

    end_time = time.time()
    print("边缘检测耗时：{:.2f}秒".format(end_time - start_time))
