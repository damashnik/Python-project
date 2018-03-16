#!/usr/bin/python

import os
import time
import ConfigParser
import socket
import multiprocessing

""" 
Start variables definition
"""
config_file = "client.cfg"

"""
Stop variables definition
"""
def delete_client_request():
    """
    Function for delete existing client request
    Client sending request contains ID and Key to server with parameter "d"
    :return:
    """
    pass

def generate_key():
    """
    Key generation for further client identification in all operations with server
    Key generated with urandom and encoded with Base-64
    In order to remove blank spaces and special characters using strip
    :return: key
    """
    key = os.urandom(24).encode('base-64')
    key.replace('/','_').strip('_\ /t/n/r')
    print key
    config.set('Client', 'key', key)
    write_log("Key "+key+" has been added to the client")
    return key

def add_client_request():
    """
    Function to add or modify information for client
    :return:
    """
    key = generate_key()
    parameters = ",".join([client_id,key,client_name])

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, int(port)))
        client.sendall(parameters)
        log_line = "Sending request to add client with ID:"+client_id+", and key "+key+" to server "+server_ip+" on port "+port+"\n"
        write_log(log_line)
        data = client.recv(1024)
        client.close()
        log_line = "Response from Server " + data + "\n"
        write_log(log_line)
        print ("Recieved", repr(data))
    except Exception as e:
        print "Can't establish connection to servers:", e


def listen_to_server(server_name,port):
    pass


def read_status_file():
    with open(client_status_file, "r+") as sf:
        return (",".join(sf.readlines()))


def write_log(line):
    '''
    In this function we will care about all events in the system
    :param log_file: 
    :return: 
    
    '''

    localtime = time.asctime(time.localtime(time.time()))
    try:
        with open(log_file, 'a+') as file:
            file.write(localtime+":"+line)

    except IOError as e:
        print("Unable to open file", e)  # Does not exist OR no read permissions


def user_menu():
    menu = {}
    if client_key != '':
        menu['1'] = "Replace Client Key."
        menu['2'] = "Delete Client."
    else:
        menu['1'] = "Add Client."
    menu['Q'] = "Exit."
    while True:
        options = menu.keys()
        for entry in options:
            print entry, menu[entry]
        selection = raw_input("Please Select:")
        if selection == '1':
            add_client_request()
        elif selection == '2':
            delete_client_request()
        elif selection == 'Q':
            break
        else:
            print ("Unknown Option Selected!")

def keep_alive():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind(server_ip, int(client_keep_alive_port))
        client.listen(1)
        conn, addr = client.accept()
        print('Status data requested by', addr)
        while 1:
            try:
                data = client_id+","+read_status_file()
                conn.sendall(data)
                log_line = "status " + data + " has been sent to server\n"
                write_log(log_line)
                continue
            except KeyboardInterrupt:
                break
    except Exception as e:
        print "Keep alive listener problems:", e






if __name__ == "__main__":

    '''
    Section of initiation parameters based on configuration file
    Configuration file client.cfg, should be located in the same directory.
    Using configparser module for config file parsing
    '''

    try:

        """
        Parsing of client.cfg file contains configuration parameters related to Client 
        """

        config = ConfigParser.ConfigParser()
        config.read(config_file)
        server_ip = config.get('Server', 'server_address')
        port = config.get('Server','port')
        client_id = config.get('Client','id')
        client_name = config.get('Client','name')
        client_keep_alive_port = config.get('Client','keep_alive_port')
        client_status_file = config.get('Client','status_file')
        try:
            client_key = config.get('Client','key')
        except:
            client_key = ''
        log_file = config.get('Client','log_file')
        log_line = "Initiation: Client "+client_id+" working with Server "+server_ip+" and listening on port "+port+"\n"
        write_log(log_line)
        """
        Create 2 parallel processes:
        client_operation for treatment of Client's operations like add, replace or remove client
        keepalive_listener for server's requests listening
         
        """
        client_operation = multiprocessing.Process(target = user_menu, args=())
        keepalive_listener = multiprocessing.Process(target=keep_alive, args=())

    except ConfigParser.Error as err:
        print("Error reading configuration", err)
        exit()


