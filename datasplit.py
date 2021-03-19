import os
import shutil
import random

def main():
    pathlist = os.listdir("./games")
    for path in pathlist:
        imglist = os.listdir('./games/'+path)
        if len(imglist) > 40:
            #随机化图片列表，并且去掉截图文件夹内最后的info文件
            random.seed(42)
            random.shuffle(imglist[0:-1])
            #检查是否已经存在文件夹，没有则创建
            try:
                os.makedirs('./test/'+path)
                os.makedirs('./train/'+path)
            except FileExistsError:
                pass
            for i in range(0, len(imglist)-1):
                #检查图片是否已经被添加进
                if(os.path.exists('./test/'+path+'/'+imglist[i]) or os.path.exists('./train/'+path+'/'+imglist[i])):
                    continue
                else:
                    if i < len(imglist)//3:
                        shutil.copyfile(
                            './games/'+path+'/'+imglist[i], './test/'+path+'/'+imglist[i])
                    else:
                        shutil.copyfile(
                            './games/'+path+'/'+imglist[i], './train/'+path+'/'+imglist[i])


if __name__ == "__main__":
    print("开始划分测试集，训练集\n---------------------------------------")
    main()
    print("划分完成")
