from matplotlib import table
import psycopg2
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class AbstractTable:
    def __init__(self, connection):
        self.connection = connection

    def select(self, table_name, **kwargs):
        where_clause = ' AND '.join([f"{key} = %s" for key in kwargs.keys() if key not in ('limit', 'order_by')])
        limit_clause = ''
        
        if 'limit' in kwargs:
            limit_clause = f" LIMIT %s"
        
        # Собираем параметры, исключая 'limit' и 'order_by'
        params = tuple(kwargs[key] for key in kwargs.keys() if key not in ('limit', 'order_by'))
        
        # Если есть limit, добавляем его в параметры
        if 'limit' in kwargs:
            params += (kwargs['limit'],)
            
        query = f"SELECT * FROM {table_name}" + (f" WHERE {where_clause}" if where_clause else "") + limit_clause
        return self._execute_query(query, params)

    def insert_voucher(self, ticket_num, user_id):
        sql = "INSERT INTO coursework.vouchers (ticket_num, user_id) VALUES (%s, %s) RETURNING id;"
        try:
            with self.connection.cursor() as cur:
                cur.execute(sql, (ticket_num, user_id))
                # Получаем ID вставленной записи
                voucher_id = cur.fetchone()[0]
                self.connection.commit()  # Зафиксируем изменения
                logging.info(f"Voucher inserted with ID: {voucher_id}")  # Логируем успешную вставку
                return voucher_id
        except psycopg2.Error as e:
            self.connection.rollback()  # Откатываем изменения в случае ошибки
            logging.error(f"Error inserting voucher: {e}")
            raise  # Перебрасываем исключение для дальнейшей обработки


    def insert(self, table_name, **kwargs):
        # Убираем проверку на существование записи
        columns = ', '.join(kwargs.keys())
        values_placeholder = ', '.join(['%s'] * len(kwargs))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"
        self._execute_query(query, tuple(kwargs.values()))
    
    def update(self, table_name, where_field, where_value, **kwargs):
        set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_field} = %s"
        self._execute_query(query, (*kwargs.values(), where_value))

    def delete(self, table_name, **kwargs):
        if table_name == 'coursework.accounts':
            login = kwargs.get('login')
            # Сначала удаляем записи из artists, ссылающиеся на login
            self._execute_query("DELETE FROM coursework.artists WHERE login = %s", (login,))
        
        # Формируем часть запроса WHERE
        where_clause = ' AND '.join([f"{key} = %s" for key in kwargs.keys()])
        
        # Генерируем полный SQL-запрос
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        
        # Выполняем запрос
        self._execute_query(query, tuple(kwargs.values()))

    def delete_all(self, table_name):
        query = f"DELETE FROM {table_name}"
        self._execute_query(query, ())

    def _execute_query(self, query, params):
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, params)
                self.connection.commit()
                if query.lower().startswith("select"):
                    headers = [desc[0] for desc in cur.description]
                    return [dict(zip(headers, row)) for row in cur.fetchall()]
        except psycopg2.Error as e:
            self.connection.rollback()
            logging.error(f"Database operation failed: {e}")
            raise Exception("Database operation failed") from e

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")

