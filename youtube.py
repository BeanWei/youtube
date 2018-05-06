import subprocess
import time
import os
import urllib
import urllib.request

#视频链接txt路径
PATH = os.path.dirname(os.path.abspath(__file__)) + "/url.txt"

#视频和封面保存路径
DOWNLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\download\\"

#查询视频信息
COMMAND_PREFIX_CHECK = 'youtube-dl -F'

#下载1080p视频
COMMAND_PREFIX_DOWNLOAD = 'youtube-dl -o "{}%(title)s.%(ext)s" -f 137+140 --write-auto-sub '.format(DOWNLOAD_PATH)
#COMMAND_PREFIX_DOWNLOAD = 'youtube-dl -f 137+140 --write-auto-sub '

#获取视频标题
COMMAND_PREFIX_TITLE = 'youtube-dl -e --get-title '

#获取视频的封面
COVER_URL = 'https://i.ytimg.com/vi/{}/maxresdefault.jpg'



def download_video(url):
    '''下载视频
    param：视频链接地址
    '''
    print("下载指令："+COMMAND_PREFIX_DOWNLOAD)
    p = subprocess.Popen(COMMAND_PREFIX_DOWNLOAD + url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    start = time.time()
    print("********Start download:" + url + "\n" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))
    while True:
        line = p.stdout.readline().decode("utf8", "ignore")
        if line == '':
            break
        print(line.strip('\n'))
    p.wait()
    end =time.time()
    print("********End:"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end)))
    print("taking："+str(int(end-start))+" seconds")

def download_cover(url):
    '''获取视频封面'''
    id = url.split("=")[1]
    cover_url = COVER_URL.format(id)
    cover_name = subprocess.getstatusoutput(COMMAND_PREFIX_TITLE + url)[1]
    save_path = DOWNLOAD_PATH + cover_name + ".jpg"
    req = urllib.request.Request(cover_url)
    res = urllib.request.urlopen(req)
    get_cover = res.read()
    with open(save_path, 'wb') as fp:
        fp.write(get_cover)
        print("封面下载完成")
    

def get_url():
    '''读取文本中的视频链接'''
    print("\n********读取文本中的视频链接********")
    f = open(PATH, 'r+')
    for line in f.readlines():
        if not line == "\n":
            if line[0] == "h":
                return line.strip('\n')
    return ''

def mark_downloaded_url(url):
    '''标记下载ok的链接'''
    output = []
    f = open(PATH, 'r+')
    i = 0
    for line in f.readlines():
        line = line.strip('\n')
        url = url.strip('\n')
        if line == url:
            line = "*" + line
        output.append(line + "\n")
        i = i + 1
    f.close()
    f = open(PATH, 'w+')
    f.writelines(output)
    f.close()

if __name__ == "__main__":
    #检查url.txt是否存在
    if not os.path.exists(PATH):
        print("没有找到视频链接存放文本-url.txt,程序即将退出")
        time.sleep(2)
        exit(0)
    while True:
        url = get_url()
        print("获取：" + url)
        if url == "":
            print("全部视频和封面已下载完成")
            exit(0)
        download_video(url)
        download_cover(url)
        mark_downloaded_url(url)
