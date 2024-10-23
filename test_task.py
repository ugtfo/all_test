import sys
# sys.path.append('C:/project/Esenia Vinogradova/test1')
import pytest
import allure
import unittest
from unittest.mock import patch
import io
from io import StringIO
from . program1 import*

from . test_helper import ObjectMother



class TestUserInteraction(unittest.TestCase):
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_1 execution')

    def test_task_1_success(self, mock_select):
        mock_select.return_value = [{'surname': 'Smith', 'firstname': 'John'}]
        
        with patch('builtins.input', side_effect=['Smith', 'John', 'Doe']):
            task_1()
            mock_select.assert_called_once_with('coursework.accounts', type_role='художник', surname='Smith', firstname='John', patronymic='Doe')

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure in task_1 execution')    
    @patch.object(DataAccessLayer, 'select')
    def test_task_1_failure(self, mock_select):
        mock_select.side_effect = Exception("Database operation failed")
        
        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        with patch('builtins.input', side_effect=['Smith', 'John', 'Doe']):
            task_1()

        # Reset redirect.
        sys.stdout = sys.__stdout__

        # Check if the expected output is in the captured output
        self.assertIn("Database operation failed", captured_output.getvalue())


    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_2 execution')
    @patch.object(DataAccessLayer, 'select')
    def test_task_2_success(self, mock_select):
            mock_select.return_value = [{'surname': 'Smith', 'firstname': 'John'}]
            
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_2()

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Check if the mock was called correctly
            mock_select.assert_called_once_with('coursework.accounts', type_role='художник')

            # Verify the output
            self.assertIn('Smith', captured_output.getvalue())
            self.assertIn('John', captured_output.getvalue())
            
            
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure in task_2 execution')
    @patch.object(DataAccessLayer, 'select')
    def test_task_2_failure(self, mock_select):
        mock_select.side_effect = Exception("Database operation failed")
        
        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        task_2()

        # Reset redirect.
        sys.stdout = sys.__stdout__

        # Check if the expected output is in the captured output
        self.assertIn("Database operation failed", captured_output.getvalue())


    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_3 execution')
    @patch.object(DataAccessLayer, 'select')
    def test_task_3_success(self, mock_select):
        # Устанавливаем значение login через program1
        login = 'user@example.com'
        
        mock_select.return_value = [{'voucher_id': 1, 'discount': 20}]
        
        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        task_3()  # Вызываем task_3 через program1

        # Reset redirect.
        sys.stdout = sys.__stdout__

        # Check if the mock was called correctly
        mock_select.assert_called_once_with('coursework.vouchers', login=login)

        # Verify the output
        self.assertIn('voucher_id', captured_output.getvalue())
        self.assertIn('discount', captured_output.getvalue())

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure in task_3 execution')
    @patch.object(DataAccessLayer, 'select')
    def test_task_3_failure(self, mock_select):
        # Устанавливаем значение login через program1
        login = 'user@example.com'
        
        mock_select.side_effect = Exception("Database operation failed")
        
        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        task_3()  # Вызываем task_3 через program1

        # Reset redirect.
        sys.stdout = sys.__stdout__

        # Check if the expected output is in the captured output
        self.assertIn("Database operation failed", captured_output.getvalue())


    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_4 execution')
    @patch.object(DataAccessLayer, 'select')
    @patch.object(DataAccessLayer, 'insert')
    def test_task_4_success(self, mock_insert, mock_select):
        # Устанавливаем значение login через program1
        login = 'user@example.com'

        # Настраиваем возвращаемые значения для select
        mock_select.side_effect = [
            [{'ticket_num': 1}],  # для первого select 'coursework.visitors'
            [{'id': 1}]  # для второго select 'coursework.vouchers'
        ]

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['Москва', '10', '3', '2']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_4()  # Вызываем task_4 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что insert был вызван дважды
            self.assertEqual(mock_insert.call_count, 2)

            # Проверка первого insert
            mock_insert.assert_any_call('coursework.visitors', ticket_num='2', residence='Москва', login=login)

            # Проверка второго insert
            mock_insert.assert_any_call(
                'coursework.vouchers', 
                id='2', 
                days=10, 
                pictures=3, 
                status='ждет', 
                ticket_num='2', 
                id_price_list=2
            )

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure in task_4 execution')
    @patch.object(DataAccessLayer, 'select')
    @patch.object(DataAccessLayer, 'insert')
    def test_task_4_failure(self, mock_insert, mock_select):
        # Устанавливаем значение login через program1
        login = 'user@example.com'

        # Настраиваем select для выбрасывания ошибки
        mock_select.side_effect = Exception("Database operation failed")
        
        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['Москва', '10', '3', '2']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_4()  # Вызываем task_4 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится сообщение об ошибке
            self.assertIn("Database operation failed", captured_output.getvalue())

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_5 execution')
    @patch.object(DataAccessLayer, 'delete')
    def test_task_5_success(self, mock_delete):
        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['12345', '1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_5()  # Вызываем task_5 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что delete был вызван дважды
            self.assertEqual(mock_delete.call_count, 2)

            # Проверка первого delete вызова для 'vouchers'
            mock_delete.assert_any_call('coursework.vouchers', 'id', 1)

            # Проверка второго delete вызова для 'visitors'
            mock_delete.assert_any_call('coursework.visitors', 'ticket_num', '12345')

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure task_5 execution')
    @patch.object(DataAccessLayer, 'delete')
    def test_task_5_failure(self, mock_delete):
        # Настраиваем delete для выбрасывания ошибки
        mock_delete.side_effect = Exception("Database operation failed")
        
        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['12345', '1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_5()  # Вызываем task_5 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится сообщение об ошибке
            self.assertIn("Database operation failed", captured_output.getvalue())
     
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success task_6 execution')       
    @patch.object(DataAccessLayer, 'select')
    def test_task_6_success(self, mock_select):
        # Настраиваем возвращаемое значение для select
        mock_select.return_value = [
            {'price': 100, 'ground_name': 'Москва'},
            {'price': 200, 'ground_name': 'Санкт-Петербург'}
        ]

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['Москва']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_6()  # Вызываем task_6 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что select был вызван с правильными аргументами
            mock_select.assert_called_once_with('coursework.price_list', ground_name='Москва')

            # Проверка, что результат вывода корректен
            self.assertIn('Москва', captured_output.getvalue())
            self.assertIn('100', captured_output.getvalue())

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failur task_6 execution') 
    @patch.object(DataAccessLayer, 'select')
    def test_task_6_failure(self, mock_select):
        # Настраиваем select для выбрасывания ошибки
        mock_select.side_effect = Exception("Database operation failed")

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['Москва']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_6()  # Вызываем task_6 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится сообщение об ошибке
            self.assertIn("Database operation failed", captured_output.getvalue())

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success task_7 execution')     
    @patch.object(DataAccessLayer, 'select')
    def test_task_7_success(self, mock_select):
        # Настраиваем возвращаемое значение для select
        mock_select.return_value = [
            {'id': 1, 'days': 5, 'pictures': 10, 'status': 'ждет'}
        ]

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_7()  # Вызываем task_7 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что select был вызван с правильными аргументами
            mock_select.assert_called_once_with('coursework.vouchers', id=1)

            # Проверка, что результат вывода корректен
            self.assertIn('1', captured_output.getvalue())
            self.assertIn('ждет', captured_output.getvalue())

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure task_7 execution') 
    @patch.object(DataAccessLayer, 'select')
    def test_task_7_failure(self, mock_select):
        # Настраиваем select для выбрасывания ошибки
        mock_select.side_effect = Exception("Database operation failed")

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_7()  # Вызываем task_7 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится сообщение об ошибке
            self.assertIn("Database operation failed", captured_output.getvalue())
            
            
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Invalid_inpu task_7 execution')             
    def test_task_7_invalid_input(self):
        # Патчим input для имитации некорректного ввода (например, не число)
        with patch('builtins.input', side_effect=['abc']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_7()  # Вызываем task_7 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится ошибка приведения типов (ValueError)
            self.assertIn("invalid literal for int()", captured_output.getvalue())
            
     # 8
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success task_8 execution') 
    @patch.object(DataAccessLayer, 'select')
    def test_task_8_success(self, mock_select):
        # Настраиваем возвращаемое значение для select
        mock_select.return_value = [
            {'id': 1, 'days': 5, 'pictures': 10, 'status': 'ждет', 'is_relevant': 'true'}
        ]

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_8()  # Вызываем task_8 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что select был вызван с правильными аргументами
            mock_select.assert_called_once_with('coursework.vouchers', id=1, is_relevant='true')

            # Проверка, что результат вывода корректен
            self.assertIn('1', captured_output.getvalue())
            self.assertIn('ждет', captured_output.getvalue())
            self.assertIn('true', captured_output.getvalue())
            
            
    @allure.feature('Data Access Layer Interaction')
    @allure.story('invalid_input task_8 execution')             
    def test_task_8_invalid_input(self):
        # Патчим input для имитации некорректного ввода (например, не число)
        with patch('builtins.input', side_effect=['abc']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_8()  # Вызываем task_8 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится ошибка приведения типов (ValueError)
            self.assertIn("invalid literal for int()", captured_output.getvalue())
            
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure task_8 execution')     
    @patch.object(DataAccessLayer, 'select')
    def test_task_8_failure(self, mock_select):
        # Настраиваем select для выбрасывания ошибки
        mock_select.side_effect = Exception("Database operation failed")

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_8()  # Вызываем task_8 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится сообщение об ошибке
            self.assertIn("Database operation failed", captured_output.getvalue())
            
    #9
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success task_9 execution') 
    @patch.object(DataAccessLayer, 'update')
    def test_task_9_success(self, mock_update):
        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_9()  # Вызываем task_9 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что update был вызван с правильными аргументами
            mock_update.assert_called_once_with('coursework.vouchers', status='одобрен', id=1)

            # Проверяем, что нет ошибок в выводе
            self.assertNotIn("Exception", captured_output.getvalue())
            
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure task_8 execution') 
    @patch.object(DataAccessLayer, 'update')
    def test_task_9_failure(self, mock_update):
        # Настраиваем update для выбрасывания ошибки
        mock_update.side_effect = Exception("Database operation failed")

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_9()  # Вызываем task_9 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится сообщение об ошибке
            self.assertIn("Database operation failed", captured_output.getvalue())
    
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Invalid_input task_8 execution')         
    def test_task_9_invalid_input(self):
        # Патчим input для имитации некорректного ввода (например, буквы вместо числа)
        with patch('builtins.input', side_effect=['abc']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_9()  # Вызываем task_9 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится ошибка приведения типов (ValueError)
            self.assertIn("invalid literal for int()", captured_output.getvalue())


#10
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success task_10 execution') 
    @patch.object(DataAccessLayer, 'update')
    def test_task_10_success(self, mock_update):
        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_10()  # Вызываем task_10 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что update был вызван с правильными аргументами
            mock_update.assert_called_once_with('coursework.vouchers', status='отклонен', id=1)

            # Проверяем, что нет ошибок в выводе
            self.assertNotIn("Exception", captured_output.getvalue())

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure task_10 execution') 
    @patch.object(DataAccessLayer, 'update')
    def test_task_10_failure(self, mock_update):
        # Настраиваем update для выбрасывания ошибки
        mock_update.side_effect = Exception("Database operation failed")

        # Патчим input для имитации пользовательского ввода
        with patch('builtins.input', side_effect=['1']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_10()  # Вызываем task_10 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится сообщение об ошибке
            self.assertIn("Database operation failed", captured_output.getvalue())
            
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Invalid_input task_10 execution')            
    def test_task_10_invalid_input(self):
        # Патчим input для имитации некорректного ввода (например, буквы вместо числа)
        with patch('builtins.input', side_effect=['abc']):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            task_10()  # Вызываем task_10 через program1

            # Reset redirect.
            sys.stdout = sys.__stdout__

            # Проверка, что в выводе содержится ошибка приведения типов (ValueError)
            self.assertIn("invalid literal for int()", captured_output.getvalue())
            
#11
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success task_11 execution') 
    @patch('builtins.input', side_effect=[1])  # Мокаем ввод пользователя
    @patch('dal.select')  # Мокаем вызов dal.select
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод для проверки вывода
    def test_task_11_success(self, mock_stdout, mock_select, mock_input):
        # Данные, которые должны быть возвращены при вызове dal.select
        mock_result = [
            {
                'surname': 'Doe',
                'firstname': 'Jane',
                'patronymic': 'N/A',
                'mobile_phone': '123-456-7890',
                'email': 'jane.doe@example.com'
            }
        ]
        mock_select.return_value = mock_result

        # Ожидаемый вывод в формате 'plain'
        expected_output = tabulate(mock_result, headers='keys', tablefmt='plain') + '\n'

        # Запускаем функцию
        task_11()

        # Получаем вывод
        output = mock_stdout.getvalue()
    
        # Проверяем, что вывод совпадает с ожидаемым
        self.assertEqual(output, expected_output)

        # Проверяем, что dal.select был вызван с правильными аргументами
        mock_select.assert_called_once_with(
            'coursework.accounts',
            ticket_num=1,
            join=('coursework.visitors', 'coursework.visitors.login = coursework.accounts.login'),
            fields=['surname', 'firstname', 'patronymic', 'mobile_phone', 'email']
        )
        

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Invalid_ticket_number task_11 execution') 
    @patch('builtins.input', side_effect=['invalid_ticket'])  # Мокаем ввод не числа
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_11_invalid_ticket_number(self, mock_stdout, mock_input):
        # Запускаем функцию
        task_11()

        # Получаем вывод
        output = mock_stdout.getvalue()

        # Ожидаемое сообщение об ошибке
        expected_output = "Вы неправильно ввели номер билета посетителя (не целое число)\n"

        # Проверяем, что вывод совпадает с ожидаемым
        self.assertEqual(output, expected_output)
        
 
#12
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success task_12 execution') 
    @patch('builtins.input', side_effect=[1])  # Мокаем ввод пользователя
    @patch('dal.select')  # Мокаем вызов dal.select
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_12_success(self, mock_stdout, mock_select, mock_input):
        # Данные, которые должны быть возвращены при вызове dal.select
        mock_result = [
            {
                'id': 1,
                'days': 5,
                'pictures': 10,
                'status': 'ожидает',
                'ticket_num': '001',
                'id_price_list': 1001
            }
        ]
        mock_select.return_value = mock_result

        # Ожидаемый вывод в формате табличного отображения
        expected_output = tabulate(mock_result, headers='keys') + '\n'

        # Запускаем функцию
        task_12()

        # Получаем вывод
        output = mock_stdout.getvalue()

        # Проверяем, что вывод совпадает с ожидаемым
        self.assertEqual(output, expected_output)

        # Проверяем, что dal.select был вызван с правильными аргументами
        mock_select.assert_called_once_with('coursework.vouchers', id=1)
        
 
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Handle Invalid ID Input in Task 12')
    @patch('builtins.input', side_effect=['invalid_id'])  # Мокаем ввод нечислового значения
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_12_invalid_id(self, mock_stdout, mock_input):
        # Запускаем функцию
        task_12()

        # Получаем вывод
        output = mock_stdout.getvalue()

        # Ожидаемое сообщение об ошибке
        expected_output = "invalid literal for int() with base 10: 'invalid_id'\n"

        # Проверяем, что вывод совпадает с ожидаемым
        self.assertEqual(output, expected_output)
        
        #exection 
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Handle Database Error in Task 12')
    @patch('builtins.input', side_effect=[1])  # Мокаем ввод пользователя
    @patch('dal.select', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_12_database_error(self, mock_stdout, mock_select, mock_input):
        # Запускаем функцию
        task_12()

        # Получаем вывод
        output = mock_stdout.getvalue()

        # Ожидаемое сообщение об ошибке
        expected_output = "Database error\n"

        # Проверяем, что вывод совпадает с ожидаемым
        self.assertEqual(output, expected_output)
       
 
#13
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Handle success task_13')
    @patch('builtins.input', side_effect=["Москва", "5", "3", "1", "Тверская область", "ул. Тверская, д.1", "Описание выставки"])
    @patch('dal.select')  # Мокаем вызовы dal.select
    @patch('dal.insert')  # Мокаем вызовы dal.insert
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_13_success(self, mock_stdout, mock_insert, mock_select, mock_input):
        # Настраиваем результат для вызовов select
        mock_select.side_effect = [
            [{'ticket_num': 1}],  # Для select coursework.visitors
            [{'id': 1}],          # Для select coursework.vouchers
            [{'id': 1}],          # Для select coursework.sectors
        ]

        # Задаем глобальную переменную login
        login = "user_login"

        # Ожидаемый вызов функций insert с правильными аргументами
        expected_visitors_insert = {
            'ticket_num': '2', 'residence': 'Москва', 'login': 'user_login'
        }
        expected_vouchers_insert = {
            'id': '2', 'days': 5, 'pictures': 3, 'status': 'ждет рассмотрения', 'ticket_num': '2', 'id_price_list': 1
        }
        expected_artists_insert = {
            'ground_name': 'Тверская область', 'login': 'user_login'
        }
        expected_sectors_insert = {
            'id': '2', 'id_husbandry': 'Тверская область', 's_name': 'Описание выставки', 'addr': 'ул. Тверская, д.1'
        }

        # Запускаем функцию
        task_13()

        # Проверяем, что insert был вызван с правильными аргументами
        mock_insert.assert_any_call('coursework.visitors', **expected_visitors_insert)
        mock_insert.assert_any_call('coursework.vouchers', **expected_vouchers_insert)
        mock_insert.assert_any_call('coursework.artists', **expected_artists_insert)
        mock_insert.assert_any_call('coursework.sectors', **expected_sectors_insert)

    
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Failure Task 13')
    @patch('builtins.input', side_effect=["Москва", "invalid_days", "3", "1", "Тверская область", "ул. Тверская, д.1", "Описание выставки"])
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_13_invalid_input(self, mock_stdout, mock_input):
        # Запускаем функцию с некорректным вводом
        task_13()

        # Проверяем вывод об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("invalid literal for int()", output)
        #Exection 
        
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Handle Database Error in Task 13')
    @patch('builtins.input', side_effect=["Москва", "5", "3", "1", "Тверская область", "ул. Тверская, д.1", "Описание выставки"])
    @patch('dal.select', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_13_database_error(self, mock_stdout, mock_select, mock_input):
        # Задаем глобальную переменную login
        login = "user_login"

        # Запускаем функцию
        task_13()

        # Проверяем вывод об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Database error", output)

        
#14

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Success test_task_14_success')
    @patch('builtins.input', side_effect=["1"])  # Мокаем ввод
    @patch('dal.update')  # Мокаем вызов функции dal.update
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_14_success(self, mock_stdout, mock_update, mock_input):
        # Запускаем функцию
        task_14()

        # Проверяем, что dal.update был вызван с правильными аргументами
        mock_update.assert_called_once_with('coursework.vouchers', status='принята', id=1)

        # Проверяем, что функция завершилась без ошибок
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    @allure.feature('Data Access Layer Interaction')
    @allure.story('Handle Database Error in Task 14')
    @patch('builtins.input', side_effect=["invalid_id"])  # Мокаем некорректный ввод
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_14_invalid_input(self, mock_stdout, mock_input):
        # Запускаем функцию с некорректным вводом
        task_14()

        # Проверяем вывод об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("invalid literal for int()", output)   
      
        #exection 
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Handle Database Error in Task 14')
    @patch('builtins.input', side_effect=["1"])  # Мокаем ввод
    @patch('dal.update', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_14_database_error(self, mock_stdout, mock_update, mock_input):
        # Запускаем функцию
        task_14()

        # Проверяем, что выводится сообщение об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Database error", output) 
    
    # 15   
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_15_success')
    @patch('builtins.input', side_effect=["2"])  # Мокаем ввод
    @patch('dal.update')  # Мокаем вызов функции dal.update
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_15_success(self, mock_stdout, mock_update, mock_input):
        # Запускаем функцию
        task_15()

        # Проверяем, что dal.update был вызван с правильными аргументами
        mock_update.assert_called_once_with('coursework.vouchers', status='отклонена', id=2)

        # Проверяем, что функция завершилась без ошибок
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")  # Ожидаем, что функция завершится без вывода (если всё успешно)

    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_15_invalid_input') 
    @patch('builtins.input', side_effect=["invalid_id"])  # Мокаем некорректный ввод
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_15_invalid_input(self, mock_stdout, mock_input):
        # Запускаем функцию с некорректным вводом
        task_15()

        # Проверяем вывод об ошибке (ValueError для некорректного преобразования)
        output = mock_stdout.getvalue()
        self.assertIn("invalid literal for int()", output)
   #15 Exection 
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_15_database_error') 
    @patch('builtins.input', side_effect=["2"])  # Мокаем ввод
    @patch('dal.update', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_15_database_error(self, mock_stdout, mock_update, mock_input):
        # Запускаем функцию
        task_15() 
        # Проверяем, что выводится сообщение об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Database error", output)    
        
#16
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_16_success')
    @patch('builtins.input', side_effect=["test_login"])  # Мокаем ввод
    @patch('dal.delete')  # Мокаем вызов функции delete
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_16_success(self, mock_stdout, mock_delete, mock_input):
        # Настраиваем, что delete вызывается без исключений
        mock_delete.return_value = None
        
        # Запускаем task_16
        task_16()

        # Проверяем, что delete был вызван с правильными аргументами
        mock_delete.assert_called_once_with('coursework.artists', 'login', "test_login")

        # Проверяем, что никаких сообщений об ошибке не было напечатано
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_16_database_error')
    @patch('builtins.input', side_effect=["test_login"])  # Мокаем ввод
    @patch('dal.delete', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_16_database_error(self, mock_stdout, mock_delete, mock_input):
        # Запускаем функцию
        task_16()

        # Проверяем, что delete вызвал исключение и оно обработалось
        mock_delete.assert_called_once_with('coursework.artists', 'login', "test_login")

        # Проверяем, что выводится сообщение об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Database error", output)
        
 
#17
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_17_success')
    @patch('builtins.input', side_effect=["1"])  # Мокаем ввод
    @patch('dal.delete')  # Мокаем вызов функции delete
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_17_success(self, mock_stdout, mock_delete, mock_input):
        # Настраиваем, что delete вызывается без исключений
        mock_delete.return_value = None
        
        # Запускаем task_17
        task_17()

        # Проверяем, что delete был вызван с правильными аргументами
        mock_delete.assert_called_once_with('coursework.sectors', 'id', "1")

        # Проверяем, что никаких сообщений об ошибке не было напечатано
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_17_database_error')
    @patch('builtins.input', side_effect=["1"])  # Мокаем ввод
    @patch('dal.delete', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_17_database_error(self, mock_stdout, mock_delete, mock_input):
        # Запускаем функцию
        task_17()

        # Проверяем, что delete вызвал исключение и оно обработалось
        mock_delete.assert_called_once_with('coursework.sectors', 'id', "1")

        # Проверяем, что выводится сообщение об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Database error", output)
        
#18
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_18_success')
    @patch('builtins.input', side_effect=[
        "new_user", "password123", "Doe", "Jane", "Smith", 
        "2000-01-01", "М", "1234567890", "jane.doe@example.com", "user"
    ])  # Мокаем ввод пользователя
    @patch('dal.insert')  # Мокаем вызов функции insert
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_18_success(self, mock_stdout, mock_insert, mock_input):
        # Настраиваем, что insert вызывается без исключений
        mock_insert.return_value = None
        
        # Запускаем task_18
        task_18()

        # Проверяем, что insert был вызван с правильными аргументами
        mock_insert.assert_called_once_with(
            'coursework.accounts',
            login="new_user",
            salt='0',
            hashed_password="password123",
            surname="Doe",
            firstname="Jane",
            patronymic="Smith",
            date_of_birth="2000-01-01",
            sex="М",
            mobile_phone="1234567890",
            email="jane.doe@example.com",
            type_role="user"
        )

        # Проверяем, что никаких сообщений об ошибке не было напечатано
        output = mock_stdout.getvalue()
        self.assertEqual(output, "Добавление пользователя.\n")  # Проверка, что вывод корректен

    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_18_database_error')
    @patch('builtins.input', side_effect=[
        "new_user", "password123", "Doe", "Jane", "Smith", 
        "2000-01-01", "М", "1234567890", "jane.doe@example.com", "user"
    ])  # Мокаем ввод пользователя
    @patch('dal.insert', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_18_database_error(self, mock_stdout, mock_insert, mock_input):
        # Запускаем функцию
        task_18()

        # Проверяем, что insert вызвал исключение и оно обработалось
        mock_insert.assert_called_once()

        # Проверяем, что выводится сообщение об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Database error", output)
        
#19
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_19_success')
    @patch('builtins.input', side_effect=["valid_user", "valid_password"])  # Мокаем ввод пользователя
    @patch('dal.insert')  # Мокаем вызов функции insert
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_19_success(self, mock_stdout, mock_insert, mock_input):
        # Настраиваем, что insert вызывается без исключений
        mock_insert.return_value = None
        
        # Запускаем task_19
        task_19()

        # Проверяем, что insert был вызван с правильными аргументами
        mock_insert.assert_called_once_with(
            'coursework.accounts',
            login="valid_user",
            hashed_password="valid_password"
        )

        # Проверяем, что autorized установлен в True
        self.assertTrue(autorized)

        # Проверяем, что вывод соответствует ожидаемому
        output = mock_stdout.getvalue()
        self.assertIn("Пользователь valid_user авторизован.", output)
        
        
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_19_failure')
    @patch('builtins.input', side_effect=["invalid_user", "invalid_password"])  # Мокаем ввод пользователя
    @patch('dal.insert', side_effect=Exception("Invalid credentials"))  # Мокаем ошибку
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_19_failure(self, mock_stdout, mock_insert, mock_input):
        # Запускаем функцию
        task_19()

        # Проверяем, что insert вызвал исключение и оно обработалось
        mock_insert.assert_called_once()

        # Проверяем, что autorized установлен в False
        self.assertFalse(autorized)

        # Проверяем, что выводится сообщение об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Пользователь не найден, либо логин/пароль не верны.", output)
        self.assertIn("Invalid credentials", output)


#20
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_20_success')
    def test_task_20_success(self):
        # Вызываем функцию
        task_20()

        # Проверяем, что все глобальные переменные правильно инициализированы
        self.assertEqual(username, '')  # Должно быть пустым
        self.assertEqual(password, '')  # Должно быть пустым
        self.assertEqual(type_role, '')  # Должно быть пустым
        self.assertEqual(login, '')      # Должно быть пустым
        self.assertFalse(autorized)      # Должно быть False

    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_20_failure')
    @patch('login', new='invalid_login')  # Пример: меняем логин на некорректный
    def test_task_20_failure(self):
        # Изменяем переменные перед вызовом функции
        username = 'test_user'
        password = 'test_password'
        type_role = 'admin'
        login = 'test_login'
        autorized = True

        # Вызываем функцию
        task_20()

        # Проверяем, что переменные остались пустыми
        self.assertEqual(username, '')  # Должно быть пустым
        self.assertEqual(password, '')  # Должно быть пустым
        self.assertEqual(type_role, '')  # Должно быть пустым
        self.assertEqual(login, '')      # Должно быть пустым
        self.assertFalse(autorized)      # Должно быть False
    
    #21
    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_21_success')
    @patch('dal.delete')  # Мокаем метод удаления dal.delete
    @patch('builtins.input', side_effect=["test_login"])  # Мокаем ввод
    def test_task_21_success(self, mock_input, mock_delete):
        # Вызываем функцию
        task_21()

        # Проверяем, что dal.delete был вызван с правильными параметрами
        mock_delete.assert_called_once_with('coursework.sectors', 'login', "test_login")

    @allure.feature('Data Access Layer Interaction')
    @allure.story('test_task_21_failure')
    @patch('dal.delete', side_effect=Exception("Database error"))  # Мокаем ошибку базы данных
    @patch('builtins.input', side_effect=["test_login"])  # Мокаем ввод
    @patch('sys.stdout', new_callable=StringIO)  # Мокаем стандартный вывод
    def test_task_21_failure(self, mock_stdout, mock_input, mock_delete):
        # Вызываем функцию
        task_21()

        # Проверяем, что выводится сообщение об ошибке
        output = mock_stdout.getvalue()
        self.assertIn("Database error", output)
   
   
              
# задание 7
@allure.feature('Artist Account Operations')
@allure.story('Create and Retrieve Artist Account')
class ObjectMother:
    @staticmethod
    def create_artist_account():
        return {
            'surname': 'Иванов111',
            'firstname': 'Иван222',
            'patronic': 'Иванович333',
         
        }



class TestAccountOperations(unittest.TestCase):
    @patch.object(DataAccessLayer, 'select')
    @allure.step('Test task for artist account creation')
    def test_task_1_artist(self, mock_select):
        artist = ObjectMother.create_artist_account()
        mock_select.return_value = [artist]

        with patch('builtins.input', side_effect=[artist['surname'], artist['firstname'], artist['patronic']]):
            task_1()

            mock_select.assert_called_once_with(
                'coursework.accounts',
                type_role='художник',
                surname=artist['surname'],
                firstname=artist['firstname'],
                patronymic=artist['patronic']
            )
          
        
if __name__ == '__main__':
    unittest.main()
