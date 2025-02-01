from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np

# 打开tif文件
tif_file = "D:/pythoncode/ParallelComputing/landsat/NDVI.tif"
dataset = gdal.Open(tif_file)

# 获取波段（只读取第一个波段）
band = dataset.GetRasterBand(1)

# 读取波段数据为数组
tif_array = band.ReadAsArray()

# 展示影像
plt.imshow(tif_array, cmap='gray')  # 可以根据影像类型选择合适的cmap
plt.colorbar()  # 显示色标
plt.show()
