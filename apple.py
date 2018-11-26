"""Module in charge of creating the database connection and query anything
necessary to obtain and set data in the Smart Mirror User Settings database.
"""

from dotenv import load_dotenv
from os.path import join, dirname
import json
import mysql.connector
import os


class Apple():
    """Main class that handles the reading of .env file and the creation of a
    connection to the MySQl database by an instance of itself.
    """

    def __init__(self, json):
        """Constructor like method for the 'Apple' class.
        """
        self.config = self.read_env_file()
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor()
        self.json = json

    def read_env_file(self):
        """Method for reading the .env file and creating a dictionary from it.
        """
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        config = {
            'host': os.getenv('HOST'),
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD'),
            'database': os.getenv('DATABASE')
        }
        return config

    def create_connection(self):
        """Create connection to the previously defined database

        Returns
        -------
        mysql.connector.connection.MySQLConnection
            Returns connector to database
        """
        mydb = mysql.connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            passwd=self.config['password'],
            database=self.config['database']
        )
        return mydb

    def manage_operations(self):
        """Handle the received json to return whatever the other application
        asks for.
        """
        data = json.loads(self.json)

        operations = {
            'create_mirror_profile': self.create_mirror_profile,
            'delete_user': self.delete_user,
            'update_user': self.update_user,
            'auth_user': self.auth_user
        }

        self.operation = data['operation']
        self.operation_args = data['operation_args']

        if self.operation in operations.keys():
            response = operations[self.operation]()
        else:
            raise Exception(f'Invalid operation: {self.operation} ' +
                            'function does not exist.')
        return response

    def create_mirror_profile(self):
        """Insert record in the database
        """
        keys = ['id', 'mail', 'mail_password', 'news_country',
                'password', 'weather_city', 'weather_country']
        if all(k in keys for k in self.operation_args.keys()):
            query = f"""
            INSERT INTO smartmirror (
                id, 
                mail, 
                mail_password, 
                news_country, 
                password, 
                weather_city, 
                weather_country
            )
            VALUES (
                '{self.operation_args['id']}', 
                '{self.operation_args['mail']}', 
                '{self.operation_args['mail_password']}', 
                '{self.operation_args['news_country']}', 
                '{self.operation_args['password']}', 
                '{self.operation_args['weather_city']}', 
                '{self.operation_args['weather_country']}'
            )
            """
            try:
                self.cursor.execute(query)
                self.connection.commit()
                return 'New user added correctly.'
            except mysql.connector.errors.IntegrityError:
                raise Exception('The provided ID is already being used.')
        else:
            raise Exception('Some arguments are missing. Please check the ' +
                            'json request')

    def delete_user(self):
        """Method delete an specified user from the database
        """
        keys = ['id']
        if all(k in keys for k in self.operation_args.keys()):
            query = f"""
            DELETE FROM smartmirror WHERE id = {self.operation_args['id']}
            """
            try:
                self.cursor.execute(query)
                self.connection.commit()
                return 'User deleted correctly.'
            except Exception:
                raise Exception('There was an issue while trying to ' +
                                'delete an user.')
        else:
            raise Exception('Id in request is missing. Please check the ' +
                            'json request')

    def update_user(self):
        """Method for updating the user preferences
        """
        # from IPython import embed
        # embed(header='Inside of update_user')
        if 'id' in self.operation_args.keys():
            start_query = f"""
            UPDATE smartmirror
            SET
            """
            set_query = ""
            for key, value in self.operation_args.items():
                if key is not 'id':
                    set_query += f" {key} = '{value}', "
            end_query = f" WHERE id = '{self.operation_args['id']}'"
            # from IPython import embed
            # embed(header='Inside of update_user')
            final_query = start_query + set_query[:-2] + end_query
            try:
                self.cursor.execute(final_query)
                self.connection.commit()
                return 'User updated correctly.'
            except Exception:
                raise Exception('Error while trying to update user prefs.')
        else:
            raise Exception('Id in request is missing. Please check the ' +
                            'json request')

    def auth_user(self):
        """Verifies if an user exist in our database
        """
        keys = ['id', 'password']
        if all(k in keys for k in self.operation_args.keys()):
            query = f"""
            SELECT * 
            FROM smartmirror
            WHERE id = '{self.operation_args['id']}'
            AND password = '{self.operation_args['password']}'
            """
            try:
                self.cursor.execute(query)
                users = self.cursor.fetchall()
                if len(users) >= 1:
                    return 'True'
                else:
                    return 'False'
            except mysql.connector.errors.IntegrityError:
                raise Exception('There was no user found in our database.')
        else:
            raise Exception('Some arguments are missing. Please check the ' +
                            'json request')



if __name__ == "__main__":
    json = {}
    apple = Apple(json)
    from IPython import embed
    embed(header='In the main function...')
