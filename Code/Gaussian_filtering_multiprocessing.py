from skimage.filters import gaussian
import cv2
import time
import numpy as np
from multiprocessing import Pool


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
    cv2.imwrite(f"D:\\pythoncode\\ParallelComputing\\Gaussian_filtering\\output{index}.png", image_processed)


if __name__ == "__main__":
    start_time = time.time()

    # 创建进程池，允许同时运行的进程数
    with Pool(processes=24) as pool:
        # 使用进程池并行处理图像
        pool.map(process_image, range(1, 101))

    end_time = time.time()
    print("高斯滤波耗时：{:.2f}秒".format(end_time - start_time))