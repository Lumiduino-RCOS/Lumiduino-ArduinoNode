import socket
import select
import threading
from LumiduinoNodePython.customlogger import CustomLogger
#from LumiduinoNodePython.tcpclient import TcpClient
#from tcpclient import TcpClient
import LumiduinoNodePython.containers as containers
dir(containers)
#from containers import TcpClient

class TcpServer(object):

    def __init__(self, port, logger: CustomLogger):
        self.logger = logger
        self.running = True
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockfd.setblocking(0)
        self.sockfd.bind(("0.0.0.0", port))
        self.sockfd.listen()
        self.logger.log_task_start("Listening for clients on {}".format(port))

        self.clients_map = {}

        self.read = [self.sockfd]
        self.write = []
        self.x = []

        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.start()

    def server_loop(self):
        while self.running:
            try:
                rlist, wlist, xlist = select.select(self.read, self.write, self.read, 1)

                for fd in rlist:
                    if fd is self.sockfd:
                        connection, client_addr = self.sockfd.accept()
                        connection.setblocking(0)
                        self.read.append(connection)
                        self.clients_map[connection] = containers.LumiduinoClient.tcp_client(connection, client_addr)
                        self.logger.log_task_start("client {}".format(client_addr))
                    else:
                        data = fd.recv(1024)
                        if data:
                            self.clients_map[fd].recv_tcp_fragment(data)
                        else:
                            self.logger.log_task_stop('client {}'.format(fd))
                            self.read.remove(fd)
                            self.clients_map[fd].close()
                            del self.clients_map[fd]
                            

                for fd in xlist:
                    print("{} has suffered an exception".format(fd))
                    self.read.remove(fd)
                    fd.close()
            except socket.timeout as err:
                continue

    def close(self):
        self.logger.log_task_start("Safe Server Close Sequence")
        self.running = False
        self.server_thread.join()
        for i in self.read:
            i.close()
        self.logger.log_task_stop("Safe Server close Sequence")

    