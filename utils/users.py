"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/3/31 20:08
"""
import datetime

from typing import Union
from utils import database_mysql, const
from utils.permission import permission_
from nonebot import logger, get_driver, require
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.permission import Permission


ftr: str = "%Y-%m-%d"
cursor = database_mysql.cursor
db = database_mysql.connect
superusers = get_driver().config.superusers


async def is_user_exist(gid: str, uid: str):
    cursor.execute(f"SELECT * FROM users WHERE gid='{gid}' AND uid='{uid}';")
    re = cursor.fetchone()
    if re:
        return True
    return False


async def user_init_one(gid: str, uid: str, role: str = "member", ban_count: int = 0, alive: bool = True):
    if await is_user_exist(gid, uid):
        cursor.execute(f"UPDATE users SET alive=TRUE WHERE gid='{gid}' AND uid='{uid}';")
    else:
        cursor.execute(f"INSERT INTO users VALUES('{gid}', '{uid}', '{role}', '{ban_count}', {alive});")


async def user_init_all(member_list: list):
    for member in member_list:
        gid = str(member['group_id'])
        uid = str(member['user_id'])
        if uid in superusers:
            role = "Van"
        else:
            role = member['role']
        await user_init_one(gid, uid, role)


def get_role(gid: str, uid: str) -> str:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND gid='{gid}'")
    re = cursor.fetchone()
    if re:
        return re[0]


def update_role(gid: str, uid: str, role: str) -> bool:
    try:
        cursor.execute(f"UPDATE users SET role='{role}' WHERE uid='{uid}' AND gid='{gid}';")
    except:
        return False
    logger.info(f"更新用户 {uid} 权限 {role}")
    return True


def update_role_with_check(gid: str, uid: str, role: str) -> bool:
    """
    进行检查的权限更新, 当新权限等级低于旧权限等级时不修改
    """
    try:
        if permission_('admin', get_role(gid, uid)):
            update_role(gid, uid, role)
        else:
            return False
    except:
        return False
    return True


def get_countAll(gid, uid) -> int:
    cursor.execute(f"SELECT count_all FROM sign WHERE uid='{uid}' AND gid='{gid}';")
    re = cursor.fetchone()
    if re:
        return re[0]
    return 0


def get_countContinue(gid, uid) -> int:
    cursor.execute(f"SELECT count_continue FROM sign WHERE uid='{uid}' AND gid='{gid}';")
    re = cursor.fetchone()
    if re:
        return re[0]
    return 0


def get_dateLast(gid, uid) -> str:
    cursor.execute(f"SELECT date_last FROM sign WHERE uid='{uid}' AND gid='{gid}';")
    re = cursor.fetchone()
    if re:
        return datetime.datetime.strftime(re[0], ftr)


def update_countAll(gid: str, uid: str, count_all: int) -> bool:
    cursor.execute(f"UPDATE sign SET count_all={count_all} WHERE uid='{uid}' AND gid='{gid}';")
    cursor.fetchone()
    return cursor.rowcount > 0


def update_countContinue(gid: str, uid: str, count_continue: int) -> bool:
    cursor.execute(f"UPDATE sign SET count_continue={count_continue} WHERE uid='{uid}' AND gid='{gid}';")
    cursor.fetchone()
    return cursor.rowcount > 0


def update_dateLast(gid: str, uid: str, date_last: Union[datetime.datetime, str]) -> bool:
    if type(date_last) is datetime.datetime:
        date_last = date_last.strftime(const.DATE_FORMAT_STR)
    else:
        datetime.datetime.strptime(date_last, const.DATE_FORMAT_STR)
    cursor.execute(f"UPDATE sign SET date_last='{date_last}' WHERE uid='{uid}' AND gid='{gid}';")
    cursor.fetchone()
    return cursor.rowcount > 0


def get_credit(gid, uid) -> int:
    cursor.execute(f"SELECT credit FROM credit LEFT JOIN users ON credit.uid=users.uid AND credit.gid=users.gid WHERE alive=1 AND credit.uid='{uid}' AND credit.gid='{gid}';")
    re = cursor.fetchone()
    if re:
        return re[0]
    else:
        return -1


def set_credit(gid: str, uid: str, credit: int) -> bool:
    cursor.execute(f"UPDATE credit SET credit={credit} WHERE gid='{gid}' AND uid='{uid}';")
    cursor.fetchone()
    return cursor.rowcount > 0


def set_member_later(gid, uid, time: int):
    scheduler = require("nonebot_plugin_apscheduler").scheduler
    timezone = "Asia/Shanghai"
    date = datetime.datetime.now() + datetime.timedelta(seconds=time)
    scheduler.add_job(func=update_role, trigger="date", run_date=date, timezone=timezone, args=[str(gid), str(uid), "member"])


def get_ban_count(uid: str, gid: str) -> int:
    cursor.execute(f"SELECT ban_count FROM users WHERE gid='{gid}' and uid='{uid}';")
    count = cursor.fetchone()
    if count:
        return count[0]
    else:
        return 0


def set_ban_count(uid: str, gid: str, ban_count: int) -> int:
    cursor.execute(f"UPDATE users SET ban_count={ban_count} WHERE gid='{gid}' and uid='{uid}';")
    return cursor.rowcount > 0


def get_all_Van_in_database():
    cursor.execute("SELECT * FROM users WHERE role='Van'")
    return cursor.fetchall()


def get_all_Van_in_database_distinct():
    cursor.execute("SELECT DISTINCT uid FROM users WHERE role='Van'")
    return cursor.fetchall()


def member_leave(uid, gid):
    sql = f"UPDATE users SET role='member',alive=FALSE WHERE uid='{uid}' and gid='{gid}'"
    cursor.execute(sql)


def get_alive(uid: str, gid: str) -> bool:
    cursor.execute(f"SELECT alive FROM users WHERE gid='{gid}' and uid='{uid}';")
    re = cursor.fetchone()
    if re:
        return re[0]
    else:
        return False


def is_member(uid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND role='member';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_superuser(uid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND role='superuser';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_admin(uid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND role='admin';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_owner(uid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND role='owner';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_Van(uid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND role='Van';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_member_with_gid(uid: str, gid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND gid='{gid}' AND role='member';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_superuser_with_gid(uid: str, gid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND gid='{gid}' AND role='superuser';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_admin_with_gid(uid: str, gid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND gid='{gid}' AND role='admin';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def is_owner_with_gid(uid: str, gid: str) -> bool:
    cursor.execute(f"SELECT role FROM users WHERE uid='{uid}' AND gid='{gid}' AND role='owner';")
    re = cursor.fetchone()
    if re:
        return True
    else:
        return False


def get_members_uid_by_gid(gid: str) -> list:
    cursor.execute(f"SELECT * FROM users WHERE gid='{gid}';")
    members = cursor.fetchall()
    uid = []
    for member in members:
        uid.append(member[1])

    return uid


async def superuser_checker(event: GroupMessageEvent) -> bool:
    return is_superuser_with_gid(str(event.user_id), str(event.group_id))


async def Van_checker(event: GroupMessageEvent) -> bool:
    return is_Van(str(event.user_id))

superuser: Permission = Permission(superuser_checker)
Van: Permission = Permission(Van_checker)

