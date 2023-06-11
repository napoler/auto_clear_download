# coding:utf-8
import os
# import timeit
import time
# rlist=["家里"]
import shutil
from video_convert import convert_file
from tqdm.auto import tqdm
import random
"""
自动清理目录里的拉圾内容
自动清理十天未下载完成的任务
"""
limit_size = 100  # MB 限制最小视频大小
video_type = ('.mp4', '.mkv', '.avi', '.wmv', '.ts')
tmp_type = ('.aria2', '.\Qt', '.!qB', '.torrent')


def get_FileSize(filePath):
    '''获取文件的大小,结果保留两位小数，单位为MB'''
    # filePath = unicode(filePath,'utf8')
    try:
        fsize = os.path.getsize(filePath)

    except:
        return
        pass

    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


# def get_FileModifyTime(filePath):
#     t = os.path.getmtime(filePath)
#     return TimeStampToTime(t)


def get_filetime(filePath):
    """
    获取文件创建多久了
    距离当前的时间
    单位小时
    """
    try:
        file_time = os.path.getatime(filePath)
        pass
    except:
        return
        pass

    timestamp = time.time() - file_time
    # print(timestamp/(60*60))

    # m, s = divmod(timestamp, 60)
    # h, m = divmod(m, 60)
    # print("time",h,m,s)
    return timestamp / (60 * 60)  # 返回时间差 单位小时


def main(
        rpath="",
        ffmpeg_args={
            'ab': 128,  # audio bitrate is 128kbps by default
            'vb': 2048,  # video bitrate is 800K by default
        }):
    rn = []
    files=[]
    for pathname, dirnames, filenames in os.walk(rpath):


        for filename in tqdm(filenames):

            file = os.path.join(pathname, filename)
            # print(file)
            # get_filetime(file)
            size = get_FileSize(file)
            # print(size, 'M')
            # 清理过小的视频文件
            if file.endswith(video_type):
                files.append(file)
    random.shuffle(files)
    # 执行转码
    for file in tqdm(files):
        load1, load5, load15 = os.getloadavg()
        while load1 > 50:
            time.sleep(100)
        try:
            convert_file(file, ffmpeg_args)
        except:
            pass


if __name__ == '__main__':
    ffmpeg_args = {
        'ab': 128,  # audio bitrate is 128kbps by default
        'vb': 2048,  # video bitrate is 800K by default
    }
    params = {}
    rpaths = [
        "/data/pjav/", "/data/pjaven/", "/data/pic/", "/data/movies/",
        "/data/tv/"
    ]
    # rpaths = ["/data/pjav/test/"]
    random.shuffle(rpaths)
    while True:
        for rpath in rpaths:
            main(rpath, ffmpeg_args)
        time.sleep(60*60*24)
