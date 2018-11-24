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
            'create_mirror_profile': self.create_mirror_profile
        }

        self.operation = data['operation']
        self.operation_args = data['operation_args']

        if self.operation in operations.keys():
            operations[self.operation]()
        else:
            raise Exception(f'Invalid operation: {self.operation} ' +
                            'function does not exist.')

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
            except mysql.connector.errors.IntegrityError:
                raise Exception('The provided ID is already being used.')
        else:
            raise Exception('Some arguments are missing. Please check the ' +
                            'json request')


if __name__ == "__main__":
    json = {}
    apple = Apple(json)
    from IPython import embed
    embed(header='In the main function...')
