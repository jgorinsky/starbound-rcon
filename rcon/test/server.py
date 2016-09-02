from __future__ import print_function
import rcon.rcon
import socket
from struct import pack, unpack
import threading

LISTEN_HOST = 'localhost'
LISTEN_PORT = 21026

class RconServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((LISTEN_HOST, LISTEN_PORT))
        self.sock.listen(1)

    def run(self):
        while 1:
            client, addr = self.sock.accept()   
            handler = {
            rcon.SERVERDATA_AUTH: self.handle_auth,
            rcon.SERVERDATA_EXECCOMMAND: self.handle_cmd
            }
            packet = rcon.receive_packet(client)
            handler[packet.type](client, packet)
            client.close()
        self.sock.close()

    def handle_auth(self, client, packet):
        empty_pack = rcon.make_buf(rcon.SERVERDATA_RESPONSE_VALUE, packet.id, '')
        print(empty_pack)
        auth_pack = rcon.make_buf(rcon.SERVERDATA_AUTH_RESPONSE, packet.id, '')
        print(auth_pack)
        client.send(empty_pack)
        client.send(auth_pack)

    def handle_cmd(self):
        resp_pack = rcon.make_buf(rcon.SERVERDATA_RESPONSE_VALUE, packet.id, 'test response')


def main():
    server = RconServer()
    server.run()

if __name__ == '__main__':
    main()
