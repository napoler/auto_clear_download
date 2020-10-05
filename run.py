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
tmp_type=('.aria2', '.\Qt', '.torrent')
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
    f2 = open("/mnt/b/clear/remove.txt","r")
    rlist = f2.readlines()
    rn=[]
    for pathname,dirnames,filenames in os.walk(rpath):
        for filename in filenames:
            file=os.path.join(pathname,filename)
            print(file)
            get_filetime(file)
            size=get_FileSize(file)
            print(size,'M')
            #清理过小的视频文件
            if file.endswith(video_type) and size < limit_size:
                print("过小视频",size)
                print("删除")
                rn.append(file)
                os.remove(file)
            #清理时间过长的aria2和qt下载文件等等
            timestamp=get_filetime(file)
            if file.endswith(tmp_type) and timestamp>24*10:
                print("时间过久的临时文件",timestamp)
                print("删除")
                rn.append(file)

                new_file=file.replace(".aria2",'')
                os.remove(file)
                rn.append(new_file)
                #清理对应的文件
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

            for it in rlist:
                it=it.replace("\n", "")
                #print(it,file)
                #print(str(it) in  str(file))
                if it in  str(file):
                    print("删除")
                    try:
                        rn.append(file)
                        os.remove(file)
                    except:
                        pass
   
                    break
                else:
                    #print("忽略")
                    pass
            # os.remove(file)
    print("删除：",rn)
    print("共计删除：",len(rn))
if __name__=='__main__':
    main()
