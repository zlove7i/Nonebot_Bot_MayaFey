#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.log import logger, default_format

# Custom your logger
# 
# from nonebot.log import logger, default_format
logger.add("./logs/error.log",
           rotation="1 week",
           diagnose=False,
           level="ERROR",
           format=default_format)
           
logger.add("./logs/info.log",
           rotation="1 day",
           diagnose=False,
           level="INFO",
           format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 系统自带指令
# nonebot.load_builtin_plugins("echo")


# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
