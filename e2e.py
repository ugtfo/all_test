import sys
import os

# Добавляем текущую директорию проекта в sys.path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from io import StringIO
import unittest
import allure
from unittest import mock
from unittest.mock import patch
import psycopg2

from . program1 import task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8  # Импортируйте необходимые компоненты вашего приложения
from . db import DataAccessLayer
from tabulate import tabulate
import uuid
import logging
import os





class TestDatabaseIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Настройка логирования
        if len(logging.getLogger().handlers) > 0:
            for handler in logging.getLogger().handlers[:]:
                logging.getLogger().removeHandler(handler)

        # Настройка логгера заново
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("test_log.log", encoding="utf-8"),  # Лог в файл
                logging.StreamHandler(sys.stdout)  # Лог в консоль (stdout)
            ]
        )
        cls.logger = logging.getLogger(__name__)
        cls.logger.info("Настройка тестов E2E началась")
        print("Настройка логирования...")
        
   
       

      
                
        # Создание подключения к PostgreSQL
        cls.connection = psycopg2.connect(
            database="testdb",  # Соединяемся с основной базой данных
            user="postgres",
            password="12345",  # Убедитесь, что здесь правильный пароль
            host="localhost",
            port="5432"
        )
    
        cls.connection.autocommit = True
    

 
    @classmethod
    def tearDownClass(cls):
        cls.drop_test_database()  # Сначала удаляем тестовую базу данных
        if cls.connection:
            cls.connection.close()  # Затем закрываем соединение
        logging.shutdown() 
            

    @classmethod
    def drop_test_database(cls):
        with cls.connection.cursor() as cur:
            # Удаление тестовой базы данных
            cur.execute("DROP DATABASE IF EXISTS test_db")

    def setUp(self):
        # Устанавливаем подключение к тестовой базе данных и открываем транзакцию
        self.dal = DataAccessLayer()
        self.dal.create_tables()  # Убедитесь, что таблицы созданы
        self.connection = self.dal.connection
        self.connection.autocommit = False  # Отключаем автокоммит для транзакций
        self.clear_tables()  # Очистка таблиц перед каждым тестом
        self.unique_login = self.insert_test_data()  # Вставка тестовых данных
        self.ticket_num = 1
        self.dal.insert('coursework.visitors', ticket_num='1', residence='Москва', login='ivanov_test')
  
    def clear_tables(self):
        with self.connection.cursor() as cur:
            cur.execute("DELETE FROM coursework.vouchers")
            cur.execute("DELETE FROM coursework.visitors")
            cur.execute("DELETE FROM coursework.price_list")
            cur.execute("DELETE FROM coursework.accounts")
        
    def tearDown(self):
        # Откат всех изменений после каждого теста
        self.connection.rollback()

    def insert_test_data(self):
        unique_login = f'ivanov_{uuid.uuid4()}'[:20]   # Генерируем уникальный логин
        self.dal.insert('coursework.accounts', 
                        login=unique_login, 
                        surname='Иванов', 
                        firstname='Иван', 
                        patronymic='Иванович', 
                        date_of_birth='1990-01-01', 
                        sex='м', 
                        mobile_phone='1234567890', 
                        email='ivanov123@example.com', 
                        type_role='художник')
        
        # Вставка данных о посетителе
        self.dal.insert('coursework.visitors', ticket_num='1', residence='Москва', login=unique_login)
        
        # Вставка данных в price_list, если она ещё не создана
        self.dal.insert('coursework.price_list', 
                 ground_name='ИмяСубъекта',  # Добавлено значение для ground_name
                 price=100,  
                 picture='example_picture.jpg', 
                 is_relevant=True)

        # Вставка данных о ваучерах
        self.dal.insert('coursework.vouchers', 
                        days=5,  
                        pictures=3,  
                        status='ждет',  
                        id_visitor='1',  
                        price=100,
                        login=unique_login,
                        id_pricelist=1)

        return unique_login  # Возвращаем уникальный логин для последующего использования
    @allure.step("Проверка работы task_1")
    def test_task_1_e2e(self):
        self.logger.info("Начинается тест test_task_1_e2e")
       
        # Имитация ввода через patch
        with patch('builtins.input', side_effect=['Иванов', 'Иван', 'Иванович']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                task_1()  # Вызов функции, которая выполняет основной сценарий

        # Получаем вывод
        output = mock_stdout.getvalue()
        self.logger.info(f"Вывод test_task_1_e2e: {output}")

        # Проверяем, что вывод содержит ожидаемую информацию
        self.assertIn('Иванов', output)
        self.assertIn('Иван', output)
        self.assertIn('Иванович', output)
        self.logger.info("Тест test_task_1_e2e завершен успешно")
        
    @allure.step("Проверка работы task2")     
    def test_task_2_e2e(self):
        # Имитируем вывод на консоль
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            task_2()  # Вызываем вашу функцию

            # Получаем вывод
            output = mock_stdout.getvalue()

            # Проверяем, что вывод содержит данные тестового художника
            self.assertIn('Иванов', output)
            self.assertIn('Иван', output)
            self.assertIn('Иванович', output)
            
    @allure.step("Проверка работы task_3")
    def test_task_3_e2e(self):
        # Здесь мы моделируем сценарий, в котором пользователь вызывает task_3
        result = task_3(self.unique_login)  # Вызов функции с логином
        self.assertIsNotNone(result)  # Проверяем, что результат не пустой
        self.assertGreater(len(result), 0)  # Проверяем, что есть хотя бы один ваучер
        
    @allure.step("Проверка работы task_4")
    @patch('builtins.input', side_effect=['Москва', 5, 3, 1])
    def test_task_4_e2e(self, mock_input):
        login = self.unique_login
        
        # Здесь мы моделируем взаимодействие пользователя с приложением
        task_4(login, self.connection)

        # Проверяем, что данные были добавлены
        visitors = self.dal.select('coursework.visitors', order_by='ticket_num', limit=1)
        vouchers = self.dal.select('coursework.vouchers', order_by='id', limit=1)

        # Проверяем, что данные были вставлены
        self.assertGreater(len(visitors), 0, "Visitor data not inserted")
        self.assertGreater(len(vouchers), 0, "Voucher data not inserted")
        self.assertEqual(visitors[0]['login'], login, "Login mismatch in visitors")
        self.assertEqual(visitors[0]['residence'], 'Москва', "Residence mismatch")
        self.assertEqual(vouchers[0]['days'], 5, "Days mismatch in vouchers")
        self.assertEqual(vouchers[0]['pictures'], 3, "Pictures mismatch")
        self.assertEqual(vouchers[0]['status'], 'ждет', "Status mismatch")

    def insert_voucher_data(self, ticket_num):  
        # Вставка данных в таблицу vouchers (без указания id)
        self.dal.insert('coursework.vouchers', 
                        days=5, 
                        pictures=3, 
                        status='ждет', 
                        id_visitor=ticket_num, 
                        price=100,
                        login=self.unique_login,
                        id_pricelist=1)
        print("Таблица создана и запись добавлена")

        # Получаем id добавленного ваучера для последующего удаления
        voucher = self.dal.select('coursework.vouchers', order_by='id DESC', limit=1)
        if voucher:  # Проверяем, что ваучер был добавлен
            print(f"Добавленный ваучер: {voucher}")  # Отладочный вывод
            return voucher[0]['id']
        else:
            raise Exception("Не удалось получить добавленный ваучер")



    @allure.step("Проверка работы task5")       
    def test_task_5_e2e(self):
        # Убедитесь, что запись была создана
        visitors_before = self.dal.select('coursework.visitors', id=1)
        self.assertEqual(len(visitors_before), 1)

        # Создаем мока для input
        mock_input = mock.patch('builtins.input', return_value='1').start()

        try:
            task_5()  # Ваша функция, которая выполняет удаление по id
        finally:
            mock_input.stop()

        # Проверяем, что запись была удалена
        visitors_after = self.dal.select('coursework.visitors', id=1)
        self.assertEqual(len(visitors_after), 0)
   


        
  

    # 6 
    @allure.step("Проверка работы task6")      
    def test_task_6_e2e(self):
        # Подготовка входных данных
        subject_name = "ИмяСубъекта"
        description = "Описание"  # Добавляем описание для теста

        # Вставляем тестовые данные для проверки
        self.dal.insert('coursework.price_list', 
                        ground_name=subject_name,  
                        price=100,  
                        description=description,  # Убедитесь, что это поле вставляется
                        picture='example_picture.jpg', 
                        is_relevant=True)

        # Имитация ввода через patch
        with patch('builtins.input', return_value=subject_name):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                output = task_6()  # Вызов функции, которая выполняет основной сценарий

        # Получаем вывод
        output = mock_stdout.getvalue()
        self.logger.info(f"Вывод test_task_6_e2e: {output}")

        # Проверяем, что вывод содержит ожидаемую информацию
        self.assertIn("Описание", output)  # Проверьте, что "Описание" присутствует в выводе
        self.assertIn("100", output)  # Проверьте, что "100" присутствует в выводе





    
   
    # 7
    @allure.step("Проверка работы task7")    
    @patch('builtins.input', side_effect=['1'])  # Имитация ввода id выставки
    @patch('sys.stdout', new_callable=StringIO)  # Перенаправление вывода в StringIO
    def test_task_7_e2e(self, mock_stdout, mock_input):
            task_7()  # Вызов функции

            # Получаем вывод
            output = mock_stdout.getvalue()

            # Проверяем, что вывод содержит ожидаемую информацию
            self.assertIn('ждет', output)  # Проверяем статус ваучера
            self.assertIn('100', output)  # Проверяем цену

    @patch('builtins.input', side_effect=['999'])  # Некорректный id выставки
    @patch('sys.stdout', new_callable=StringIO)  # Перенаправление вывода в StringIO
    def test_task_7_e2e_invalid_id(self, mock_stdout, mock_input):
            task_7()  # Вызов функции

            # Получаем вывод
            output = mock_stdout.getvalue()

            # Проверяем, что вывод сообщает о ненайденной записи
            self.assertIn('Запись с id=999 не найдена.', output)

    @patch('builtins.input', side_effect=['abc'])  # Некорректный ввод (не числовое значение)
    @patch('sys.stdout', new_callable=StringIO)  # Перенаправление вывода в StringIO
    def test_task_7_e2e_non_numeric_input(self, mock_stdout, mock_input):
            task_7()  # Вызов функции

            # Получаем вывод
            output = mock_stdout.getvalue()

            # Проверяем, что вывод сообщает об ошибке
            self.assertIn('Ошибка: Введите корректное числовое значение для id выставки.', output)



# 8
    @allure.step("Проверка работы task8")   
    def test_task_8(self):
        # Подставляем тестовый id
        test_id = 1

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect=[str(test_id)]):  # Подставляем id
                task_8()  # Вызов функции
            output = mock_stdout.getvalue()  # Получаем вывод функции

            # Проверяем, что функция запрашивает ввод
            self.assertIn("Введите id выставки (от 1 до 100):", output) 
            
            # Проверяем, что выводимое сообщение верно
            self.assertIn(f"Запись с id={test_id} не найдена.", output) 



if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=False) 
  
