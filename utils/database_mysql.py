"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/3/23 12:47
"""

from nonebot import get_driver, require
from nonebot.log import logger
from utils.path import sql_base
import pymysql


host = get_driver().config.mysql_host
port = get_driver().config.mysql_port
user = get_driver().config.mysql_user
password = get_driver().config.mysql_password
database = get_driver().config.mysql_db

connect = pymysql.connect(host=host, user=user, passwd=password, autocommit=True)
cursor = connect.cursor()


def execute_sql(path):
    results, result = "", []
    with open(path, "r", encoding="utf-8") as sqls:
        for sql in sqls.readlines():
            sql = sql.replace("\n", "").replace("\r", "").replace("{database}", database)
            if not sql.startswith("--") and not sql.endswith("--") and sql != "":
                if not sql.startswith("--"):
                    results = results + sql

        for i in results.split(";"):
            if i == "":
                pass
            elif i.startswith("/*"):
                result.append(i + ";")
            else:
                result.append(i + ";")

    for x in result:
        cursor.execute(x)


def Database_init():
    # 数据库初始化
    execute_sql(sql_base)
    cursor.execute(f"USE {database};")


try:
    cursor.execute(f"USE {database};")
    cursor.execute(f"SELECT * FROM users;")
except:
    Database_init()


scheduler = require("nonebot_plugin_apscheduler").scheduler
timezone = "Asia/Shanghai"
@scheduler.scheduled_job("interval", hours=4, timezone=timezone)
async def _():
    cursor.execute(f"USE {database};")
    cursor.execute("SELECT alive FROM users;")
    logger.info("执行防数据库断连")
