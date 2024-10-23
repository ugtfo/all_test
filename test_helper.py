class AccountBuilder:
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

    def build(self):
        return self.data


class ObjectMother:
    @staticmethod
    def create_artist_account():
        return {
    
            'firstname': 'Vincen',
            'email': 'vincent@art.com',
      
            'type_role': 'artist'
        }

    @staticmethod
    def create_admin_account():
        return {
         
            'firstname': 'Admin',
            'email': 'admin@admin.com',
          
            'type_role': 'admin'
        }

    @staticmethod
    def create_customer_account():
        return {
     
            'firstname': 'John Doe',
            'email': 'john@customer.com',
         
            'type_role': 'customer'
        }
