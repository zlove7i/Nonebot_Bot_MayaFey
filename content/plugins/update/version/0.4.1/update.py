"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/6/12 11:51
"""
import json
import shutil

import requests
import os

# 路径处理
dir_path = os.path.dirname(os.path.abspath(__file__))
dir_path = dir_path.split("\\")
dir_path.pop(-1)
dir = ""
for a in dir_path:
    dir += a + "/"
version = float(requests.get("http://cdn.shinelight.xyz/nonebot/version.html").text)
dir_source = dir
dir_last = dir_source + str(version) + "/"
dir_base = dir.replace(f"content/plugins/update/version/", "")
dir_plugin = dir_base + "content/plugins/"
dir_plugin_private = dir_base + "content/plugin_private/"
dir_utils = dir_base + "utils/"
url_base = "http://cdn.shinelight.xyz/nonebot/version/" + f"{version}/"

try:
    # 下载工具
    def download_to_plugin(path, *args):
        last = ".py"
        if args:
            last = args[0]
        with open(dir_plugin + path + last, 'w+', encoding="utf-8") as file:
            file.write(requests.get(url_base + path + last).text)


    def download_to_plugin_private(path, *args):
        last = ".py"
        if args:
            last = args[0]
        with open(dir_plugin_private + path + last, 'w+', encoding="utf-8") as file:
            file.write(requests.get(url_base + path + last).text)


    def download_to_utils(path, *args):
        last = ".py"
        if args:
            last = args[0]
        with open(dir_utils + path + last, 'w+', encoding="utf-8") as file:
            file.write(requests.get(url_base + "utils/" + path + last).text)


    # 翻译文件更新
    with open(dir_base + "config/" + "translate.json", "w+", encoding="utf-8") as file:
        file.write(requests.get("http://cdn.shinelight.xyz/nonebot/translate.json").text)
        file.close()

    # 权限文件更新
    for f in os.listdir(dir_base + "config/" + "permission/" + "common"):
        name = f.split(".")[0]
        with open(dir_base + "config/" + "permission/" + "common/" + f"{name}.json", "w+", encoding="utf-8") as file:
            file.write(requests.get("http://cdn.shinelight.xyz/nonebot/permission_common.json").text)
            file.close()

    for f in os.listdir(dir_base + "config/" + "permission/" + "special"):
        name = f.split(".")[0]
        with open(dir_base + "config/" + "permission/" + "special/" + f"{name}.json", "w+", encoding="utf-8") as file:
            file.write(requests.get("http://cdn.shinelight.xyz/nonebot/permission_special.json").text)
            file.close()

    # 不统计列表更新
    with open(dir_base + "config/" + "total/" + "unable.txt", "w+", encoding="utf-8") as file:
        file.write(requests.get("http://cdn.shinelight.xyz/nonebot/unable.txt").text)
        file.close()

    # 不可关闭列表更新
    with open(dir_base + "config/" + "control/" + "unset.txt", "w+", encoding="utf-8") as file:
        file.write(requests.get("http://cdn.shinelight.xyz/nonebot/unset.txt").text)
        file.close()

    # 更新部分
    shutil.rmtree(dir_plugin + "notices")
    os.mkdir(dir_plugin + "passive")
    download_to_plugin("passive/" + "__init__")
    download_to_plugin("passive/" + "rules")

    download_to_utils("__init__")
    download_to_utils("hook_update")

    download_to_plugin("withdraw/" + "__init__")
    # 增加部分
    os.mkdir(dir_plugin + "repeater")
    download_to_plugin("repeater/" + "__init__")

    os.mkdir(dir_plugin_private)
    with open(dir_plugin_private + "__init__.py", "w+", encoding="utf-8") as file:
        file.close()
    os.mkdir(dir_plugin_private + "execSql")
    download_to_plugin_private("execSql/" + "__init__")

    os.mkdir(dir_plugin + "saymoney")
    download_to_plugin("saymoney/" + "__init__")

    # 结束

# 异常处理
except Exception as e:
    js = {}
    with open(dir_base + "config/" + "update/" + "updating.json", "r+", encoding="utf-8") as f:
        js = json.loads(f.read())
        js["error"] = str(e)

    with open(dir_base + "config/" + "update/" + "updating.json", "w+", encoding="utf-8") as f:
        f.write(json.dumps(js))