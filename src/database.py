import os
from sqlite3 import Error, connect

# todo replace raw sqlite with sqlalchemy


class DbManager:
    def __init__(self, path=os.getcwd() + "\\db.sqlite"):
        super().__init__()

        self.connection = None
        self.create_connection(path)

    def create_connection(self, path):
        try:
            self.connection = connect(path)

            # enable the foreign key constraints
            self.connection.execute("PRAGMA foreign_keys = ON;")

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
# class DbManager


class DbManagerTag:
    def __init__(self, path_dict):
        super().__init__()

        self.TAGS = "tags"
        self.PATHS = "paths"

        self.root_dir = path_dict['root_dir']
        self.db_dir = path_dict['db_dir']
        self.db_file_sqlite = path_dict['db_file_sqlite']

        if not os.path.isfile(self.db_file_sqlite):
            with open(self.db_file_sqlite, 'w') as f:
                f.close()

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

        self.db_manager = DbManager(path=self.db_file_sqlite)
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
        return self.execute_read_query(query)

    def get_tags(self):
        query = "SELECT * FROM " + self.TAGS
        return [tag[0] for tag in self.execute_read_query(query)]

    def get_paths_tagged(self, tag_name):
        query = "SELECT path FROM " + self.PATHS + " WHERE tag_name LIKE '" + tag_name + "';"
        return [path for path in self.execute_read_query(query)]

    def insert_tag(self, new_tag):
        query = "INSERT INTO " + self.TAGS + " VALUES ( '" + new_tag + "' );"
        self.db_manager.execute_query(self.connection, query)

    def insert_path(self, tag, path):
        query = "INSERT INTO " + self.PATHS + " (tag_name, path) VALUES ('" + tag + "', '" + path + "');"
        self.db_manager.execute_query(self.connection, query)

    def exists_tag(self, tag):
        return self.get_tag(tag)

    def exists_path_tagged(self, tag, path):
        query = "SELECT * FROM " + self.PATHS + " WHERE tag_name LIKE '" + tag + "' AND path LIKE '" + path + "';"
        return self.execute_read_query(query)

    def delete_tag(self, tag):
        query = "DELETE FROM " + self.TAGS + " WHERE tag_name LIKE '" + tag + "';"
        self.db_manager.execute_query(self.connection, query)

    def delete_path_tagged(self, tag, path):
        query = "DELETE FROM " + self.PATHS + " WHERE tag_name LIKE '" + tag + "' AND path LIKE '" + path + "';"
        self.db_manager.execute_query(self.connection, query)

    def close_connection(self):
        if self.connection:
            self.db_manager.connection.close()
            print("Connection closed.")
# class DbManagerTag


class DbTag(DbManagerTag):
    def __init__(self, path_dict):
        super().__init__(path_dict)

    def get_tag(self, tag):
        return super(DbTag, self).get_tag(tag)

    def get_tags(self):
        return super(DbTag, self).get_tags()

    def get_paths_tagged(self, tag_name):
        return super(DbTag, self).get_paths_tagged(tag_name)

    def exists_tag(self, tag):
        return super(DbTag, self).exists_tag(tag)

    def exists_path_tagged(self, tag, path):
        return super(DbTag, self).exists_path_tagged(tag, path)

    def insert_tag(self, tag):
        super(DbTag, self).insert_tag(tag)

    def insert_path(self, tag, path):
        super(DbTag, self).insert_path(tag, path)

    def delete_tag(self, tag):
        super(DbTag, self).delete_tag(tag)

    def delete_path_tagged(self, tag, path):
        super(DbTag, self).delete_path_tagged(tag, path)

    def close_connection(self):
        super(DbTag, self).close_connection()
# class DbTag
