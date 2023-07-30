import pymysql

connection_object = None


def connect_to_db():
    global connection_object
    if not connection_object:
        db_server_name = "sql7.freesqldatabase.com"
        db_user = "sql7635068"
        db_password = "6Qe3WfJSiL"
        db_name = "sql7635068"
        char_set = "utf8mb4"
        cursor_type = pymysql.cursors.DictCursor
        connection_object = pymysql.connect(host=db_server_name, user=db_user, password=db_password,

                                            db=db_name, charset=char_set, cursorclass=cursor_type)

    return connection_object


def execute_query(sql_query, *args):
    db_connection = connect_to_db()
    cursorObject = db_connection.cursor()
    x = cursorObject.execute(sql_query, args)
    db_connection.commit()
    return x


try:
    connect_to_db()
    # drop_client = "DROP TABLE client"
    # execute_query(drop_client)
    # create_client_table = "CREATE TABLE client(id int AUTO_INCREMENT PRIMARY KEY, LastName varchar(32), FirstName varchar(32))"
    # execute_query(create_client_table)
    # create_network_table = "CREATE TABLE network(id int AUTO_INCREMENT PRIMARY KEY, client_id int, FOREIGN KEY(client_id) REFERENCES client(id), name varchar(64), location varchar(64))"
    # execute_query(create_network_table)
    # create_device_table = "CREATE TABLE device(id int AUTO_INCREMENT PRIMARY KEY, network_id int , FOREIGN KEY(network_id) REFERENCES network(id), ip varchar(64), mac varchar(64))"
    # execute_query(create_device_table)
    # create_connection_table = "CREATE TABLE connection(id int AUTO_INCREMENT PRIMARY KEY, src_device_id int , FOREIGN KEY(src_device_id) REFERENCES device(id), dst_device_id int , FOREIGN KEY(dst_device_id) REFERENCES device(id), protocol varchar(64))"
    # execute_query(create_connection_table)
    # create_technician_table = "CREATE TABLE technician(id int AUTO_INCREMENT PRIMARY KEY, name varchar(64), password varchar(64))"
    # execute_query(create_technician_table)
    # create_permission_table = "CREATE TABLE permission(id int AUTO_INCREMENT PRIMARY KEY, client_id int , FOREIGN KEY(client_id) REFERENCES client(id), technician_id int , FOREIGN KEY(technician_id) REFERENCES technician(id))"
    # execute_query(create_permission_table)
    # alter_device_table = "ALTER TABLE device ADD COLUMN vendor varchar(64)"
    # execute_query(alter_device_table)
    # alter_connection_table = "ALTER TABLE connection ADD COLUMN network_id int , FOREIGN KEY (network_id) REFERENCES network(id)"
    # execute_query(alter_connection_table)



except Exception as e:

    print("Exeception occured:{}".format(e))

finally:
    if connection_object:
        connection_object.close()
