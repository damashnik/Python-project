import os
import datetime
import ConfigParser
import socket
import sqlite3

config_file = "server.cfg"
local_datetime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

def read_from_db (table):
    try:
        db_conn = sqlite3.connect(database)
        db_line = "select clientID, clientIP, clientKey from " + table +";"
        cursor = db_conn.cursor()
        try:
            cursor.execute(db_line)
            return cursor.fetchall()
        except Exception as e:
            print "Error", e
        db_conn.close()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
    except Exception as e:
        print "Error",e

def update_clients_status(table, values):
    try:
        db_conn = sqlite3.connect(database)
        db_line = "insert " + table + " values " + str(values)
        write_log(db_line)
        cursor = db_conn.cursor()
        try:
            cursor.execute(db_line)
            return_value = 1
        except Exception as e:
            print "Error", e

        db_conn.commit()
        db_conn.close()
        return return_value
    except sqlite3.Error as e:
        print("Database error: %s" % e)
    except Exception as e:
        print "Error", e



def request_clients_status():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, int(port)))
    server.listen(2)
    conn, addr = server.accept()
    print('Connected by', addr)
    while 1:
        try:
            data = conn.recv(1024)
            if not data: continue
            #conn.sendall(data)
            data_tuple=tuple(data.split(","))
            client_action = data_tuple[0]
            client_id = data_tuple[1]
            client_key = data_tuple[2]
            client_name = data_tuple[3]
            values = (client_id, addr[0],client_key,client_name, local_datetime)
            if client_action == "a":
                if add_to_db ('clients', values):
                    conn.sendall("Client "+data+" has been added successfully")
                    log_line = "Client "+data+" has been added successfully\n"
                    write_log(log_line)
                else:
                    print "To be defined - add / replace client"
            else:
                if del_from_db ('clients', values):
                    conn.sendall("Client "+data+" has been removed successfully")
                    log_line = "Client "+data+" has been removed successfully\n"
                    write_log(log_line)
                else:
                    print "To be defined - remove client"
            continue
        except KeyboardInterrupt:
            break
    #conn.close()

def write_log(line):
    '''
    In this function we will care about all events in the system
    :param log_file:
    :return:

    '''

    try:
        with open(log_file, 'a+') as file:
            file.write(local_datetime + ":" + line)

    except IOError as e:
        print("Unable to open file", e)  # Does not exist OR no read permissions


if __name__ == "__main__":

    '''
    Section of initiation parameters based on configuration file
    Configuration file server.cfg, should be located in the same directory.
    Using configparser module for config file parsing
    '''

    try:
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        server_ip = config.get('Server','server_address')
        port = config.get('Server','port')
        log_file = config.get('Server','log_file')
        database = config.get('Server','db')
        log_line = "Initiation: server " + server_ip + " working with Server " + server_ip + " and listening on port " + port + " database is "+database+"\n"
        write_log(log_line)
        list_of_clients = read_from_db('clients')
        for client in list_of_clients:
            print client
            status = request_clients_status()
            update_clients_status('reports', status)

    except ConfigParser.Error as err:
        print("Error reading configuration", err)
        exit()

