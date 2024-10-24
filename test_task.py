import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pytest
import allure
import unittest
from unittest.mock import patch
import io
from io import StringIO
from .program1 import task_1, task_2, task_3, DataAccessLayer
from .test_helper import ObjectMother

print(sys.path) 
class TestUserInteraction(unittest.TestCase):
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_1 execution')

    @patch.object(DataAccessLayer, 'select')
    def test_task_1_success(self, mock_select):
        mock_select.return_value = [{'surname': 'Smith', 'firstname': 'John'}]
        
        with patch('builtins.input', side_effect=['Smith', 'John', 'Doe']):
            task_1()
            mock_select.assert_called_once_with('coursework.accounts', type_role='художник', surname='Smith', firstname='John', patronymic='Doe')

    @pytest.mark.test_task  # Используем маркер здесь
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

    @pytest.mark.test_task  # Используем маркер здесь
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
            
    @pytest.mark.test_task  # Используем маркер здесь           
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

    @pytest.mark.test_task  # Используем маркер здесь
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_3 execution')
    @patch.object(DataAccessLayer, 'select')
    def test_task_3_success(self, mock_select):
        login = 'user@example.com'
        mock_select.return_value = [{'voucher_id': 1, 'discount': 20}]

        result = task_3(login)  # Вызываем task_3

        # Проверяем, что mock был вызван правильно
        mock_select.assert_called_once_with('coursework.vouchers', login=login)

        # Проверяем, что возвращаемое значение содержит нужный voucher_id
        self.assertIsNotNone(result)  # Убедитесь, что результат не None
        self.assertIn({'voucher_id': 1, 'discount': 20}, result)  # Проверяем содержимое результата
        
    



        
if __name__ == '__main__':
    from db import DataAccessLayer 
