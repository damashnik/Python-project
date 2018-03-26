import os
import time
import ConfigParser
import socket
import hashlib

""" 
Start variables definition
"""
config_file = "client.cfg"
localtime = time.asctime(time.localtime(time.time()))
"""
Stop variables definition
"""

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
            file.write(localtime + ":" + line)

    except IOError as e:
        print("Unable to open file", e)  # Does not exist OR no read permissions


def keep_alive():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind(server_ip, int(client_keep_alive_port))
        client.listen(1)
        conn, addr = client.accept()
        print('Status data requested by', addr)
        while 1:
            try:
                data = client_id + "," + read_status_file()
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
        client_id = config.get('Client', 'id')
        client_name = config.get('Client', 'name')
        client_keep_alive_port = config.get('Client', 'keep_alive_port')
        client_status_file = config.get('Client', 'status_file')
        log_file = config.get('Client', 'log_file')
        try:
            client_key = config.get('Client', 'key')
        except:
            print("Client is not registered yet, please register client and run service again")
            log_line = "Client is not registered yet"
            write_log(log_line)
            exit()
        log_line = "Initiation: Client " + client_id + " working with Server " + server_ip + " and listening on port " + client_keep_alive_port + "\n"
        write_log(log_line)
        keep_alive()
    except ConfigParser.Error as err:
        print("Error reading configuration", err)
        exit()
