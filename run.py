# coding:utf-8
import os
import timeit
# rlist=["家里"]

def main():
    rpath=raw_input("输入目录：")
    #rpath="/mnt/c/transmission/aria"
    f2 = open("remove.txt","r")
    rlist = f2.readlines()
    rn=[]
    for pathname,dirnames,filenames in os.walk(rpath):
        for filename in filenames:
            file=os.path.join(pathname,filename)
            print(file)
            for it in rlist:
                it=it.replace("\n", "")
                #print(it,file)
                #print(str(it) in  str(file))
                if it in  str(file):
                    print("删除")
                    rn.append(file)
                    os.remove(file)
                    break
                else:
                    #print("忽略")
                    pass
            # os.remove(file)
    print("删除：",rn)
    print("共计删除：",len(rn))
if __name__=='__main__':
    main()