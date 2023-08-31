import sqlite3
import colorama
from colorama import Fore, Style
import json
import os

with open('v3.json', 'r') as json_file:
    data = json.load(json_file)

value = data["y"]
if value == "null":

    print(f"{Fore.RED}+—————————————————————————————————————————+ ")
    print("|您是否以有数据库                         |")
    print("|如果您已有数据库请下方输入您的数据库name |")
    print("|如果您没有数据库可以在下方输入new        |")
    print(f"+—————————————————————————————————————————+{Style.RESET_ALL}")

    Date = input("如果您已有数据库请输入您的数据库name : ")

    if Date == "new":

        conn = sqlite3.connect('new_database.db')
        cursor = conn.cursor()

        cursor.execute('''
                    CREATE TABLE day (
                    number INTEGER PRIMARY KEY AUTOINCREMENT,
                    numdays INTEGER,
                    fname TEXT,
                    lname TEXT
                    )
            ''')
        
        conn.commit()
        cursor.close()
        conn.close()

        with open('v3.json','r') as f:
            d = json.load(f)

            d['address'] = f"{Date}.db"
            d['y'] = "have"

        with open('v3.json','w') as f:
            json.dump(d, f,ensure_ascii=False)
    
    else:
        with open('v3.json','r') as f:
            d = json.load(f)

            d['address'] = f"{Date}.db"
            d['y'] = "have"

        with open('v3.json','w') as f:
            json.dump(d, f,ensure_ascii=False)

