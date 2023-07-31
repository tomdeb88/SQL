import sqlite3
from sqlite3 import Error

db_file = "database.db"


def create_connection(db_name):
    conn = None

    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, sql):
    conn = create_connection(db_file)
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


if __name__ == "__main__":
    employees_sql = """
    CREATE TABLE IF NOT EXISTS employees (
    id integer PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    position text NOT NULL

    );
    """

    personal_details = """
    CREATE TABLE IF NOT EXISTS stuff_info (
    id integer PRIMARY KEY,
    employee_id integer NOT NULL,
    gender text,
    address text,
    city text,
    phone integer,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
    
    );
    """
    conn = create_connection(db_file)
    # Creating tables

    if conn is not None:
        create_table(conn, employees_sql)
        create_table(conn, personal_details)
        conn.close()


def add_emp(conn, emp):
    sql = "INSERT INTO employees (first_name, last_name, position) VALUES(?,?,?)"
    c = conn.cursor()
    c.execute(sql, emp)
    conn.commit()
    return c.lastrowid


def add_info(conn, info):
    sql = "INSERT INTO stuff_info (employee_id,gender,address,city,phone) VALUES(?,?,?,?,?)"
    c = conn.cursor()
    c.execute(sql, info)
    conn.commit()
    return c.lastrowid


if __name__ == "__main__":
    conn = create_connection(db_file)

    emp_1 = ("Tomasz", "Debowski", "Wozny")
    emp_2 = ("Marzena", "Muszyna", "Sekretarka")
    emp_3 = ("Robert", "Nowak", "Tenisista")
    emp_4 = ("Anna", "Nowak", "Recepcjonistka")
    info = (3, "m", "Nowa 9", "Poznan", 999555444)

    emp_id = add_emp(conn, emp_3)
    info_id = add_info(conn, info)
    conn.close()


def select_all(conn, table):
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    records = c.fetchall()
    return records


# if __name__=="__main__":
#     conn = create_connection(db_file)
#     for emp in select_all(conn, "stuff_info"):
#         print(emp)
#     conn.close()


def select_by_atrribute(conn, tabel, **attr):
    parameters = [f"{k}=?" for k in attr]
    parameters = " AND ".join(parameters)
    values = tuple(v for v in attr.values())
    c = conn.cursor()
    c.execute(f"SELECT * FROM {tabel} WHERE {parameters}", values)
    records = c.fetchall()
    return records


# if __name__=='__main__':
#     conn = create_connection(db_file)
#     print(select_by_atrribute(conn, "stuff_info", gender="m"))
#     conn.close()


def updateing(conn, table, first_name, last_name, **attr):
    parameters = [f"{k}=?" for k in attr]
    parameters = " ,".join(parameters)
    values = tuple(v for v in attr.values())
    values += (
        first_name,
        last_name,
    )
    print(parameters, values)
    sql = f"""UPDATE {table} SET {parameters} WHERE first_name=? AND last_name=?"""

    c = conn.cursor()
    c.execute(sql, values)
    conn.commit()


# if __name__ == "__main__":
#     conn = create_connection(db_file)
#     updateing(conn, "employees", "Tomasz", "Debowski", position="Barman")
#     conn.close()


def delete(conn, table, **kwarg):
    parameters = [f"{k}=?" for k in kwarg]
    parameters = " AND ".join(parameters)
    values = tuple(v for v in kwarg.values())

    c = conn.cursor()
    c.execute(f"DELETE FROM {table} WHERE {parameters}", values)
    conn.commit()


# if __name__ == "__main__":
#     conn = create_connection(db_file)
#     delete(conn, "employees", position="Tenisista")
#     conn.close()
