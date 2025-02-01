from urllib import request
import urllib.request
import random
import math
import time
import numpy as np
import io
import PIL.Image as pil
import cv2
import ast


def load_tasks_from_file(filepath):
    """该函数用于从txt文档中提取要爬取的瓦片坐标和保存路径"""
    tasks = []
    with open(filepath, 'r') as f:
        for line in f:
            task = ast.literal_eval(line.strip())  # 将每行字符串解析为 tuple
            tasks.append(task)
    return tasks


def deg2num(lat_deg, lon_deg, zoom):
    """该函数通过经纬度反算切片行列号 3857坐标系"""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def getimg(Tpath, x, y):
    """该函数用于下载瓦片"""
    # 反爬虫措施
    agents = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1']
    try:
        # print(str(x) + '_' + str(y) + '下载成功')
        req = urllib.request.Request(Tpath)
        req.add_header('User-Agent', random.choice(agents))  # 换用随机的请求头
        pic = urllib.request.urlopen(req, timeout=60)
        timg = pic.read()
        outimg = pil.new('RGBA', (256, 256))
        outimgfile = io.BytesIO(timg)
        img = pil.open(outimgfile)
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    except Exception:
        # print(str(x) + '_' + str(y) + '下载失败,重试')
        getimg(Tpath, x, y)
    return img


def GetMapTile(lat1, lon1, lat2, lon2):
    """该函数根据经纬度范围获取背景"""
    zooms = []
    for i in range(1, 19):
        l = deg2num(lat1, lon1, i)
        r = deg2num(lat2, lon2, i)
        if l[0] - r[0] == 0 or l[1] - r[1] == 0:
            continue
        else:
            zooms.append(i)
    # 下载有瓦片数据的地方的瓦片数据
    zoom = zooms[-1]
    # 根据经纬度确定瓦片位置
    lefttop = deg2num(lat1, lon1, zoom)
    rightbottom = deg2num(lat2, lon2, zoom)
    # 一边下载一边拼接
    imgcolumns = []
    imglist_all = []
    for x in range(lefttop[0], rightbottom[0]):
        imgrows = []
        imglist_row = []
        for y in range(lefttop[1], rightbottom[1]):

            # 从天地图爬取影像
            tilepath = 'http://t2.tianditu.gov.cn/DataServer?T=img_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=2ce94f67e58faa24beb7cb8a09780552'

            img = getimg(tilepath, x, y)
            imgrows.append(img)

        imgcolumn = np.vstack(imgrows)
        imgcolumns.append(imgcolumn)
    finalimg = np.hstack(imgcolumns)
    return finalimg


def worker(lat1, lon1, lat2, lon2, output_path):
    """该函数用于获取图像背景并将图像保存到本地"""
    img = GetMapTile(lat1, lon1, lat2, lon2)
    cv2.imwrite(output_path, img)


if __name__ == '__main__':

    tasks = load_tasks_from_file('tasks.txt')

    start_time = time.time()

    for task in tasks:
        worker(task[0], task[1], task[2], task[3], task[4])

    end_time = time.time()
    print("爬虫耗时：{:.2f}秒".format(end_time-start_time))

