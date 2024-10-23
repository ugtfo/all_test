from multiprocessing import connection
from tabulate import tabulate
from . db import DataAccessLayer
from prettytable import PrettyTable
# User Interaction Layer
dal = DataAccessLayer()
import logging
from prettytable import PrettyTable

# Настройка логирования
logging.basicConfig(level=logging.DEBUG,  # Уровень логирования
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат вывода
                    handlers=[
                        logging.FileHandler("app.log"),  # Лог в файл
                        logging.StreamHandler()  # Лог в консоль
                    ])

logger = logging.getLogger(__name__)  # Создание логгера

def task_1():
    try:
        surname = input("Введите фамилию художника :")
        firstname = input("Введите имя художника :")
        patronymic = input("Введите отчество художника :")
        result = dal.select('coursework.accounts', type_role='художник', surname=surname, firstname=firstname, patronymic=patronymic)
        print(tabulate(result, headers='keys'))
    except Exception as e:
        print(e)
      

def task_2():
    try:
        result = dal.select('coursework.accounts', type_role='художник')
        print(tabulate(result, headers='keys'))
    except Exception as e:
        print(e)



def task_3(login):
    try:
        result = dal.select('coursework.vouchers', login=login)
        
        # Проверяем, что результат не пустой
        if result:
            return result  # Возвращаем результат для теста
        else:
            print("Нет данных для указанного логина.")
            return None
    except Exception as e:
        print(e)  # Включаем обработку ошибок
        return None
        
def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Пожалуйста, введите корректное целое число.")


