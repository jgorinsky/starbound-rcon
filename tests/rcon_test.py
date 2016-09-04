import unittest
from rcon import Rcon, main as rcon_main
from .server import RconServer, HOST, PORT

PASSWORD = 'password'

class RconTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = RconServer()
        cls.server.run()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_auth(self):
        rcon = Rcon(HOST, PORT, PASSWORD)
        rcon.close()

    def test_send(self):
        rcon = Rcon(HOST, PORT, PASSWORD)
        response = rcon.send('help')
        self.assertTrue('test response' in response)
        rcon.close()

    def test_main(self):
        response = rcon_main(['--password', PASSWORD, '--server', HOST, '--port', str(PORT), 'test-server'])
        self.assertTrue('test response' in response)


