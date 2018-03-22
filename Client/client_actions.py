#!/usr/bin/python

import os
import sys
import time
import ConfigParser
import socket

""" 
Start variables definition
"""
config_file = "client.cfg"
localtime = time.asctime(time.localtime(time.time()))
"""
Stop variables definition
"""
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
    config.write(config_file)
    write_log("Key "+key+" has been added to the client")
    return key

def send_client_request(action):
    """
    Function to add, modify or remove information for client
    :return:
    """
    if action == "a":
        key = generate_key()
        parameters = ",".join(["a",client_id,key,client_name])
    else:
        parameters = ",".join(["d", client_id, client_key, client_name])
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


def read_status_file():
    with open(client_status_file, "r+") as sf:
        return (",".join(sf.readlines()))


def write_log(line):
    '''
    In this function we will care about all events in the system
    :param log_file: 
    :return: 
    '''
    try:
        with open(log_file, 'a+') as file:
            file.write(localtime+":"+line)

    except IOError as e:
        print("Unable to open file", e)  # Does not exist OR no read permissions

def user_menu():
    if client_key != '':
        print ("""
        1. Replace Client Key
        2. Delete Client
        Q. Exit
        """
        )
    else:
        print ("""
        1. Add Client
        Q. Exit
        """
        )
    selection = raw_input("Please Select:")
    if selection == '1':
        send_client_request("a")
    elif selection == '2':
        send_client_request("d")
    elif selection == 'Q':
        exit()
    else:
        print ("Unknown Option Selected!")


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
        print len(sys.argv)
        if len(sys.argv) > 1 and sys.argv[1]=="a":
            send_client_request("a")
        elif len(sys.argv) > 1 and sys.argv[1] == "d":
            send_client_request("d")
        else:
            user_menu()
 #       config_file.close()
    except ConfigParser.Error as err:
        print("Error reading configuration", err)
        exit()


