import random
import pymysql
import cfg


# Functions


def get_con():
    con = pymysql.connect(
        host=cfg.sql_host,
        user=cfg.sql_user,
        password=cfg.sql_pass,
        database=cfg.sql_name
    )
    return con


def add_user(telegram_id, step, days, units):
    con = get_con()
    sql = "INSERT INTO `users`(`telegram_id`, `step`, `days`, `units`)" \
          "VALUES('%s','%s','%s', '%s')" % (telegram_id, step, days, units)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


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


def get_user_step(telegram_id):
    con = get_con()
    sql = "SELECT `step` FROM `users` WHERE `telegram_id` = '%s';" % telegram_id
    with con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


def get_user_units(telegram_id):
    con = get_con()
    sql = "SELECT `units` FROM `users` WHERE `telegram_id` = '%s';" % telegram_id
    with con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


def get_user_days_qty(telegram_id):
    con = get_con()
    sql = "SELECT `days` FROM `users` WHERE `telegram_id` = '%s';" % telegram_id
    with con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


def change_step(telegram_id, step):
    con = get_con()
    sql = "UPDATE `users` SET `step` = '%s' WHERE `telegram_id` = '%s';" \
          % (step, telegram_id)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


def change_days_qty(telegram_id, days_qty):
    con = get_con()
    sql = "UPDATE `users` SET `days` = '%s' WHERE `telegram_id` = '%s';" \
          % (days_qty, telegram_id)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


def change_units_system(telegram_id, units):
    con = get_con()
    sql = "UPDATE `users` SET `units` = '%s' WHERE `telegram_id` = '%s'" \
          % (units, telegram_id)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


# SQL  TABLE  PICTURES


def add_new_file(telegram_id, color, path):
    con = get_con()
    sql = "INSERT INTO `pictures`(`owner`, `color`, `path`)" \
          " VALUES('%s', '%s', '%s');" % (telegram_id, color, path)
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()


def get_photos(qty, color=''):
    con = get_con()
    if color == '':
        sql = "SELECT `path` FROM `pictures` LIMIT %s;" \
              % qty
    else:
        sql = "SELECT `path` FROM `pictures` WHERE `color` = '%s' LIMIT %s;" \
              % (color, qty)
    photos = []
    photo_to_send = []
    with con:
        cur = con.cursor()
        cur.execute(sql)
        photos = cur.fetchall()

    while qty > 0 or len(photos) > 0:
        random_index = random.randint(0, len(photos) - 1)
        photo_to_send.append(photos[random_index])
        photos.pop(random_index)

    return photo_to_send

