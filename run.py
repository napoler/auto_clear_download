# coding:utf-8
import os
import timeit
# rlist=["家里"]
path=input("输入目录：")
f2 = open("remove.txt","r")
rlist = f2.readlines()
def main():
    for pathname,dirnames,filenames in os.walk(path):
        for filename in filenames:
            file=os.path.join(pathname,filename)
            print(file)
            for it in rlist:
                if it in  file:
                    print("删除")
                    os.remove(file)
                    break
                else:
                    # print("忽略")
                    pass
            # os.remove(file)
if __name__=='__main__':
    main()