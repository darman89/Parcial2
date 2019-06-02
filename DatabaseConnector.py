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


def create_ApkTable():
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
        """,
                """
        DROP TABLE IF EXISTS "public"."testactivitynotdefined";
        CREATE TABLE testactivitynotdefined(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" json NOT NULL
        );
        """,
                """
        DROP TABLE IF EXISTS "public"."testinvalidactivityname";
        CREATE TABLE testinvalidactivityname(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" json NOT NULL
        );
        """,
                """
        DROP TABLE IF EXISTS "public"."testinvalidlabel";
        CREATE TABLE testinvalidlabel(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" json NOT NULL
        );
        """,
                """
        DROP TABLE IF EXISTS "public"."testwrongmainactivity";
        CREATE TABLE testwrongmainactivity(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" json NOT NULL
        );
        """,
                """
        DROP TABLE IF EXISTS "public"."testmissingpermissionmanifest";
        CREATE TABLE testmissingpermissionmanifest(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" json NOT NULL
        );
        """,
                """
        DROP TABLE IF EXISTS "public"."testsdkversion";
        CREATE TABLE testsdkversion(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" json NOT NULL
        );
        """,
                """
        DROP TABLE IF EXISTS "public"."testwrongstringresource";
        CREATE TABLE testwrongstringresource(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" json NOT NULL
        );
        """,
                """
        DROP TABLE IF EXISTS "public"."compareapkmutants";
        CREATE TABLE compareapkmutants(
            "id" SERIAL,
            "mutant_apk" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
            "result" bool,
            "diff" TEXT NOT NULL
        );
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


def select_Apk_ActivitiesNames():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT activities_names FROM apk LIMIT 1")
        row: list = list(cur.fetchone()[0])
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def select_Apk_ActivitiesLabels():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT activities_labels FROM apk LIMIT 1")
        row: list = list(cur.fetchone()[0])
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def select_Apk_MainActivity():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT main_activity FROM apk LIMIT 1")
        row: str = cur.fetchone()[0]
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def select_Apk_PermissionsList():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT permissions_list FROM apk LIMIT 1")
        row: list = list(cur.fetchone()[0])
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def select_Apk_MinSdkVersion():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT min_sdk_version FROM apk LIMIT 1")
        row: str = cur.fetchone()[0]
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def select_Apk_TargetSdkVersion():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT target_sdk_version FROM apk LIMIT 1")
        row: str = cur.fetchone()[0]
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def select_Apk_StringsApp():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT strings_app FROM apk LIMIT 1")
        row: str = cur.fetchone()[0]
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_ActivityNotDefinedTest(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO testactivitynotdefined(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_InvalidActivityNameTest(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO testinvalidactivityname(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_InvalidLabelTest(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO testinvalidlabel(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_WrongMainActivityTest(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO testwrongmainactivity(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_MissingPermissionManifestTest(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO testmissingpermissionmanifest(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_SdkVersionTest(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO testsdkversion(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_InvalidWrongStringResourceTest(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO testwrongstringresource(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_CompareApkMutantMethods(mutant_apk, result, diff):
    conn = None
    sql = """INSERT INTO compareapkmutants(mutant_apk, result, diff) VALUES(%s, %s, %s);"""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, (mutant_apk, result, diff,))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_ApkTable()
