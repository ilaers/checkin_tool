#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time, sys, configparser,random,base64,logging,json
from logging import handlers
from threading import Thread

try:
    from tkinter import *
except ImportError:  # Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    # Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    # Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    # import tkFileDialog
    # import tkSimpleDialog
else:  # Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    # import tkinter.filedialog as tkFileDialog
    # import tkinter.simpledialog as tkSimpleDialog    #askstring()

import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)# 禁用安全请求警告

from ui import Application_ui

conf = configparser.ConfigParser()
ini_path = 'config.ini'
conf.read(ini_path, encoding='utf-8')
if 'rabbit' in conf.sections():
    for i in conf.items('rabbit'):
        print (i)
        if 'username' in i:
            rabbit_username = i[1]
        elif 'password' in i:
            rabbit_password = base64.b64decode(i[1])
        elif 'login_url' in i:
            rabbit_login_url = i[1]
        elif 'checkin_url' in i:
            rabbit_checkin_url = i[1]
        elif 'loop' in i:
            rabbit_loop = i[1]
else:
    sys.exit()

if 'myunlu' in conf.sections():
    for i in conf.items('myunlu'):
        if 'username' in i:
            myunlu_username = i[1]
        elif 'password' in i:
            myunlu_password =base64.b64decode(i[1])
        elif 'login_url' in i:
            myunlu_login_url = i[1]
        elif 'checkin_url' in i:
            myunlu_checkin_url = i[1]
        elif 'loop' in i:
            myunlu_loop = i[1]
else:
    sys.exit()

if 'mteam' in conf.sections():
    for i in conf.items('mteam'):
        if 'username' in i:
            mteam_username = i[1]
        elif 'password' in i:
            mteam_password =base64.b64decode(i[1])
        elif 'login_url' in i:
            mteam_login_url = i[1]
        elif 'checkin_url' in i:
            mteam_checkin_url = i[1]
        elif 'loop' in i:
            mteam_loop = i[1]
else:
    sys.exit()

if 'app' in conf.sections():
    for i in conf.items('app'):
        if 'default_frame' in i:
            default_frame = i[1]
else:
    sys.exit()
