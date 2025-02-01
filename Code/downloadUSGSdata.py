import multiprocessing
import time
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer


def search_scenes(username, password, dataset, latitude, longitude, start_date, end_date, max_cloud_cover):

    scene_ids = []

    api = API(username, password)

    scenes = api.search(
        dataset=dataset,
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
        max_cloud_cover=max_cloud_cover
    )

    for scene in scenes:
        scene_ids.append(scene['landsat_scene_id'])

    api.logout()

    return scene_ids


def downloadfile(ee, scene_id, retries):
    for attempt in range(retries):
        try:
            ee.download(scene_id, output_dir='D:\\pythoncode\\ParallelComputing\\USGS')
            break  # 如果下载成功，退出循环
        except Exception as e:
            print(f" {scene_id} 下载失败, 进行第 {attempt + 1} 次尝试. Error: {e}")
            time.sleep(5)  # 等待5秒后重试
            if attempt == retries - 1:
                print(f" {scene_id} 无法下载.")



if __name__ == "__main__":

    username = 'your own username'  # 此处请替换为你自己注册的用户名
    password = 'your own password'  # 此处请替换为你自己的密码
    dataset = 'landsat_tm_c2_l1'    # 数据集
    latitude = 50.85                # 纬度
    longitude = -4.35               # 经度
    start_date = '1995-01-01'       # 搜索起始日期
    end_date = '1995-12-31'         # 搜索终止日期
    max_cloud_cover = 10            # 最大云量


    scene_ids = search_scenes(username, password, dataset, latitude, longitude, start_date, end_date, max_cloud_cover)

    print(f"共发现{len(scene_ids)}幅影像。")

    processes = []

    ee = EarthExplorer(username, password)
    retries = 3

    for scene_id in scene_ids:
        p = multiprocessing.Process(target=downloadfile, args=(ee, scene_id, retries))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    ee.logout()