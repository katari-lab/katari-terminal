 #
import unittest
from src.gateways.AudioGateway import AudioGateway

class TestAudioGateway(unittest.TestCase):

    def setUp(self):
        self.gateway = AudioGateway()

    def test_is_mp3_silent(self):        
        response = self.gateway.is_mp3_silent("C:\\Users\\gregnl\\AppData\\Local\\Temp\\tmplk68o7it.mp3")                
        self.assertTrue(response)