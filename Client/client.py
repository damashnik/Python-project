#!/usr/bin/python

import os
import time
import ConfigParser
import socket

config_file = "client.cfg"


def delete_client_request():
    pass


def add_client_request():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, int(port)))
    client.sendall(client_id)
    log_line = "Sending request to add client with ID:"+client_id+", to server "+server_ip+" on port "+port+"\n"
    write_log(log_line)
    data = client.recv(1024)
    client.close()
    log_line = "Response from Server" + data + "\n"
    write_log(log_line)
    print ("Recieved", repr(data))


def listen_to_server(server_name,port):
    pass


def read_status_file():
    pass

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
    menu['1'] = "Add Client."
    menu['2'] = "Delete Client."
    menu['3'] = "Run Client."
    menu['4'] = "Exit."
    while True:
        options = menu.keys()
        for entry in options:
            print entry, menu[entry]

        selection = raw_input("Please Select:")
        if selection == '1':
            add_client_request()
        elif selection == '2':
            delete_client_request()
        elif selection == '3':
            listen_to_server()
        elif selection == '4':
            break
        else:
            print ("Unknown Option Selected!")


if __name__ == "__main__":

    '''
    Section of initiation parameters based on configuration file
    Configuration file client.cfg, should be located in the same directory.
    Using configparser module for config file parsing
    '''

    try:
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        server_ip = config.get('Server', 'server_address')
        port = config.get('Server','port')
        client_id = config.get('Client','id')
        log_file = config.get('Client','log_file')
        log_line = "Initiation: Client "+client_id+" working with Server "+server_ip+" and listening on port "+port+"\n"
        write_log(log_line)
        user_menu()
    except ConfigParser.Error as err:
        print("Error reading configuration", err)
        exit()


