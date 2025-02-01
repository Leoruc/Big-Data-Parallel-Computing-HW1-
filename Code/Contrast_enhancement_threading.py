import threading
from skimage import exposure
import cv2
import time
import numpy as np


def read_image(filename):
    image = cv2.imread(filename)
    return image


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def expose(image):
    image_eq = exposure.equalize_hist(image)
    image_eq_uint8 = (image_eq * 255).astype(np.uint8)  # 将浮点图像转换回uint8格式，符合imwrite函数的要求
    return image_eq_uint8


def process_image(index):
    image = read_image(f"output{index}.png")
    image_gray = rgb2gray(image)
    image_processed = expose(image_gray)
    cv2.imwrite(f"D:\\pythoncode\\ParallelComputing\\Expose\\output{index}.png", image_processed)


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
    print("对比度增强耗时：{:.2f}秒".format(end_time - start_time))

