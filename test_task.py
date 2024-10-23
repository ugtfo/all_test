import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
import allure
import unittest
from unittest.mock import patch
import io
from io import StringIO
from program1 import task_1, task_2, task_3, DataAccessLayer
from test_helper import ObjectMother


class TestUserInteraction(unittest.TestCase):
    @allure.feature('Data Access Layer Interaction')
    @allure.story('Successful task_1 execution')

    @patch.object(DataAccessLayer, 'select')
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


        
if __name__ == '__main__':
    unittest.main()