def task_4(login, connection):  # Передаем connection как аргумент
    try:
        residence = input("Введите место регистрации: ")
        days = get_int_input("Введите количество дней: ")
        pictures = get_int_input("Введите количество картин: ")
        id_pricelist = get_int_input("Введите id из прайс-листа: ")

        visitors = dal.select('coursework.visitors', order_by='ticket_num', limit=1)
        ticket_num = str(int(visitors[0]['ticket_num']) + 1) if visitors else '1'

        dal.insert('coursework.visitors', ticket_num=ticket_num, residence=residence, login=login)

        vouchers = dal.select('coursework.vouchers', order_by='id', limit=1)
        voucher_id = str(int(vouchers[0]['id']) + 1) if vouchers else '1'

        dal.insert('coursework.vouchers', id=voucher_id, days=days, pictures=pictures,
                   status='ждет', ticket_num=ticket_num, id_pricelist=id_pricelist)

        connection.commit()  # Сохраняем изменения в БД
        print("Данные успешно добавлены!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        connection.rollback()  # Откат транзакции в случае ошибки

        
        
def task_5(ticket=None, ident=None):
    # Проверяем, если значение ticket не передано, запрашиваем у пользователя
    if ticket is None:
        ticket = input("Введите номер билета: ")
    
    # Обрабатываем ввод идентификатора с проверкой на ошибки
    if ident is None:
        try:
            ident = int(input("Введите id: "))
        except ValueError:
            print("Ошибка: id должно быть числом.")
            return  # Прерываем выполнение функции, если id некорректен
    
    try:
        # Удаляем записи из обеих таблиц с использованием kwargs
        dal.delete('coursework.vouchers', id=ident)
        dal.delete('coursework.visitors', ticket_num=ticket)
        
        print("Записи успешно удалены.")
    except ValueError as ve:
        print(f"Ошибка: Неверный формат для id - {ve}")  # Обработка ошибок преобразования в int
    except Exception as e:
        print(f"Ошибка: {e}")  # Обработка других исключений




# Additional tasks would follow the same pattern...

def task_6():
    try:
        X = input("Введите имя субъекта, где проводится выставка: ")
        logger.debug(f"Получено имя субъекта: {X}")

        # Получаем результаты запроса
        result = dal.select('coursework.price_list', ground_name=X)
        logger.debug(f"Результат запроса: {result}")

        if result is None or len(result) == 0:
            logger.warning("Нет результатов для данного имени субъекта.")
            print("Нет данных для отображения.")  # Добавлено для вывода в тесте
            return None

        # Применяем табуляцию с выравниванием столбцов
        formatted_result = []
        for row in result:
            description = row['description'] if row['description'] is not None else ''  # Проверка на None
            formatted_result.append({
                'id': str(row['id']).rjust(3),
                'price': str(row['price']).rjust(5),
                'description': description.ljust(20)
            })

        output = tabulate(formatted_result, headers='keys', tablefmt='plain')
        logger.info(f"Вывод функции:\n{output}")
        print(output)  # Добавлено для вывода в тесте
        return output
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        return None





        
        

import logging

def task_7():
    try:
        logging.info("Starting task_7 function")
        
        # Запрашиваем id выставки у пользователя
        X = int(input("Введите id выставки (от 1 до 100): "))
        logging.info(f"User entered id: {X}")
        
        # Выполняем запрос к таблице vouchers
        logging.info("Executing database query...")
        result = dal.select('coursework.vouchers', id=X)
        logging.info(f"Query result: {result}")
        
        # Проверка, что результат не пустой
        if result:
            logging.info("Displaying result in table format")
            # Выводим результат в виде таблицы
            print(tabulate(result, headers='keys'))
        else:
            logging.warning(f"Запись с id={X} не найдена.")
            print(f"Запись с id={X} не найдена.")
    
    except ValueError:
        logging.error("Ошибка: Введите корректное числовое значение для id выставки.")
        print("Ошибка: Введите корректное числовое значение для id выставки.")
    
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        print(f"Произошла ошибка: {e}")
    
    logging.info("Finished task_7 function")



def task_8():
    try:
        # Запрос id выставки у пользователя
        print("Введите id выставки (от 1 до 100):")  # Выводим сообщение перед вводом
        X = int(input())
        logging.info(f"Пользователь ввел id: {X}")

        # Выполняем запрос к таблице vouchers
        result = dal.select('coursework.vouchers', id=X, is_relevant='true')

        # Проверка, что результат не пустой
        if result:
            print(tabulate(result, headers='keys'))
        else:
            print(f"Запись с id={X} не найдена.")  # Сообщение, если нет записи

    except ValueError:
        print("Ошибка: Введите корректное числовое значение для id выставки.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")




def task_9():
    try:
        voucher_id = int(input("Введите id ваучера: "))
        dal.update('coursework.vouchers', 'id', voucher_id, status='одобрен')
        logging.info(f"Статус ваучера с ID {voucher_id} обновлен на 'одобрен'")
    except Exception as e:
        logging.error(f"Ошибка при обновлении статуса ваучера: {e}")

def task_10():
    try:
        X = int(input("Введите id предзаказа: "))

        dal.update('coursework.vouchers', status='отклонен', id=X)
    except Exception as e:
        print(e)


def task_11():
    try:
        # Получаем номер билета как целое число
        X = int(input("Введите номер билета посетителя: "))

        # Выполняем запрос через dal.select, передавая нужные фильтры
        result = dal.select(
            'coursework.accounts',
            ticket_num=X,
            join=('coursework.visitors', 'coursework.visitors.login = coursework.accounts.login'),
            fields=['surname', 'firstname', 'patronymic', 'mobile_phone', 'email']
        )

        # Печатаем результат в табличном формате
        print(tabulate(result, headers='keys', tablefmt='plain'))
    
    except ValueError:
        # Обрабатываем ошибку некорректного типа (не целое число)
        print("Вы неправильно ввели номер билета посетителя (не целое число)")
    
    except Exception as e:
        # Обрабатываем любые другие ошибки
        print(f"Произошла ошибка: {e}")



def task_12():
    try:
        X = int(input("ВВведите id предзаказа: "))

        result = dal.select('coursework.vouchers', id=X)
        print(tabulate(result, headers='keys'))
    except Exception as e:
        print(e)


def task_13():
    global login
    try:
        residence = input("Введите место регистрации :")
        days = int(input("Введите количество дней :"))
        pictures = int(input("Введите количество картин :"))
        id_price_list = int(input("Введите id из прайс-листа :"))

        ticket_num = str(dal.select('coursework.visitors', order_by='ticket_num', limit=1)[0]['ticket_num'] + 1)

        dal.insert('coursework.visitors', ticket_num=ticket_num, residence=residence, login=login)

        voucher_id = str(dal.select('coursework.vouchers', order_by='id', limit=1)[0]['id'] + 1)

        dal.insert('coursework.vouchers', id=voucher_id, days=days, pictures=pictures,
                   status='ждет рассмотрения', ticket_num=ticket_num, id_price_list=id_price_list)

        g_name = input("Введите название субъекта РФ :")
        addr = input("Введите дрес выставки :")
        descr = input("Введите описание выставки :")
        id = str(dal.select('coursework.sectors', order_by='id', limit=1)[0]['id'] + 1)

        dal.insert('coursework.artists', ground_name=g_name, login=login)

        dal.insert('coursework.sectors', id=id, id_husbandry=g_name, s_name=descr, addr=addr)
    except Exception as e:
        print(e)

def task_14():
    try:
        X = int(input("Введите id выставки: "))

        dal.update('coursework.vouchers', status='принята', id=X)
    except Exception as e:
        print(e)

def task_15():
    try:
        X = int(input("Введите id выставки: "))

        dal.update('coursework.vouchers', status='отклонена', id=X)
    except Exception as e:
        print(e)

def task_16():
    try:
        X = input("Введите login: ")

        dal.delete('coursework.artists', 'login', X)
    except Exception as e:
        print(e)

def task_17():
    try:
        X = input("Введите id выставки: ")

        dal.delete('coursework.sectors', 'id', X)
    except Exception as e:
        print(e)


def task_18():
    global login
    try:
        print("Добавление пользователя.")

        login = input("Введите логин нового пользователя :")
        passwrd = input("Введите пароль :")
        surname = input("Введите фамилию :")
        firstname = input("Введите имя :")
        patronymic = input("Введите отчество :")
        date_b = input("Введите дату рождения :")
        sex = input("Введите пол (М/Ж):")
        mobile_phone = input("Введите телефон :")
        email = input("Введите емайл :")
        type_role = input("Введите роль :")

        dal.insert('coursework.accounts', login=login, salt='0', hashed_password=passwrd, surname=surname, firstname=firstname, patronymic=patronymic, date_of_birth=date_b, sex=sex, mobile_phone=mobile_phone, email=email, type_role=type_role)
    except Exception as e:
        print(e)


def task_19():
    global autorized, type_role, login

    print("Авторизация пользователя.")

    login = input("Введите логин пользователя :")
    passwrd = input("Введите пароль :")
    try:
        dal.insert('coursework.accounts', login=login, hashed_password=passwrd)

        autorized = True
        print(f"Пользователь {login} авторизован.\n")
    except Exception as e:
        autorized = False
        print("Пользователь не найден, либо логин/пароль не верны.\n")
        print(e)

def task_20():
    global username, password, type_role, login, main_menu, autorized
    username = ''  # имя пользователя
    password = ''  # пароль
    type_role = ''  # роль
    login = ''
    autorized = False

def task_21():
    try:
        X = input("Введите login: ")

        dal.delete('coursework.sectors', 'login', X)
    except Exception as e:
        print(e)
        
class UserBuilder:
    def __init__(self):
        self.data = {
            'login': 'default_login',
            'hashed_password': 'default_password',
            'surname': 'Doe',
            'firstname': 'John',
            'patronymic': 'Smith',
            'date_of_birth': '2000-01-01',
            'sex': 'М',
            'mobile_phone': '1234567890',
            'email': 'john.doe@example.com',
            'type_role': 'художник'
        }

    def with_login(self, login):
        self.data['login'] = login
        return self

    def with_password(self, password):
        self.data['hashed_password'] = password
        return self

    def with_surname(self, surname):
        self.data['surname'] = surname
        return self

    def with_firstname(self, firstname):
        self.data['firstname'] = firstname
        return self

    def with_patronymic(self, patronymic):
        self.data['patronymic'] = patronymic
        return self

    def with_date_of_birth(self, date_of_birth):
        self.data['date_of_birth'] = date_of_birth
        return self

    def with_sex(self, sex):
        self.data['sex'] = sex
        return self

    def with_mobile_phone(self, mobile_phone):
        self.data['mobile_phone'] = mobile_phone
        return self

    def with_email(self, email):
        self.data['email'] = email
        return self

    def with_type_role(self, type_role):
        self.data['type_role'] = type_role
        return self

    def build(self):
        return self.data
    

class UserFactory:
    @staticmethod
    def create_artist_account():
        return UserBuilder()\
            .with_login('artist_login')\
            .with_password('artist_password')\
            .with_surname('Artist')\
            .with_firstname('Art')\
            .with_patronymic('Artistovich')\
            .with_date_of_birth('1990-01-01')\
            .with_sex('М')\
            .with_mobile_phone('1234567890')\
            .with_email('artist@example.com')\
            .with_type_role('художник')\
            .build()

    @staticmethod
    def create_admin_account():
        return UserBuilder()\
            .with_login('admin_login')\
            .with_password('admin_password')\
            .with_surname('Admin')\
            .with_firstname('Admin')\
            .with_patronymic('Adminovich')\
            .with_date_of_birth('1985-01-01')\
            .with_sex('М')\
            .with_mobile_phone('0987654321')\
            .with_email('admin@example.com')\
            .with_type_role('администратор')\
            .build()