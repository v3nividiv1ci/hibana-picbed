import pymysql
import mysql_opr.pool as pool


def recreate_user_account():
    conn, cursor = pool.create_conn()
    # cursor.execute("DROP TABLE IF EXISTS USER_ACCOUNT")
    sql = """CREATE TABLE IF NOT EXISTS `USER_ACCOUNT`(
        `ID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `USERNAME` VARCHAR(200) NOT NULL,
	    `PASSWORD` VARCHAR(200) NOT NULL,
        PRIMARY KEY ( `ID` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    cursor.execute(sql)
    conn.commit()
    pool.close_conn(conn, cursor)


def recreate_pic_route():
    conn, cursor = pool.create_conn()
    # cursor.execute("DROP TABLE IF EXISTS PIC_ROUTE")
    sql = """CREATE TABLE IF NOT EXISTS `PIC_ROUTE`(
        `ID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `ROUTE` VARCHAR(200) NOT NULL,
        PRIMARY KEY ( `ID` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    cursor.execute(sql)
    conn.commit()
    pool.close_conn(conn, cursor)





