# coding: utf-8

import requests
import os
import telegram
import time
from telegram import error as TGError
import sys
import json

# 自定义区域

cookies_str = ''
api_key = ''
chat_id = ''

# 自定义区域结束


class DictDiffer(object):
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(
            current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])


def get_cookies(cookies_str):
    cookies = {}
    try:
        for cookie in cookies_str.split(';'):
            name, value = cookie.split('=')
            cookies[name] = value
        return cookies
    except:
        print('cookies 异常')
        exit()


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


if __name__ == "__main__":

    os.chdir(sys.path[0])

    text = ''

    cookies = get_cookies(cookies_str)

    url = 'https://m.weibo.cn/api/container/getIndex'

    page = 0
    followed_count = 0

    followed = {}

    print('获取关注列表中...')

    while True:
        page += 1

        data = {
            'containerid': '231093_-_selffollowed',
            'page': page
        }

        res = requests.get(url, params=data, cookies=cookies).json()

        try:
            if page == 1:
                cards = res['data']['cards'][1]['card_group']
            else:
                cards = res['data']['cards'][0]['card_group']

            for card in cards:
                id = str(card['user']['id'])
                screen_name = card['user']['screen_name']
                print(id, screen_name)
                followed[id] = screen_name
                followed_count += 1

        except IndexError:
            print('总关注：'+str(followed_count))
            break
        except KeyError:
            print('获取关注列表失败，可能触发微博反爬虫或 cookies 失效')
            try:
                bot = telegram.Bot(token=api_key)
                bot.sendMessage(chat_id=chat_id,
                                text='微博小助手:\n获取关注列表失败，可能触发微博反爬虫或 cookies 失效')
                exit()
            except TGError.InvalidToken:
                print('Telegram bot API token 非法')
                exit()
            except TGError.NetworkError:
                print('Telegram 无法连接')
                exit()

    if os.path.exists('weibo_follow_data.json'):
        file = open('weibo_follow_data.json', 'r', encoding='utf-8')
        old = json.load(file)
        file.close()

        diff = DictDiffer(followed, old)

        added = diff.added()
        removed = diff.removed()
        changed = diff.changed()

        if added or removed or changed:
            time_stamp = get_FileModifyTime('weibo_follow_data.json')
            text += ('距 '+time_stamp+'\n')
            text += '关注列表发生如下变化\n\n'

            if added:
                print('新增以下关注：')
                text += '新增以下关注：\n'
                for _ in added:
                    print(_, followed[_])
                    text += (followed[_] + '\n')
                text += '\n'

            if removed:
                print('减少以下关注：')
                text += '减少以下关注：\n'
                for _ in removed:
                    print(_, old[_])
                    text += (old[_] + '\n')
                text += '\n'

            if changed:
                print('以下用户已修改 ID：')
                text += '以下用户已修改 ID：\n'
                for _ in changed:
                    print('原 ID：'+old[_], '现 ID：'+followed[_])
                    text += ('原 ID：'+old[_]+' '+'现 ID：'+followed[_]+'\n')
                text += '\n'

            text = ('微博小助手\n\n'+text+'\n')

            print(text)

            try:
                bot = telegram.Bot(token=api_key)
                bot.sendMessage(chat_id=chat_id, text=text)
            except TGError.InvalidToken:
                print('Telegram bot API token 非法')
                exit()
            except TGError.NetworkError:
                print('Telegram 无法连接')
                exit()

    file = open('weibo_follow_data.json', 'w', encoding='utf-8')
    json.dump(followed, file,  ensure_ascii=False)
    file.close()