# Data Access Layer
class DataAccessLayer(AbstractTable):
    def __init__(self):
        self.connection_info = {
            'database': "testdb",
            'host': "localhost",
            'user': "postgres",
            'password': "12345",
            'port': "5432"
        }
        connection = psycopg2.connect(**self.connection_info)
        super().__init__(connection)

    def execute_query(self, query, params=()):
        """ Выполняет произвольный SQL-запрос """
        return self._execute_query(query, params)
    
    def create_test_user(self, login):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO coursework.visitors (ticket_num, residence, login) VALUES (%s, %s, %s)",
                        (f'test_ticket_{login}', 'Test Residence', login))
            self.connection.commit()

    def insert_test_visitor(self, login):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO coursework.visitors (ticket_num, residence, login) VALUES (%s, %s, %s)",
                       (f'test_ticket_{login}', 'Test Residence', login))
        self.connection.commit()

    def insert_test_pricelist(self):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO coursework.price_list (id, price) VALUES (1, 100.00)")  # Пример
        self.connection.commit()

    def insert_test_voucher(self, login):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO coursework.vouchers (days, pictures, status, ticket_num, id_pricelist) VALUES (%s, %s, %s, %s, %s)",
                       (7, 3, 'active', f'test_ticket_{login}', 1))  # Пример
        self.connection.commit()

    def clear_test_data(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM coursework.vouchers WHERE ticket_num LIKE 'test_ticket_%';")
        cursor.execute("DELETE FROM coursework.visitors WHERE login = %s;", (self.login,))
        cursor.execute("DELETE FROM coursework.price_list WHERE id = 1;")  # Пример
        self.connection.commit()

    def delete_all_from_price_list(self):
        with self.connection.cursor() as cursor:
            # Сначала удаляем записи из vouchers, которые ссылаются на price_list
            cursor.execute("DELETE FROM coursework.vouchers WHERE id_pricelist IS NOT NULL;")
            # Теперь можно удалить записи из price_list
            cursor.execute("DELETE FROM coursework.price_list;")
            self.connection.commit()
        
    def delete_visitor(self, visitor_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM coursework.vouchers WHERE id_visitor = %s;", (visitor_id,))
            cursor.execute("DELETE FROM coursework.visitors WHERE id = %s;", (visitor_id,))
            self.connection.commit()
            

        
    def clear_price_list(self):
        with self.connection.cursor() as cur:
            cur.execute("DELETE FROM coursework.price_list;")
            self.connection.commit()
            
    def create_tables(self):
        logging.info("Creating tables...")
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS coursework.vouchers CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS coursework.price_list CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS coursework.visitors CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS coursework.artists CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS coursework.accounts CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS coursework.sectors CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS coursework.visiting_grounds CASCADE;")
            
            
            
            cursor.execute("""
                        CREATE SCHEMA IF NOT EXISTS coursework;
                    """)
            cursor.execute("""
             CREATE TABLE IF NOT EXISTS coursework.visiting_grounds(
            id SERIAL PRIMARY KEY,
            ground_name TEXT UNIQUE NOT NULL

            );
            """)
            
     

            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS coursework.sectors(
                id SERIAL PRIMARY KEY,
                id_husbandry INTEGER REFERENCES coursework.visiting_grounds(id)
            );
                        """)

         

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS coursework.accounts(
                login VARCHAR(20) PRIMARY KEY,
                salt TEXT,
                hashed_password TEXT,
                surname VARCHAR(30) NOT NULL,
                firstname VARCHAR(30) NOT NULL,
                patronymic VARCHAR(30),
                date_of_birth DATE NOT NULL,
                sex CHAR(1) NOT NULL,
                mobile_phone VARCHAR(30) NOT NULL,
                email VARCHAR(50) NOT NULL,
                type_role VARCHAR(10) NOT NULL
            );

            """)
            
            
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS coursework.artists(
                id INTEGER REFERENCES coursework.sectors,
                login VARCHAR(20) REFERENCES coursework.accounts,
                PRIMARY KEY (id, login)
            );        
                    
                        """)

            cursor.execute("""
           CREATE TABLE IF NOT EXISTS coursework.visitors (
                    id SERIAL PRIMARY KEY,
                    ticket_num VARCHAR(10),
                    residence VARCHAR(100),
                    login VARCHAR(50)
                );

                    """)
                    
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS coursework.price_list(
                    id SERIAL PRIMARY KEY,
                    picture TEXT NOT NULL,
                    ground_name TEXT NOT NULL, 
                    price NUMERIC(10, 2) CONSTRAINT valid_price CHECK (price > 0),
                    is_relevant BOOLEAN NOT NULL,
                    id_sector INTEGER REFERENCES coursework.sectors,
                    description TEXT  
                );
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS coursework.vouchers (
                id SERIAL PRIMARY KEY,
                login VARCHAR(255),
                days INT,
                pictures INT,
                status VARCHAR(50),
                price DECIMAL,
                ticket_num VARCHAR(50),
                id_visitor INT REFERENCES coursework.visitors(id),
                id_pricelist INT REFERENCES coursework.price_list(id),
                is_relevant BOOLEAN
            );
            """)

            self.connection.commit()
            logging.info("Tables created.")
