import unittest
from rcon import Rcon
from rcon.test.server import RconServer, HOST, PORT

class RconTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = RconServer()
        cls.server.run()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_auth(self):
        rcon = Rcon(HOST, PORT, 'password')
        rcon.close()

    def test_send(self):
        rcon = Rcon(HOST, PORT, 'password')
        rcon.send('help')
        rcon.close()
