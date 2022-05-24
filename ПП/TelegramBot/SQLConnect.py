import pymysql
import cfg


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