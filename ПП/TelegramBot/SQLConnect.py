import config
import pymysql
import config

con = pymysql.connect(
    host=config.db_host,
    user=config.db_user,
    password=config.db_pass,
    database=config.db_name
)

with con:
    sql = "SELECT `id`, `telegram_id`, `step`, `pictures` FROM `users`;"
    cur = con.cursor()
    cur.execute(sql)
    print(cur.fetchall())
