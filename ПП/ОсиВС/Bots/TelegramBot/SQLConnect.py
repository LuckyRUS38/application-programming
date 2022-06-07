import pymysql
import cfg
import random


def get_con():
    con = pymysql.connect(
        host=cfg.db_host,
        user=cfg.db_user,
        password=cfg.db_pass,
        database=cfg.db_name
    )
    return con


def get_user_step(telegram_id):
    con = get_con()
    sql = "SELECT `step` FROM `users` WHERE `telegram_id` = '%s';" % telegram_id
    with con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


def get_users_pictures_qty(telegram_id):
    con = get_con()
    sql = "SELECT `pictures` FROM `users` WHERE `telegram_id` = '%s';" % telegram_id
    with con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


def is_user_exists(telegram_id):
    con = get_con()
    sql = "SELECT COUNT(*) FROM `users` WHERE `telegram_id` = '%s';" % telegram_id
    with con:
        cur = con.cursor()
        cur.execute(sql)
        qty = cur.fetchone()[0]
        if qty == 0:
            return False
        return True


def add_user(telegram_id, step, pictures_qty):
    con = get_con()
    sql = "INSERT INTO `users`(`telegram_id`, `step`, `pictures`)" \
          "VALUES('%s','%s','%s')" % (telegram_id, step, pictures_qty)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


def change_step(telegram_id, step):
    con = get_con()
    sql = "UPDATE `users` SET `step` = '%s' WHERE `telegram_id` = '%s';" \
          % (step, telegram_id)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


def change_pictures_qty(telegram_id, pictures_qty):
    con = get_con()
    sql = "UPDATE `users` SET `pictures` = '%s' WHERE `telegram_id` = '%s';" \
          % (pictures_qty, telegram_id)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


def change_name(telegram_id, name):
    con = get_con()
    sql = "UPDATE `users` SET `name` = '%s' WHERE `telegram_id` = '%s'" \
          % (name, telegram_id)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


# SQL  TABLE  PICTURES


def add_new_filo(telegram_id, color, path):
    con = get_con()
    sql = "INSERT INTO `pictures`(`owner`, `color`, `path`)" \
          " VALUES('%s', '%s', '%s');" % (telegram_id, color, path)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


def get_photos(qty, color='', full_info=False):
    con = get_con()
    sql_add = ""
    if full_info:
        sql_add = ",`owner`, `color`"
    if color == '':
        sql = "SELECT `path`%s FROM `pictures`;" % sql_add
    else:
        sql = "SELECT `path`%s FROM `pictures` WHERE `color` = '%s'" \
              % (sql_add, color)
    photos = []
    photo_to_send = []
    with con:
        cur = con.cursor()
        cur.execute(sql)
        photos = list(cur.fetchall())

    while qty > 0 and len(photos) > 0:
        if len(photos) == 1:
            photo_to_send.append(photos[0])
            photos.pop(0)
            break
        random_index = random.randint(0, len(photos) - 1)
        photo_to_send.append(photos[random_index])
        photos.pop(random_index)
        qty -= 1

    return photo_to_send
