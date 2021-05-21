import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing


class DbConnector:
    def __init__(self):
        self.host = 'Your IP database'
        self.user = 'USERNAME'
        self.password = 'PASSWORD'
        self.db = 'DATABASE NAME'

    def create_connection(self):
        """ create a database connection to a MySQL database """
        connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            cursorclass=DictCursor
            )

        return connection

    def create_table_versions(self):
        """ create a table with browser versions """
        with closing(self.create_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute('CREATE TABLE IF NOT EXISTS `Versions` ('
                               '`id` INT NOT NULL AUTO_INCREMENT, `lovenseBrowser` TINYTEXT,'
                               '`lovenseExtension` TINYTEXT, `firefoxDesktop` TINYTEXT, '
                               '`firefoxAndroid` TINYTEXT, `firefoxIOS` TINYTEXT, '
                               '`chrome` TINYTEXT, `alohaAndroid` TINYTEXT, '
                               '`alohaIOS` TINYTEXT,'
                               '`date` DATE NOT NULL,'
                               'PRIMARY KEY (id))')

        return self

    def select_all_versions(self) -> object:
        with closing(self.create_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Versions order by id desc limit 1')

                for line in cursor:
                    return line

    def form_query(self, data):
        keys = ''
        values = ''

        for key in data:
            keys += '{},'.format(key)
            values += '"{}",'.format(data[key])

        query = 'INSERT INTO Versions ({}) VALUES ({})'.format(keys[:-1], values[:-1])
        return query

    def insert_new_data(self, data):
        with closing(self.create_connection()) as connection:
            with connection.cursor() as cursor:
                query = self.form_query(data)
                cursor.execute(query)
                connection.commit()