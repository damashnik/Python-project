import ConfigParser
import time
import sqlite3
config_file = 'sqlite.cfg'
database = ""
def write_log(line):
    '''
    In this function we will care about all events in the system
    :param log_file:
    :return:

    '''

    localtime = time.asctime(time.localtime(time.time()))
    try:
        with open(log_file, 'a+') as file:
            file.write(localtime + ":" + line)

    except IOError as e:
        print("Unable to open file", e)  # Does not exist OR no read permissions

def sqlite3_create_connection(db_file):
    """ Create database connection to SQLite database
        specified by db_file
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print e

    return None

def create_table (conn, create_table_sql):
    try:
        c = conn.cur

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
    except ConfigParser.Error as err:
        print("Error reading configuration", err)
        exit()
