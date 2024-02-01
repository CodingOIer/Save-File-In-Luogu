'''
Author: CodingOIer redefinition0726@163.com
Date: 2024-01-29 16:50:37
LastEditors: CodingOIer redefinition0726@163.com
LastEditTime: 2024-02-01 16:14:49
FilePath: \Save-File-In-Luogu\main.py

Copyright (c) 2024 by CodingOIer, All Rights Reserved.
'''

import requests
import os
import time
import datetime
import pytz


def getCsrf(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        '_contentOnly': 'WoXiHuanFanQianXing',
        'x-luogu-type': 'content-only',
        'cookie': cookie,
        'x-requested-with': 'XMLHttpRequest',
    }
    res2 = requests.get("https://www.luogu.com.cn/", headers=headers)
    res2 = res2.text
    csrftoken = res2.split(
        '''<meta name="csrf-token" content="''')[-1].split("\">")[0]
    return csrftoken


def makeHeader(cookie):
    csrf = getCsrf(cookie)
    res = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        '_contentOnly': 'WoXiHuanFanQianXing',
        'x-luogu-type': 'content-only',
        'cookie': cookie,
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.luogu.com.cn/',
        'x-csrf-token': csrf,
        "content-type": 'application/json',
    }
    return res


def punchPaste(code, cookie):
    header = makeHeader(cookie)
    data = {
        'public': 'false',
        'data': code,
    }
    res = requests.post("https://www.luogu.com.cn/paste/new",
                        headers=header, json=data).text
    if len(res) != 17:
        return res
    else:
        r = ''
        i = 7
        while i <= 14:
            r += res[i]
            i += 1
        return r


def inputCookie():
    print('Input your uid')
    uid = input()
    print('Input your cookie')
    client_id = input()
    f = open('./.config', 'w')
    l = len(uid)
    for i in range(l):
        f.write(uid[i])
        f.write(uid[(l - 1) - i])
    f.write('\n')
    for i in range(40):
        f.write(client_id[i])
        f.write(client_id[39 - i])
    f.close()


def testCookie(cookie):
    print()


def getCookie():
    f = open('./.config', 'r')
    temp = f.readline()
    uid = ''
    i = 0
    while i < len(temp) - 1:
        uid += temp[i]
        i += 2
    temp = f.readline()
    client_id = ''
    i = 0
    while i < len(temp):
        client_id += temp[i]
        i += 2
    f.close()
    if (len(client_id) != 40 or len(uid) == 0):
        return 'RE'
    return '__client_id=' + client_id + ';_uid=' + uid + ';'


def clear():
    os.system('cls')


if __name__ == '__main__':
    clear()
    try:
        f = open('./.config', 'r')
        f.close()
        if (getCookie() == 'RE'):
            print('''Can't read cookie from config file, please input again''')
            inputCookie()
    except:
        print('''Can't find config file, please input again''')
        inputCookie()
    cookie = getCookie()
    clear()
    while True:
        command = input()
        if command == 'exit':
            clear()
            print('Programming will exit in 1 second')
            time.sleep(3)
            break
        elif command == 'logout':
            clear()
            print('Config file will remove, and programming will exit in 1 second')
            os.system('del .\\.config')
            time.sleep(3)
            break
        else:
            try:
                f = open(command, 'r', encoding='utf-8')
                temp = f.readlines()
                f.close()
                file = ''
                for i in temp:
                    file += i
                last = ''
                l = len(command)
                i = l - 1
                while i >= 0 and command[i] != '\\' and command[i] != '.':
                    last = command[i] + last
                    i -= 1
                if command[i] == '\\':
                    last = 'plain'
                line = ["""```plain""", """time: """ + str(datetime.datetime.now(pytz.timezone(
                    'Asia/Shanghai'))), """file: """ + command, """```""", """""", """```""" + last, file, """```"""]
                l = len(line)
                submit = ''
                for i in range(l):
                    submit += line[i]
                    submit += '\n'
                res = punchPaste(submit, cookie)
                if res == 'RE':
                    print("Can't punch paste, error message is " + res)
                    time.sleep(3)
                    clear()
                else:
                    print(
                        "The link of your paste is https://www.luogu.com.cn/paste/" + res)
                    time.sleep(3)
                    clear()
            except:
                print("Can't open submit file")
                time.sleep(3)
                clear()
