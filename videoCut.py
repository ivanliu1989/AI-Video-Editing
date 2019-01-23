import os
import re
import sys
import math
import time
import subprocess
from subprocess import run


class VideoDurationProcess:
    def __init__(self, filename):
        self.filename = filename
        return

    def preprocess(self, filename):
        # 初始化参数
        vfilename = self.filename
        logname = ""
        durtxt = ""
        durtime = ""
        duration = 0
        # 进程
        parameter = "ffmpeg.exe -i " + sys.path[0] + "/" + vfilename + " -report"
        run(parameter, shell=True)
        logexists = False
        logdir = os.listdir()
        print("读取视频信息...")
        print("目前文件：" + vfilename)
        while logexists == False:
            for logfile in logdir:
                extname = os.path.splitext(logfile)[1][1:]
                if extname == "log":
                    durfile = logfile
                    readlog = open(durfile, 'rb')
                    content = readlog.read().decode("utf-8")
                    readlog.close()
                    os.remove(logfile)
                    readdur = content[content.rfind("Duration:"):content.rfind("start") - 2]
                    print(readdur)
                    reg = 'Duration\:\s(\d+)\:(\d+)\:([\d\.]+)'
                    durtime = re.compile(reg).findall(readdur)
                    duration = int(durtime[0][0]) * 3600 + int(durtime[0][1]) * 60 + float(durtime[0][2])
                    print("总时长：" + str(duration) + "秒")
                    logexists = True
                    return duration
                else:
                    time.sleep(1)


class VideoCut:
    def __init__(self, filename):
        self.filename = filename
        return

    def process(self, filename, parttime):
        # 初始化数据
        vfilename = "input/" + self.filename
        # 可自定义输出后缀
        extvname = os.path.splitext(self.filename)[1][1:]
        # extvname = "mp4"
        durtime = VideoDurationProcess(vfilename).preprocess(vfilename)
        startat = 0
        # 进程
        print("预计分段数：" + str(math.ceil(int(durtime) / int(parttime))))
        print("-------------")
        for i in range(1, math.ceil(int(durtime) / int(parttime) + 1)):
            print("正在分割第" + str(i) + "段...")
            parameter = "ffmpeg -n -ss " + str(startat) + " -i " + vfilename + " -c copy -t " + str(
                parttime) + " output/" + self.filename + "_" + str(i) + "." + extvname
            run(parameter, shell=True)
            startat += parttime
        print("-----------已完成：" + vfilename + "-----------")
        return


if __name__ == "__main__":
    # 初始化介绍
    if os.path.exists("ffmpeg.exe"):
        print("视频分割软件 by:Black")
        print("-----------------------")
        print("请将本文件及ffmpeg.exe放在同一目录下，")
        print("并将要转换的视频放在input目录下")
    else:
        print("请把ffmpeg放到本目录后重试...")
        pass
    # 初始化参数

    if not os.path.exists("input"):
        os.mkdir("input")
    if not os.path.exists("output"):
        os.mkdir("output")
    parttime = input("请输入每多少秒分一段：")
    print("-----------------------")
    # 获取文件&处理
    filesnames = os.listdir("input")
    for filename in filesnames:
        VideoCut(filename).process(filename, int(parttime))
    print("全部处理完成！")