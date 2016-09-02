import rcon.rcon
import socket
import asyncore
import threading

HOST = 'localhost'
PORT = 21026

class RconHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        handler = {
            rcon.SERVERDATA_AUTH: self.handle_auth,
            rcon.SERVERDATA_EXECCOMMAND: self.handle_cmd
        }
        packet = rcon.receive_packet(self)
        handler[packet.type](packet)

    def handle_auth(self, packet):
        empty_pack = rcon.make_buf(rcon.SERVERDATA_RESPONSE_VALUE, packet.id, '')
        auth_pack = rcon.make_buf(rcon.SERVERDATA_AUTH_RESPONSE, packet.id, '')
        self.send(empty_pack)
        self.send(auth_pack)

    def handle_cmd(self, packet):
        resp_pack = rcon.make_buf(rcon.SERVERDATA_RESPONSE_VALUE, packet.id, 'test response')
        self.send(resp_pack)


class RconServer(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((HOST, PORT))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            client, addr = pair
            handler = RconHandler(client)

    def run(self):
        self.thread = threading.Thread(target=asyncore.loop)
        self.thread.start()

    def stop(self):
        self.close()
        self.thread.join()

if __name__ == '__main__':
    run()