else :
    
    print(f"{Fore.GREEN}+—————————————————————————————————————————+ ")
    print("|Y是计入天数                              |")
    print("|n是计算全部人的天数                      |")
    print("|r是注册或者删除用户的全部数据            |")
    print('|k是清空全部数据进入下一个月              |')
    print(f"+—————————————————————————————————————————+{Style.RESET_ALL}")

    login = input("Y/n/r/k :")

    #计入天数
    if login.lower() == "y":
        with open('v3.json', 'r') as f:
            d = json.load(f)

        conn = sqlite3.connect(d['address'])
        cur = conn.cursor()

        while True:
            member = input("用户名 (输入 'exit' 退出): ")
            if member.lower() == 'exit':
                break  
            day = int(input("住的天数: "))
            cur.execute('SELECT * FROM day WHERE number = ?', (member,))
            result = cur.fetchone()
            if result is None:
                print("输入错误的 member 号码")
            else:
                cur.execute('UPDATE day SET numdays = numdays + ? WHERE number = ?', (day, member))
                conn.commit()
                cur.execute('SELECT * FROM day WHERE number = ?', (member,))
                result = cur.fetchone()
                print(result)

    #计算全部人的天数
    #计算电费和水费
    elif login == 'n':

        electricitybill = input("电费 : ")
        waterfee = input("水费 ： ")

        conn = sqlite3.connect("new_database.db")
        cursor = conn.cursor()

    # 执行 SQL 语句，查询 day 表中所有的 numdays 并求和
        sql = "SELECT SUM(numdays) FROM day"
        cursor.execute(sql)
        result = cursor.fetchone()

        print("The sum of all numdays in the day table is:", result[0])
        cursor.close()
        conn.close()

        conn = sqlite3.connect("new_database.db")
        cursor = conn.cursor()
    # 执行 SQL 语句，查询 day 表中的全部 numdays、fname 和 lname 值
        sql = "SELECT numdays, fname, lname FROM day"
        cursor.execute(sql)
        data_list = cursor.fetchall()

    # 关闭数据库连接
        conn.close()
        
        num1 = float(electricitybill) / float(result[0])
        num2 = float(waterfee) / float(result[0])

        print(f"{num1}  {num2}")
    # 计算每个 numdays 值乘以 num1 和 num2 的结果，然后打印对应的 fname 和 lname
        for idx, data in enumerate(data_list, start=1):
            numdays, fname, lname = data
            result1 = numdays * num1
            result2 = numdays * num2
            formatted_result = "${:,.2f}".format(result1)
            formatted_result2 = "${:,.2f}".format(result2)  # 格式化为货币形式
            print(f"结果 {idx}: name={fname} {lname}, 电费={formatted_result} 水费= {formatted_result2}")

    elif login == "r":
        while True:
            print(f"{Fore.GREEN}+—————————————————————————————————————————+ ")
            print("|R :用于注册新的用户到数据库里            |")
            print("|                                         |")
            print("|D :用于删除指定用户的资料                |")
            print('|                                         |')
            print(f"+—————————————————————————————————————————+{Style.RESET_ALL}")
            rd = input("请输入R或者D进行操作 ：")
            if rd == "r":
                numdays = 0
                fname = input("请输入 fname 的值：")
                lname = input("请输入 lname 的值：")

        # 连接到数据库
                conn = sqlite3.connect("new_database.db")
                cursor = conn.cursor()

        # 执行 SQL 语句，插入新记录到 day 表
                sql = "INSERT INTO day (numdays, fname, lname) VALUES (?, ?, ?)"
                cursor.execute(sql, (numdays, fname, lname))
                conn.commit()

                print(f"{Fore.GREEN}新记录已成功插入到 day 表。{Style.RESET_ALL}")

            # 关闭数据库连接
                conn.close()

                member2 = input("按Enter继续操作 (输入 'exit' 退出): ")
                if member2.lower() == 'exit':
                    break  



            elif rd == "d":
                while True:
                    # 获取要删除的记录的 fname 和 lname 值
                    lname_to_delete = input("请输入要删除的记录的 lname 值：")

                    # 连接到数据库
                    conn = sqlite3.connect("new_database.db")
                    cursor = conn.cursor()

                    # 执行 SQL 语句，删除 day 表中符合条件的记录
                    sql = "DELETE FROM day WHERE lname = ?"
                    cursor.execute(sql, (lname_to_delete))
                    conn.commit()

                    print(f"{Fore.RED}指定记录已成功从 day 表中删除。{Style.RESET_ALL}")

                    # 关闭数据库连接
                    conn.close()

                    conn = sqlite3.connect("new_database.db")
                    cursor = conn.cursor()

                    # 执行 SQL 语句，查询 day 表中的全部数据
                    sql = "SELECT * FROM day"
                    cursor.execute(sql)
                    data_list = cursor.fetchall()

                    # 关闭数据库连接
                    conn.close()

                    # 打印 day 表中的全部数据
                    for idx, data in enumerate(data_list, start=1):
                        print(f"{data}")

                    
                    member2 = input("按Enter继续操作 (输入 'exit' 退出): ")
                    if member2.lower() == 'exit':
                        break  

    elif login == 'k':
        
        import sqlite3
        
        # 连接到数据库
        conn = sqlite3.connect("new_database.db")
        cursor = conn.cursor()
        
        # 执行 SQL 语句，查询 day 表中的全部数据
        sql_select = "SELECT * FROM day"
        cursor.execute(sql_select)
        data_list = cursor.fetchall()
        
        # 关闭数据库连接
        conn.close()
        
        # 将查询到的数据保存到文本文件
        with open("day_data_before_update.txt", "w") as f:
            for idx, data in enumerate(data_list, start=1):
                number, numdays, fname, lname = data[:4]
                f.write(f"记录 {idx}: numdays={numdays}, name={fname} {lname}\n")
        
        # 重新连接到数据库
        conn = sqlite3.connect("new_database.db")
        cursor = conn.cursor()
        
        # 执行 SQL 语句，更新 day 表中的所有 numdays 值为 0
        sql_update = "UPDATE day SET numdays = 0"
        cursor.execute(sql_update)
        conn.commit()
        
        print("day 表中的所有 numdays 值已更新为 0。")
        
        # 关闭数据库连接
        conn.close()
    



