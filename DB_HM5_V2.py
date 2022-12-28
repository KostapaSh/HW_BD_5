import psycopg2 as psy


#########Функция, создающая структуру БД (таблицы)####################################################
def creat_structure_bd(cur):

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Userbd(
        id SERIAL PRIMARY KEY,
        nameuser varchar(60) NOT NULL,
        subname varchar(60) NOT NULL,
        email_user varchar(60) NOT NULL);
    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Phone(
        id SERIAL PRIMARY KEY,
        Userbd_id integer NOT NULL REFERENCES Userbd (id),
        phone varchar(15));
    ''')
    print("Таблица создана", "\n")

#########Функция, основной пользовательский ввод######################################################
def data_user():
    set_data_user = []

    user_name = input("Укажите имя >>")
    if user_name != "":
        set_data_user.append(user_name)
    else:
        user_name = None
        set_data_user.append(user_name)
    subname = input("Укажите фамилию >>")
    if subname != "":
        set_data_user.append(subname)
    else:
        subname = None
        set_data_user.append(subname)
    email_user = input("Укажите email >>")
    if email_user != "":
        set_data_user.append(email_user)
    else:
        email_user = None
        set_data_user.append(email_user)
    enter_phone = str(input("Укажите номер телефонных>>"))
    if enter_phone != "":
        set_data_user.append(enter_phone)
    else:
        enter_phone = None
        set_data_user.append(enter_phone)

    return set_data_user


#########Функция, получить id пользователя в БД######################################################

def get_id_data_user(cur, get_data_user):
    user_data = get_data_user
    user_id_data = []

    if user_data[0] != None and user_data[1] != None and user_data[2] != None:
        cur.execute('''SELECT id FROM userbd WHERE nameuser=%s and subname=%s and email_user=%s;''',
                    (user_data[0], user_data[1], user_data[2]))
        get_id_user = cur.fetchone()
        user_id_data.append(get_id_user)
        user_id_data.extend(user_data)
    else:
        get_id_user = None
        user_id_data.append(get_id_user)
        user_id_data.extend(user_data)

    return user_id_data


#########Функция, позволяющая добавить нового клиента#################################################
def add_client(cur, user):
    user_data = user

    if user_data[0] == None:
        cur.execute('''INSERT INTO userbd (nameuser, subname, email_user) VALUES (%s, %s, %s) RETURNING id;''',
                    (user_data[1], user_data[2], user_data[3]))
        id_user = cur.fetchone()
        if user_data[4] != None:
            cur.execute('''INSERT INTO Phone (userbd_id, phone) VALUES (%s, %s);''',
                        (id_user, user_data[4]))

        print("Пользователь добавлен")
    else:
        print(f'Пользователь уже есть в БД >> {user_data[1]}, {user_data[2]}, {user_data[3]}')

#########Функция, позволяющая добавить телефон для существующего клиента##############################

def add_phone(cur, user):

    user_data = user

    if user_data[0] != None and user_data[4] != None:
        cur.execute('''INSERT INTO phone (userbd_id, phone) VALUES (%s, %s);''',
                    (user_data[0], user_data[4]))
        print(f'Номер: {user_data[4]} добавлен пользователю {user_data[1]}, {user_data[2]}')
    else:
        print("Пользователь не существует в БД либо номер задан не верно")


#########Функция, позволяющая изменить данные о клиенте###############################################

def change_client(cur, user):
    user_data = user
    new_user_data = []

    if user_data[0] != None:
        print("Укажите новые данные:")
        new_user_data = data_user()
        if new_user_data[0] != None:
            cur.execute('''UPDATE userbd SET nameuser=%s WHERE id=%s;''',
                        (new_user_data[0], user_data[0]))
        if new_user_data[1] != None:
            cur.execute('''UPDATE userbd SET subname=%s WHERE id=%s;''',
                        (new_user_data[1], user_data[0]))
        if new_user_data[2] != None:
            cur.execute('''UPDATE userbd SET email_user=%s WHERE id=%s;''',
                        (new_user_data[2], user_data[0]))
        if new_user_data[3] != None:
            cur.execute('''SELECT id FROM Phone WHERE phone=%s;''',
                        (new_user_data[3],))
            id_phone = cur.fetchone()
            if id_phone == None:
                cur.execute('''INSERT INTO phone (userbd_id, phone) VALUES (%s, %s);''',
                            (user_data[0], new_user_data[3]))
            else:
                print("Номер уже существует")
        print("Данные обновлены")
    else:
        print("Пользователь не существует в БД")

#########Функция, позволяющая удалить телефон для существующего клиента###############################

def delete_phone(cur, user):
    user_data = user

    if user_data[0] != None and user_data[4] != None:
        cur.execute('''SELECT id FROM Phone WHERE phone=%s and userbd_id=%s;''',
                        (user_data[4], user_data[0]))
        id_phone = cur.fetchone()
        if id_phone != None:
            cur.execute('''DELETE FROM phone WHERE id= %s;''', (id_phone))
            print(f'Номер {user_data[4]} удален')
    else:
        print("Параметры заданы не верно")

#########Функция, позволяющая удалить существующего клиента###########################################
def delete_client(cur, user):
    user_data = user
    if user_data[0] != None:
        cur.execute('''DELETE FROM phone WHERE userbd_id= %s;''', (user_data[0]))
        cur.execute('''DELETE FROM userbd WHERE id= %s;''', (user_data[0]))
        print("Пользователь удален")
    else:
        print("Пользователь не найден")

#########Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)######
def find_client(cur, user):
    user_data = user
    find_user = None

    if user_data[0] != None and user_data[1] != None and user_data[2] == None and user_data[3] == None:
        cur.execute('''SELECT userbd.nameuser, userbd.subname, userbd.email_user, phone.phone FROM userbd
                                LEFT JOIN phone ON userbd.ID = phone.USERBD_ID
                                WHERE nameuser=%s and subname=%s;''',
                    (user_data[0], user_data[1]))
        find_user = cur.fetchall()
    elif user_data[0] != None and user_data[1] != None and user_data[2] != None and user_data[3] == None:
        cur.execute('''SELECT userbd.nameuser, userbd.subname, userbd.email_user, phone.phone FROM userbd
                        LEFT JOIN phone ON userbd.ID = phone.USERBD_ID
                        WHERE nameuser=%s and subname=%s and email_user=%s;''',
                    (user_data[0], user_data[1], user_data[2]))
        find_user = cur.fetchall()
    elif user_data[0] != None and user_data[1] != None and user_data[2] == None and user_data[3] != None:
        cur.execute('''SELECT userbd.nameuser, userbd.subname, userbd.email_user, phone.phone FROM userbd
                        LEFT JOIN phone ON userbd.ID = phone.USERBD_ID
                        WHERE nameuser=%s and subname=%s and phone=%s;''',
                    (user_data[0], user_data[1], user_data[3]))
        find_user = cur.fetchall()
    elif user_data[0] != None and user_data[1] != None and user_data[2] != None and user_data[3] != None:
        cur.execute('''SELECT userbd.nameuser, userbd.subname, userbd.email_user, phone.phone FROM userbd
                                LEFT JOIN phone ON userbd.ID = phone.USERBD_ID
                                WHERE nameuser=%s and subname=%s and email_user=%s and phone=%s;''',
                    (user_data[0], user_data[1], user_data[2], user_data[3]))
        find_user = cur.fetchall()

    if find_user != None:
        for data in find_user:
            print(f'Имя: {data[0]}, Фамилия: {data[1]}, e-mail: {data[2]}, tel: {data[3]}')
    else:
        print("Пользователь не найден")

#########Функция, показать всех#########################################################################
def show_all(cur):

    all_user = []

    cur.execute('''SELECT userbd.nameuser, userbd.subname, userbd.email_user, phone.phone FROM userbd 
                LEFT JOIN phone ON userbd.ID = phone.USERBD_ID
                ORDER BY userbd.nameuser;''')
    all_user = cur.fetchall()

    for data in all_user:
        print(f'Имя: {data[0]}, Фамилия: {data[1]}, e-mail: {data[2]}, tel: {data[3]} \n')

#########Функция, удалить БД#########################################################################
def dell_bd(cur):
    cur.execute('''
    DROP TABLE IF EXISTS Phone;
    DROP TABLE IF EXISTS Userbd;
    ''')
    print("БД удалена", "\n")


if __name__ == "__main__":
    with psy.connect(database="BD_HW_5_V2", user="postgres", password="dialog") as conn:
        with conn.cursor() as curs:
            while True:
                print("Меню:")
                print(" 1 – Cоздать структуру БД (таблицы)", "\n",
                      "2 – Добавить нового клиента.", "\n",
                      "3 - Добавить телефон для существующего клиента.", "\n",
                      "4 – Изменить данные о клиенте.", "\n",
                      "5 - Удалить телефон для существующего клиента.", "\n",
                      "6 - Удалить существующего клиента.", "\n",
                      "7 - Найти клиента по его данным (имени, фамилии, email-у или телефону)", "\n",
                      "8 - Показать всех клиентов", "\n",
                      "9 - Удалить БД (таблицы)"
                     " 0 - Выход")
                operation = input('Введите команду >>', )
                print()
                if operation == '1':
                    creat_structure_bd(curs)
                    conn.commit()
                elif operation == '2':
                    add_client(curs, get_id_data_user(curs, data_user()))
                    conn.commit()
                elif operation == '3':
                    add_phone(curs, get_id_data_user(curs, data_user()))
                    conn.commit()
                elif operation == '4':
                    change_client(curs, get_id_data_user(curs, data_user()))
                    conn.commit()
                elif operation == '5':
                    delete_phone(curs, get_id_data_user(curs, data_user()))
                    conn.commit()
                elif operation == '6':
                    delete_client(curs, get_id_data_user(curs, data_user()))
                    conn.commit()
                elif operation == '7':
                    find_client(curs, data_user())
                elif operation == '8':
                    show_all(curs)
                elif operation == '9':
                    dell_bd(curs)
                    conn.commit()
                elif operation == '0':
                    print('Выход')
                    conn.close()
                    break
                else:
                    print('Такого меню нет', '\n')
