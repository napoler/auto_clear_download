# coding:utf-8
import os
# import timeit
import time
# rlist=["家里"]
import shutil
"""
自动清理目录里的拉圾内容
自动清理十天未下载完成的任务
"""
limit_size=100 #MB 限制最小视频大小
video_type=('.mp4', '.mkv', '.avi', '.wmv', '.iso')
tmp_type=('.aria2', '.qt', '.torrent')
def get_FileSize(filePath):
    '''获取文件的大小,结果保留两位小数，单位为MB'''
    # filePath = unicode(filePath,'utf8')
    try:
        fsize = os.path.getsize(filePath)

    except :
        return
        pass   
    
    fsize = fsize/float(1024*1024)
    return round(fsize,2)
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
    except :
        return
        pass

    timestamp=time.time()-file_time
    # print(timestamp/(60*60))

    # m, s = divmod(timestamp, 60)
    # h, m = divmod(m, 60)
    # print("time",h,m,s)
    return timestamp/(60*60) #返回时间差 单位小时
def main():
    #    rpath=raw_input("输入目录：")
    rpath="/mnt/c/transmission/aria"
    # f2 = open("/mnt/b/clear/remove.txt","r")
    # rlist = f2.readlines()
    rn=[]
    for pathname,dirnames,filenames in os.walk(rpath):
        for filename in filenames:
            file=os.path.join(pathname,filename)
            
            if file.endswith(".aria2"):
                new_file=file.replace(".aria2",'')
                os.remove(file)
                try:
                    os.remove(new_file)
                    pass
                except:
                    
                    pass
                try:
                    shutil.rmtree(new_file)
                    pass
                except:
                    pass
                
                rn.append(file)
                rn.append(new_file)

    print("删除：",rn)
    print("共计删除：",len(rn))
if __name__=='__main__':
    main()
