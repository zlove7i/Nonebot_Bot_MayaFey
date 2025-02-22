"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/3/27 18:32
"""
import os
import platform
import random
import sys
import requests

import httpx

from nonebot import logger, get_driver
from .json_tools import json_load, json_write
from .path import config_path, translate_path
from .url import avatar_base_url

nicknames = get_driver().config.nickname


async def mk(type_, path_, *mode, **kwargs):
    """
    创建文件夹 下载文件
    :param type_: ['dir', 'file']
    :param path_: Path
    :param mode: ['wb', 'w']
    :param kwargs: ['url', 'content', 'dec', 'info'] 文件地址 写入内容 描述信息 和 额外信息
    :return: None
    """
    if 'info' in kwargs:
        logger.info(kwargs['info'])
    if type_ == "dir":
        os.mkdir(path_)
        logger.info(f"创建文件夹{path_}")
    elif type_ == "file":
        if 'url' in kwargs:
            if kwargs['dec']:
                logger.info(f"开始下载文件{kwargs['dec']}")
            async with httpx.AsyncClient() as client:
                r = await client.get(kwargs['url'])
                if mode[0] == "w":
                    with open(path_, "w", encoding="utf-8") as f:
                        f.write(r.text)
                elif mode[0] == "wb":
                    with open(path_, "wb") as f:
                        f.write(r.content)
                logger.info(f"下载文件 {kwargs['dec']} 到 {path_}")
        else:
            if mode:
                with open(path_, mode[0], encoding="utf-8") as f:
                    f.write(kwargs["content"])
                logger.info(f"创建文件{path_}")
            else:
                raise Exception("mode 不能为空")
    else:
        raise Exception("type_参数错误")


def mk_sync(type_, path_, *mode, **kwargs):
    """
    创建文件夹 下载文件
    :param type_: ['dir', 'file']
    :param path_: Path
    :param mode: ['wb', 'w']
    :param kwargs: ['url', 'content', 'dec', 'info'] 文件地址 写入内容 描述信息 和 额外信息
    :return: None
    """
    if 'info' in kwargs:
        logger.info(kwargs['info'])
    if type_ == "dir":
        os.mkdir(path_)
        logger.info(f"创建文件夹{path_}")
    elif type_ == "file":
        if 'url' in kwargs:
            if kwargs['dec']:
                logger.info(f"开始下载文件{kwargs['dec']}")
                r = requests.get(kwargs['url'])
                if mode[0] == "w":
                    with open(path_, "w", encoding="utf-8") as f:
                        f.write(r.text)
                elif mode[0] == "wb":
                    with open(path_, "wb") as f:
                        f.write(r.content)
                logger.info(f"下载文件 {kwargs['dec']} 到 {path_}")
        else:
            if mode:
                with open(path_, mode[0], encoding="utf-8") as f:
                    f.write(kwargs["content"])
                logger.info(f"创建文件{path_}")
            else:
                raise Exception("mode 不能为空")
    else:
        raise Exception("type_参数错误")


def translate(mode: str, name: str) -> str:
    """
    插件名称翻译
    mode: e2c(英译中) c2e(中译英)
    name: 插件名
    """
    # 翻译文件
    plugin_translate: dict = json_load(translate_path)
    # e2c 英译中
    if mode == 'e2c':
        if name not in plugin_translate:
            return name
        for name_en in plugin_translate:
            if name == name_en:
                return plugin_translate[name_en]

    # c2e 中译英
    elif mode == 'c2e':
        for name_en in plugin_translate:
            if plugin_translate[name_en] == name:
                return name_en
        return name

    else:
        return name


def translate_update(plugin_name: str, translated: str):
    """
    更新插件翻译
    plugin_name: 插件名
    translated: 翻译文本
    """
    js = json_load(translate_path)
    js.update({plugin_name: translated})
    json_write(translate_path, js)


# 添加撤回标志
def add_target(time_s: int) -> str:
    return f"\n(该消息将于 {time_s} s后撤回)"


def reboot():
    if platform.system() == "Windows":
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        os.execv(sys.executable, ['python3'] + sys.argv)


def get_bot_name() -> str:
    return str(random.sample(nicknames, 1)[0])


def get_avatar(uid: str):
    """
    获取头像bytes,无法获取时返回None
    """
    request = requests.get(url=avatar_base_url % uid)
    if request.status_code == 200:
        return request.content
    else:
        return None