rabbit_flag=1
myunlu_flag=1
class Rabbit_Checkin(Thread):
    def __init__(self, username, password, login_url, checkin_url,rabbit_text,rabbit_label_text,rabbit_log):
        Thread.__init__(self)
        self.username = username
        self.passsword = password
        self.login_url = login_url
        self.checkin_url = checkin_url
        self.rabbit_text=rabbit_text
        self.rabbit_label_text=rabbit_label_text
        self.rabbit_log=rabbit_log
    def run(self):
        global  rabbit_flag
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101',
        }
        login_data = {'email': self.username,
                      'passwd': self.passsword,
                      'remember_me': 'week'
                      }
        # proxy = {'http': 'http://127.0.0.1:8848'}
        # 循环
        t1 = float(time.time())
        rabbit_num = 0
        while 1:
            if rabbit_flag == 0:
                break
            if rabbit_num > 0:
                if float(time.time()) - t1 < 60*60*24:
                    continue
            # 条件成立，开始登录签到
            self.rabbit_text.insert(1.0, '###############\n{},开始本次rabbit登录。\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            self.rabbit_log.warning('###############\n开始本次rabbit登录。')
            s = requests.Session()
            r1 = s.post(url=self.login_url,
                        headers=headers,
                        data=login_data,
                        # proxies=proxy,
                        verify=False)
            status_code = r1.status_code
            print(status_code)
            contents = json.loads(r1.content)
            if status_code == 200 and contents.get('ret') == 1:
                self.rabbit_text.insert(1.0, '{},rabbit登录成功。\n'.format(
                    time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                self.rabbit_log.warning('rabbit登录成功。')
                r2 = s.post(
                    url=self.checkin_url,
                    headers=headers,
                    # proxies=proxy,
                    verify=False
                )
                status_code2 = r2.status_code
                contents2 = json.loads(r2.content)
                if status_code2 and contents2.get('ret')==1:
                    self.rabbit_text.insert(1.0, '{},rabbit签到成功。\n'.format(
                        time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                    self.rabbit_log.warning('rabbit签到成功。')
            else:
                self.rabbit_text.insert(1.0, '{},rabbit签到成功。\n'.format(
                    time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                self.rabbit_log.warning('rabbit签到成功。')
            rabbit_num += 1
            self.rabbit_label_text.set(
                '最后签到:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            t1 = float(time.time())
        # 跳出循环，停止签到
        self.rabbit_text.insert(1.0, '{},停止rabbit签到！\n###############\n'.format(
            time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
        self.rabbit_log.warning('停止rabbit签到！')
        
class Myunlu_Checkin(Thread):
    def __init__(self, username, password, login_url, checkin_url,myunlu_text,myunlu_label_text,myunlu_log):
        Thread.__init__(self)
        self.username = username
        self.passsword = password
        self.login_url = login_url
        self.checkin_url = checkin_url
        self.myunlu_text=myunlu_text
        self.myunlu_label_text=myunlu_label_text
        self.myunlu_log=myunlu_log
    def run(self):
        global  myunlu_flag
        headers = {
            'Host': 'myunlu.com',
            'Connection': 'keep-alive',
            'Origin': 'https://myunlu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
        }
        #循环
        t1=float(time.time())
        myunlu_num=0
        while 1:
            if myunlu_flag==0:
                break
            if myunlu_num>0:
                if float(time.time()) -t1<random.uniform(60*15,60*16):
                    continue
            #条件成立，开始登录签到
            self.myunlu_text.insert(1.0,'###############\n{},开始本次登录。\n'.format(time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            self.myunlu_log.warning('###############\n开始本次登录。')
            s = requests.session()
            r1 = s.get(url=self.login_url, headers=headers, verify=False)
            soup = BeautifulSoup(r1.content, 'html.parser')
            csrftoken = soup.find('input', {'name': 'csrfToken'}).get('value')#获取登录的token
            self.myunlu_text.insert(1.0,'{},获取本次登录csrftoken：{}。\n'.format(time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time()))),csrftoken))
            self.myunlu_log.warning('获取本次登录csrftoken：{}。'.format(csrftoken))
            postdata = {'csrfToken': csrftoken,
                        'email': self.username,
                        'password': self.passsword,
                        'rememberMe': 'on'
                        }
            headers['Referer'] = 'https://myunlu.com/signin'
            r2 = s.post(url=self.login_url, headers=headers, data=postdata, verify=False)

            if r2.status_code == requests.codes.ok:
                self.myunlu_text.insert(1.0,'{},登录成功。\n'.format(time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                self.myunlu_log.warning('登录成功。')
                headers['Referer'] = 'https://myunlu.com/user/center'
                r3 = s.get(url='https://myunlu.com/user/invite', headers=headers, verify=False)
                soup = BeautifulSoup(r3.content, 'html.parser')
                pp = soup.find_all('p')
                for p in pp:
                    if u'邀请码：' in p.text:
                        invite = p.text
                        self.myunlu_text.insert(1.0,'{},签到成功。\n'.format(time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                        self.myunlu_text.insert(1.0,'{}\n'.format(invite))
                        self.myunlu_log.warning('签到成功.')
            myunlu_num+=1
            self.myunlu_label_text.set('最后签到:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            t1 = float(time.time())
        #跳出循环，停止签到
        self.myunlu_text.insert(1.0,'{},停止签到！\n###############\n'.format(time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
        self.myunlu_log.warning('停止签到！')
class Application(Application_ui):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        # print('self.{}'.format(default_frame))
        # globals()['self.{}'.format(default_frame)].tkraise()
        self.myunlu_frame.tkraise()

        self.level_relations = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'crit': logging.CRITICAL
        }  # 日志级别关系映射
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        self.rabbit_log = self.Logger('{}_rabbit.log'.format(time.strftime('%Y-%m-%d', time.localtime(int(time.time())))),
                                    level='warning')

        self.myunlu_log = self.Logger('{}_myunlu.log'.format(time.strftime('%Y-%m-%d', time.localtime(int(time.time())))),
                                level='warning')

        self.mteam_log = self.Logger('{}_mteam.log'.format(time.strftime('%Y-%m-%d', time.localtime(int(time.time())))),
                                    level='warning')

    def Logger(self, filename, level='info', when='D', backCount=180,
               fmt='%(asctime)s -[line:%(lineno)d] - %(levelname)s: %(message)s'):  # %(pathname)s
        logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        logger.addHandler(sh)  # 把对象加到logger里
        logger.addHandler(th)
        return logger

    def exit_Cmd(self, event=None):
        # TODO, Please finish the function here!
        if askokcancel("退出", "是否退出  “签到工具”  ?"):
            self.master.destroy()

    def rabbit_checkin_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.rabbit_frame.tkraise()

    def rabbit_start_Cmd(self, event=None):
        # TODO, Please finish the function here!
        rc1 = Rabbit_Checkin(rabbit_username, rabbit_password, rabbit_login_url,
                             rabbit_checkin_url, self.rabbit_text, self.rabbit_label_text, self.rabbit_log)
        rc1.start()

    def rabbit_stop_Cmd(self, event=None):
        # TODO, Please finish the function here!
        global rabbit_flag
        rabbit_flag=0

    def rabbit_checkbutton_Cmd(self, event=None):
        # TODO, Please finish the function here!
        conf = configparser.ConfigParser()
        ini_path = 'config.ini'
        conf.read(ini_path, encoding='utf-8')
        if self.rabbit_checkVar.get() == '1':
            conf.set("rabbit", "loop", "0")  #更改值
            self.rabbit_text.insert(1.0, '{},rabbit的循环签到已取消.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            self.rabbit_log.warning('rabbit的循环签到已取消。')
        elif self.rabbit_checkVar.get() == '0':
            conf.set("myunlu", "loop", "1")   #更改值
            self.rabbit_text.insert(1.0, '{},rabbit的循环签到已启动.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            self.rabbit_log.warning('rabbit的循环签到已启用。')
        conf.write(open('config.ini', "r+", encoding="utf-8"))  # r+模式
    #############################
    def myunlu_checkin_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.myunlu_frame.tkraise()

    def myunlu_start_Cmd(self, event=None):
        # TODO, Please finish the function here!
        mc1=Myunlu_Checkin(myunlu_username,myunlu_password,myunlu_login_url,
                           myunlu_checkin_url,self.myunlu_text,self.myunlu_label_text,self.myunlu_log)
        mc1.start()
    def myunlu_stop_Cmd(self, event=None):
        # TODO, Please finish the function here!
        global myunlu_flag
        myunlu_flag=0


    def myunlu_checkbutton_Cmd(self, event=None):
        # TODO, Please finish the function here!
        onf = configparser.ConfigParser()
        ini_path = 'config.ini'
        conf.read(ini_path, encoding='utf-8')
        if self.myunlu_checkVar.get() == '1':
            conf.set("myunlu", "loop", "0")  # 更改值
            self.myunlu_text.insert(1.0, '{},myunlu的循环签到已取消.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            self.myunlu_log.warning('myunlu的循环签到已取消。')
        elif self.myunlu_checkVar.get() == '0':
            conf.set("myunlu", "loop", "1")  # 更改值
            self.myunlu_text.insert(1.0, '{},myunlu的循环签到已启动.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            self.myunlu_log.warning('myunlu的循环签到已启动。')
    #############################

    def mteam_checkin_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.mteam_frame.tkraise()

    def mteam_start_Cmd(self, event=None):
        # TODO, Please finish the function here!
        pass

    def mteam_stop_Cmd(self, event=None):
        # TODO, Please finish the function here!
        pass

    def mteam_checkbutton_Cmd(self, event=None):
        # TODO, Please finish the function here!
        if self.mteam_checkVar.get() == '1':
            self.myunlu_log.warning()
            self.mteam_text.insert(1.0, '{},mteam的循环签到已取消.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
        elif self.mteam_checkVar.get() == '0':
            self.mteam_text.insert(1.0, '{},mteam的循环签到已启动.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))


class Checkin_App(object):
    def app_start(self):
        top = Tk()
        top.title('{}'.format('签到工具'))
        top.resizable(width=False, height=False)  # 窗口禁止拉伸
        # linux和windows通用的最大化
        self.w, self.h = top.maxsize()
        sw = top.winfo_screenwidth()
        sh = top.winfo_screenheight()
        x = int((sw - self.w * 0.3) / 2)
        y = int((sh - self.h * 0.4) / 2)
        width = int(self.w * 0.30)
        height = int(self.h * 0.40)
        top.geometry("{}x{}+{}+{}".format(width, height, x, y))
        top.attributes('-toolwindow', 0,  # 可设置窗口为工具栏样式
                       '-alpha', 1,  # 可设置透明度，0完全透明，1不透明。窗口内的所有内容
                       '-fullscreen', False,  # 设置全屏
                       '-topmost', False)  # 设置窗口置顶。
        top.overrideredirect(0)  # 去掉标题栏
        Application(top).mainloop()
        try:
            top.destroy()
        except:
            pass
