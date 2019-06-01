import psycopg2
from configparser import ConfigParser

DATABASE_INI = 'database.ini'


def config(filename=DATABASE_INI, section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def insert_ApkProperties(app_name, main_activity, min_sdk_version, target_sdk_version, activities_labels,
                         activities_names,
                         services_names, permissions_list, strings_app):
    """ Connect to the PostgreSQL database server """
    conn = None
    sql = """INSERT INTO apk(app_name, main_activity, min_sdk_version, target_sdk_version, activities_labels, activities_names, services_names, permissions_list, strings_app) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('Executing PostgreSQL Query...')
        cur.execute(sql, (
            app_name, main_activity, min_sdk_version, target_sdk_version, activities_labels, activities_names,
            services_names,
            permissions_list, strings_app,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def createApkTable():
    """ create apk table in the PostgreSQL database """
    commands = ("""
        DROP TABLE IF EXISTS "public"."apk";
        CREATE TABLE "public"."apk" (
          "app_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
          "main_activity" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
          "activities_labels" json NOT NULL,
          "activities_names" json NOT NULL,
          "services_names" json NOT NULL,         
          "permissions_list" json NOT NULL,
          "min_sdk_version" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
          "target_sdk_version" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
          "strings_app" json NOT NULL
        )
        """,
        """
        ALTER TABLE "public"."apk" 
        ADD PRIMARY KEY ("app_name");
        """,)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    createApkTable()
