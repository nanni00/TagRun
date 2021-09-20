import sqlite3
from sqlite3 import Error
import os


# todo replace raw sqlite with sqlalchemy


class DbManager:
    def __init__(self, path=os.getcwd() + "\\TagRun.sqlite"):
        super().__init__()

        self.connection = None
        self.create_connection(path)

    def create_connection(self, path):
        try:
            self.connection = sqlite3.connect(path)

            # enable the foreign key constraints
            self.connection.execute("PRAGMA foreign_keys = ON;")
            # self.connection.cursor().execute("PRAGMA foreign_keys = ON;")

            # print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_connection(self):
        if self.connection is not None:
            return self.connection
        else:
            return None

    def execute_query(self, connection, query):
        if connection is not None:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
                connection.commit()
                # print("Query executed successfully")
            except Error as e:
                print(f"The error '{e}' occurred")


class DbTag:
    def __init__(self):
        super().__init__()

        self.TAGS = "tags"
        self.PATHS = "paths"

        create_tags_table = """
        CREATE TABLE IF NOT EXISTS tags (
            tag_name TEXT PRIMARY KEY
        );
        """

        create_paths_table = """
        CREATE TABLE IF NOT EXISTS paths (
            tag_name TEXT NOT NULL,
            path TEXT NOT NULL,
            PRIMARY KEY (tag_name, path),
            FOREIGN KEY (tag_name) REFERENCES tags (tag_name)
            ON DELETE CASCADE
        );
        """

        self.db_manager = DbManager(path="C:\\databases\\sqlite\\TagRun.sqlite")
        self.connection = self.db_manager.get_connection()

        self.db_manager.execute_query(self.connection, query=create_tags_table)
        self.db_manager.execute_query(self.connection, query=create_paths_table)

    def execute_read_query(self, query):
        cursor = self.db_manager.get_connection().cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_tag(self, tag):
        query = "SELECT * FROM " + self.TAGS + " WHERE tag_name LIKE '" + tag + "';"
        # print(self.execute_read_query(query))
        return self.execute_read_query(query)

    def get_tags(self):
        query = "SELECT * FROM " + self.TAGS
        # print(query)
        return [tag[0] for tag in self.execute_read_query(query)]

    def get_paths_tagged(self, tag_name):
        query = "SELECT path FROM " + self.PATHS + " WHERE tag_name LIKE '" + tag_name + "';"
        print(query)
        print(self.execute_read_query(query))
        return [path for path in self.execute_read_query(query)]

    def insert_tag(self, new_tag):
        query = "INSERT INTO " + self.TAGS + " VALUES ( '" + new_tag + "' );"
        # print(query)
        self.db_manager.execute_query(self.connection, query)

    def insert_path(self, tag_name, path):
        query = "INSERT INTO " + self.PATHS + " (tag_name, path) VALUES ('" + tag_name + "', '" + path + "');"
        self.db_manager.execute_query(self.connection, query)

    def exists_tag(self, tag):
        return self.get_tag(tag)

    def exists_path_tagged(self, tag, path):
        query = "SELECT * FROM " + self.PATHS + " WHERE tag_name LIKE '" + tag + "' AND path LIKE '" + path + "';"
        return self.execute_read_query(query)

    def delete_tag(self, tag):
        query = "DELETE FROM " + self.TAGS + " WHERE tag_name LIKE '" + tag + "';"
        self.db_manager.execute_query(self.connection, query)


if __name__ == "__main__":
    db = DbTag()
