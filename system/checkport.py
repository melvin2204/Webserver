import socket, errno,logging
def checkport(HOST,PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            logging.critical("Port already in use!")
            s.close()
            return False
        else:
            logging.critical(e)
            s.close()
            return False
    s.close()
    return True