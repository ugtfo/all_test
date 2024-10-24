import sys
# sys.path.append('C:/project/Esenia Vinogradova/test1')
from io import StringIO
import allure
import unittest
from unittest.mock import patch
import psycopg2
from . program1 import task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9
from . db import DataAccessLayer
from tabulate import tabulate
import uuid
import logging


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
                logging.FileHandler("test_log_integration.log", encoding="utf-8"),  # Лог в файл
                logging.StreamHandler(sys.stdout)  # Лог в консоль (stdout)
            ]
        )
        # cls.logger = logging.getLogger(__name__)
        # cls.logger.info("Настройка тестов E2E началась")
        # # Создание подключения к PostgreSQL
        # cls.connection = psycopg2.connect(
        #     database="bob1",  # Соединяемся с основной базой данных
        #     user="postgres",
        #     password="12345",
        #     host="localhost",
        #     port="5432"
        # )
        # cls.connection.autocommit = True

    # @classmethod
    # def tearDownClass(cls):
    #     cls.drop_test_database()  # Удаление тестовой базы данных
    #     if cls.connection:
    #         cls.connection.close()  # Закрытие соединения

    # @classmethod
    # def drop_test_database(cls):
    #     with cls.connection.cursor() as cur:
    #         cur.execute("DROP DATABASE IF EXISTS test_db")

    def setUp(self):
        self.dal = DataAccessLayer()
        self.dal.create_tables()  # Создание таблиц
        self.connection = self.dal.connection
        self.connection.autocommit = False  # Отключение автокоммита
        self.clear_tables()  # Очистка таблиц перед каждым тестом
        self.unique_login = self.insert_test_data()  # Вставка тестовых данных
        self.logger.info("Тестовая среда настроена.")

    def clear_tables(self):
        with self.connection.cursor() as cur:
            cur.execute("DELETE FROM coursework.vouchers")
            cur.execute("DELETE FROM coursework.visitors")
            cur.execute("DELETE FROM coursework.price_list")
            cur.execute("DELETE FROM coursework.accounts")

    def tearDown(self):
        self.connection.rollback()  # Откат изменений после каждого теста

    def insert_test_data(self):
        unique_login = f'ivanov_{uuid.uuid4()}'[:20]
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
        
        self.dal.insert('coursework.visitors', ticket_num='1', residence='Москва', login=unique_login)
        self.dal.insert('coursework.price_list', 
                        ground_name='ИмяСубъекта', 
                        price=100,  
                        picture='example_picture.jpg', 
                        is_relevant=True)
        self.dal.insert('coursework.vouchers', 
                        days=5,  
                        pictures=3,  
                        status='ждет',  
                        id_visitor='1',  
                        price=100,
                        login=unique_login,
                        id_pricelist=1)

        return unique_login
    @allure.step("Проверка работы task_1_i")
    def test_task_1_i(self):
        self.logger.info("Начинается тест test_task_1_i")
        with patch('builtins.input', side_effect=['Иванов', 'Иван', 'Иванович']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                task_1()

        output = mock_stdout.getvalue()
        self.logger.info(f"Вывод test_task_1_i: {output}")

        self.assertIn('Иванов', output)
        self.assertIn('Иван', output)
        self.assertIn('Иванович', output)
        self.logger.info("Тест test_task_1_e2e завершен успешно")
        
    @allure.step("Проверка работы task_2_i")
    def test_task_2_i(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            task_2()
            output = mock_stdout.getvalue()
            self.assertIn('Иванов', output)
            self.assertIn('Иван', output)
            self.assertIn('Иванович', output)

    @allure.step("Проверка работы task_3_i")
    def test_task_3_i(self):
        result = task_3(self.unique_login)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

    @allure.step("Проверка работы task_4_i")
    @patch('builtins.input', side_effect=['Москва', 5, 3, 1])
    def test_task_4_i(self, mock_input):
        login = self.unique_login
        task_4(login, self.connection)

        visitors = self.dal.select('coursework.visitors', order_by='ticket_num', limit=1)
        vouchers = self.dal.select('coursework.vouchers', order_by='id', limit=1)

        self.assertGreater(len(visitors), 0, "Visitor data not inserted")
        self.assertGreater(len(vouchers), 0, "Voucher data not inserted")
        self.assertEqual(visitors[0]['login'], login, "Login mismatch in visitors")
        self.assertEqual(visitors[0]['residence'], 'Москва', "Residence mismatch")
        self.assertEqual(vouchers[0]['days'], 5, "Days mismatch in vouchers")
        self.assertEqual(vouchers[0]['pictures'], 3, "Pictures mismatch")
        self.assertEqual(vouchers[0]['status'], 'ждет', "Status mismatch")

    def insert_voucher_data(self, ticket_num):
        self.dal.insert('coursework.vouchers', 
                        days=5, 
                        pictures=3, 
                        status='ждет', 
                        id_visitor=ticket_num, 
                        price=100,
                        login=self.unique_login,
                        id_pricelist=1)

        voucher = self.dal.select('coursework.vouchers', order_by='id DESC', limit=1)
        if voucher:
            return voucher[0]['id']
        else:
            raise Exception("Не удалось получить добавленный ваучер")
        
    @allure.step("Проверка работы task_5_i")
    @patch('builtins.input', side_effect=['1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_task_5_i(self, mock_stdout, mock_input):
        self.logger.info("Starting test_task_5_i")
        
        self.dal.insert('coursework.visitors', ticket_num='1', residence='Москва', login='ivanov123')
        voucher_id = self.insert_voucher_data('1')

        self.dal.delete_visitor(1)

        deleted_voucher = self.dal.select('coursework.vouchers', id=voucher_id)
        self.assertEqual(len(deleted_voucher), 0, f"Запись с id {voucher_id} не была удалена")
        self.logger.info(f"Voucher with id {voucher_id} has been deleted successfully.")

        deleted_visitor = self.dal.select('coursework.visitors', id=1)
        self.assertEqual(len(deleted_visitor), 0, "Запись с id 1 не была удалена из visitors")
        self.logger.info("Visitor with id 1 has been deleted successfully.")


    @allure.step("Проверка работы task_6_i")
    @patch('builtins.input', side_effect=['ИмяСубъекта'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_task_6_i(self, mock_stdout, mock_input):
        self.dal.delete_all_from_price_list()
        self.dal.insert('coursework.price_list', ground_name='ИмяСубъекта', price=100, picture='example_picture.jpg', description='Описание', is_relevant=True)
        
        all_data = self.dal.select('coursework.price_list')
        print(f"Все данные в price_list: {all_data}")

        # Получаем вывод функции
        output = task_6()  # Теперь функция возвращает значение

        # Извлечение вывода из mock_stdout
        printed_output = mock_stdout.getvalue()

        # Форматирование вывода в виде таблицы
        table_data = [
            ['Вывод функции', output],
            ['Вывод из print', printed_output.strip()]
        ]
        table = tabulate(table_data, headers=['Описание', 'Значение'], tablefmt='grid')
        print(table)  # Вывод таблицы

        # Проверки
        self.assertIsNotNone(output)  # Убедитесь, что output не None
        self.assertIn("Все данные в price_list", printed_output)  # Проверьте, что 'Все данные' выведены
        self.assertIn("Описание", printed_output)  # Проверяем наличие 'Описание'
        self.assertIn("100", printed_output)  # Проверяем наличие '100'


    @allure.step("Проверка работы task_7_i")
    @patch('builtins.input', side_effect=['1'])  # Имитация ввода id выставки
    @patch('sys.stdout', new_callable=StringIO)  # Перенаправление вывода в StringIO
    def test_task_7_i(self, mock_stdout, mock_input):
        task_7()
        output = mock_stdout.getvalue()

        self.assertIn('ждет', output)
        self.assertIn('100', output)

    @patch('builtins.input', side_effect=['999'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_task_7_i_invalid_id(self, mock_stdout, mock_input):
        task_7()
        output = mock_stdout.getvalue()
        self.assertIn('Запись с id=999 не найдена.', output)

    @allure.step("Проверка работы task_8_i")
    @allure.step("Проверка работы task_8_i")    
    def test_task_8_i(self):
        self.logger.info("Начинается тест test_task_8_i")
        # Подставляем тестовый id
        test_id = 1
        # Добавляем необходимые данные в таблицу перед запуском функции
        self.insert_test_data()  # Убедитесь, что данные вставлены

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect=[str(test_id)]):  # Подставляем id
                task_8()  # Вызов функции
            output = mock_stdout.getvalue()  # Получаем вывод функции

            # Проверяем, что функция запрашивает ввод
            self.assertIn("Введите id выставки (от 1 до 100):", output) 
            
            # Проверяем, что выводимое сообщение верно
            self.assertIn(f"Запись с id={test_id} не найдена.", output) 
       
       
    @allure.step("Проверка работы task_9_i")            
    @patch('builtins.input', side_effect=['1'])  # Имитация ввода id ваучера
    @patch('sys.stdout', new_callable=StringIO)  # Перенаправление вывода в StringIO
    def test_task_9_update_voucher_status(self, mock_stdout, mock_input):
        self.logger.info("Начинается тест test_task_9_update_voucher_status")

        # Подставляем необходимые данные в таблицу перед запуском функции
        self.dal.insert('coursework.vouchers', 
                        days=5, 
                        pictures=3, 
                        status='ждет', 
                        id_visitor='1', 
                        price=100,
                        login=self.unique_login,
                        id_pricelist=1)
        
        # Получаем ID последнего вставленного ваучера
        voucher_id = self.dal.select('coursework.vouchers', order_by='id DESC', limit=1)[0]['id']

        # Имитация ввода ID ваучера
        with patch('builtins.input', side_effect=[str(voucher_id)]):
            task_9()  # Вызов функции

        # Проверяем, что статус ваучера обновился
        updated_voucher = self.dal.select('coursework.vouchers', id=voucher_id)
        self.assertEqual(updated_voucher[0]['status'], 'одобрен', "Статус ваучера не обновлён корректно")

        # Проверяем вывод функции
        output = mock_stdout.getvalue()
        self.assertNotIn('Traceback', output)  # Убедитесь, что ошибок не было
        self.logger.info("Тест test_task_9_update_voucher_status завершен успешно")

if __name__ == "__main__":
    unittest.main()
