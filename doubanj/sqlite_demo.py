import sqlite3
# from util import connection

"""
下面是 python 操作 sqlite 数据库的范例代码
注意，代码上课会讲，你不用看懂，也不用运行
"""


def create(conn):
    sql_create = '''
    CREATE TABLE `users` (
        `id`        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `username`  TEXT NOT NULL UNIQUE,
        `password`  TEXT NOT NULL,
        `email`     TEXT
    )
    '''
    # 用 execute 执行一条 sql 语句
    conn.execute(sql_create)
    print('创建成功')


def insert(conn, username, password, email):
    sql_insert = '''
    INSERT INTO
        `users`(`username`,`password`,`email`)
    VALUES
        (?, ?, ?);
    '''
    # sql_insert = '''
    #     INSERT INTO
    #         `users`(`username`,`password`,`email`)
    #     VALUES
    # '''
    # sql_insert + '({}, {}, {})'.format(username, password, email)

    # 参数拼接要用 ?，execute 中的参数传递必须是一个 tuple 类型
    conn.execute(sql_insert, (username, password, email))
    print('插入数据成功')


def select(conn):
    sql = '''
    SELECT
        id, username, email
    FROM
        users
    '''
    cursor = conn.execute(sql)
    for row in cursor:
        print(row)


def select_bad(conn):
    username = "'sql1'"
    password = "'fadasdsad' OR '1'='1'"
    # password = "'' OR '1'='1'; DROP TABLE users"
    sql = '''
    SELECT 
      *
    FROM
      users
    WHERE 
      username={} AND password = {};
    '''.format(username,password)
    print('bad sql', sql)
    # SELECT * FROM users WHERE username = '' OR '1'='1';
    cursor = conn.execute(sql)
    # cursor = conn.execute(sql,(username,password,))
    for row in cursor:
        print(row)


def delete(conn, user_id):
    sql_delete = '''
    DELETE FROM
        users
    WHERE
        id=?
    '''
    conn.execute(sql_delete, (user_id,))


def update(conn, user_id, email):
    """
    UPDATE
        `users`
    SET
        `email`='gua', `username`='瓜'
    WHERE
        `id`=6
    """
    sql_update = '''
    UPDATE
        `users`
    SET
        `email`=?
    WHERE
        `id`=?
    '''
    conn.execute(sql_update, (email, user_id))


def main():
    # 指定数据库名字并打开
    db_path = 'demo.sqlite'
    connection = sqlite3.connect(db_path)
    print("打开了数据库")
    # 打开数据库后 就可以用 create 函数创建表
    # create(connection)

    # 然后可以用 insert 函数插入数据
    # insert(connection, 'sql2', '1234', 'a@b.c')

    # 可以用 delete 函数删除数据
    #delete(connection, 3)

    # 可以用 update 函数更新数据
    # update(connection, 2, 'skchang08@126.com')

    # select 函数查询数据
    # select(connection)
    select_bad(connection)
    # 必须用 commit 函数提交你的修改
    # 否则你的修改不会被写入数据库
    connection.commit()
    # 用完数据库要关闭
    connection.close()


if __name__ == '__main__':
    main()
