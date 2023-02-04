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
clear subtitle
"""
limit_size = 100  # MB 限制最小视频大小
subtitle_type = ('.ass', '.srt')
tmp_type = ('.aria2', '.\Qt', '.!qB', '.torrent')
clear_wd = ["zh-CN.srt", "zh-cn.srt", "zh-CN.ass", "zh-cn.ass"]


def main(
        rpath="",
        ffmpeg_args={

        }):
    rn = []
    i = 0
    for pathname, dirnames, filenames in os.walk(rpath):
        for filename in filenames:
            file = os.path.join(pathname, filename)

            if file.endswith(subtitle_type):
                load1, load5, load15 = os.getloadavg()
                while load1 > 50:
                    time.sleep(100)
                for r in clear_wd:
                    if r in file:
                        try:

                            os.remove(file)
                            i = i+1

                            print(f"rm file {i}:{file}")
                            break
                        except:
                            pass


if __name__ == '__main__':
    ffmpeg_args = {

    }
    params = {}
    rpaths = [
        "/data/pjav/", "/data/pjaven/", "/data/pic/", "/data/movies/",
        "/data/tv/"
    ]
    # rpaths = ["/data/pjav/test/"]
    random.shuffle(rpaths)

    for rpath in rpaths:
        main(rpath, ffmpeg_args)
