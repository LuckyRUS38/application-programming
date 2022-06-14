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


def add_new_friends(friend_list):
    sql = "INSERT INTO `users`(`vk_id`, `first_name`, `second_name`, `date_of_birth`, `city`, `generation`)" \
          "VALUES "
    for friend in friend_list:
        sql_part = "(%s, '%s', '%s', '%s', '%s', %s),\n" % (
        friend['vk_id'], friend['first_name'], friend['second_name'], friend['date_of_birth'], friend['city'],
        friend['generation'])
        sql += sql_part
    sql += ";"

    con = get_con()
    with con:
        cur = con.cursor()
        cur.execute(sql)


def add_new_links(links_list):
    sql = "INSERT INTO `links`(`vk_id1`, `vk_id2`) VALUES "

    for link in links_list:
        sql_part = "(%s, %s),\n" % (link['vk_id1'], link['vk_id2'])
    con = get_con()
    with con:
        cur = con.cursor()
        cur.execute(sql)


def get_not_loaded(vk_id):
    sql = "SELECT `vk_id` FROM `users` WHERE `is_loaded` = 0 LIMIT 1"
    con = get_con()
    with con:
        cur = con.cursor()
        cur.execute(sql)
        result = cur.fetchone()[0]
        if result == 0:
            return False
        else:
            return True


def mark_is_loaded(vk_id):
    sql = "UPDATE `users` GET  `is_loaded` = 1 WHERE `vk_id` = %s" % vk_id
    con = get_con()
    with con:
        cur = con.cursor()
        cur.execute(sql)


def is_vk_id_inserted(vk_id):
    sql = "SELECT COUNT(*) FROM `users` WHERE `vk_id` = %s" % vk_id
    con = get_con()
    with con:
        cur = con.cursor()
        cur.execute(sql)
        count = cur.fetchone()[0]
        if count == 0:
            return False
        else:
            return True


def is_vk_ids_linked(vk_id1, vk_id2):
    sql = "SELECT COUNT(*) FROM `links` WHERE (`vk_id1` = %s AND `vk_id2` = %s) OR (`vk_id1` = %s OR `vk_id2` = %s)" % (vk_id1, vk_id2, vk_id1, vk_id2)
    con = get_con()
    with con:
        cur = con.cursor()
        cur.execute(sql)
        count = cur.fetchone()[0]
        if count == 0:
            return False
        else:
            return True