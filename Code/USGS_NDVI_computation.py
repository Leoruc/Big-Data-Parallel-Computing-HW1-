from osgeo import gdal, gdalconst
import os
import time


def NDVI_calculte(Red_band_file, NIR_band_file, NDVI_output_file):
    """
    红光与近红外波段分别存储为tif文件的NDVI指数计算
    :param Red_band_file: 红光波段文件
    :param NIR_band_file: 近红外波段文件
    :param NDVI_output_file: 输出NDVI影像
    :return:
    """
    band_Red = gdal.Open(Red_band_file, gdalconst.GA_ReadOnly)
    band_NIR = gdal.Open(NIR_band_file, gdalconst.GA_ReadOnly)

    cols_Red = band_Red.RasterXSize  # 列数
    rows_Red = band_Red.RasterYSize  # 行数
    cols_NIR = band_NIR.RasterXSize  # 列数
    rows_NIR = band_NIR.RasterYSize  # 行数
    data_type_Red = band_Red.GetRasterBand(1).DataType
    data_type_NIR = band_NIR.GetRasterBand(1).DataType
    geotrans = list(band_Red.GetGeoTransform())
    if (cols_Red != cols_NIR or rows_Red != rows_NIR or data_type_Red != data_type_NIR):
        print("输入红光波段与近红外波段影像参数不对应")
        return

    if os.path.exists(NDVI_output_file) and os.path.isfile(NDVI_output_file):  # 如果已存在同名影像
        os.remove(NDVI_output_file)  # 则删除之

    NDVI = band_Red.GetDriver().Create(NDVI_output_file, xsize=cols_Red, ysize=rows_Red, bands=1,
                                       eType=data_type_Red)  # 创建空的与待处理的tif文件
    NDVI.SetProjection(band_Red.GetProjection())  # 设置投影坐标
    NDVI.SetGeoTransform(geotrans)  # 设置地理变换参数

    data_Red = band_Red.ReadAsArray(buf_xsize=cols_Red, buf_ysize=rows_Red)  # 以numpy数组形式读取出图像
    data_NIR = band_NIR.ReadAsArray(buf_xsize=cols_NIR, buf_ysize=rows_NIR)
    data_NDVI = data_NIR
    count = 0  # 记录异常值的个数
    list_x = []
    list_y = []  # 记录异常值像素的X,Y坐标
    k = 1  # 记录进度
    print("完成进度:", end=" ")
    for i in range(0, rows_Red):
        for j in range(0, cols_Red):
            if (data_NIR[i][j] + data_Red[i][j] != 0 and data_Red[i][j] != 0 and data_NIR[i][j] != 0):
                data_NDVI[i][j] = (data_NIR[i][j] - data_Red[i][j]) / (data_NIR[i][j] + data_Red[i][j])
                if (data_NDVI[i][j] < -1 or data_NDVI[i][j] > 1):  # 剔除异常值，使最终NDVI范围在[-1, 1]内
                    data_NDVI[i][j] = 0
                    count += 1  # 记录异常值的个数，
                    list_x.append(i + 1)
                    list_y.append(j + 1)  # 记录异常值像素的X,Y坐标
            else:
                data_NDVI[i][j] = 0
        if i == int(k * (rows_Red / 10)) - 1:  # 以10%的进度单位设置进度条
            print(str(k) + "0% ", end="")  # 记录进度
            k += 1
    NDVI.GetRasterBand(1).WriteArray(data_NDVI)  # 写入数据到新影像中
    NDVI.GetRasterBand(1).FlushCache()
    NDVI.GetRasterBand(1).ComputeBandStats(False)  # 计算统计信息
    print("\n已剔除异常值，异常值个数为" + str(count) + "个")
    print("正在写入完成")
    del band_Red
    del band_NIR


if __name__ == "__main__":
    start_time = time.time()
    print("**********正在开始读取**********")
    band_Red = "D:/pythoncode/ParallelComputing/landsat/LC09_L2SP_005016_20241014_20241015_02_T1_SR_B4.tif"  # 红光波段文件
    band_NIR = "D:/pythoncode/ParallelComputing/landsat/LC09_L2SP_005016_20241014_20241015_02_T1_SR_B5.tif"  # 近红外波段文件
    NDVI_output_file = "D:/pythoncode/ParallelComputing/landsat/NDVI.tif "  # 输出NDVI指数文件
    NDVI_calculte(band_Red, band_NIR, NDVI_output_file)
    end_time = time.time()
    print("生成NDVI图像耗时：{:.2f}秒".format(end_time-start_time))
    print("**********读取计算完成**********")