import unittest
from src.gateways.OpenIAGateway import OpenAIGateway

class TestOpenIAGateway(unittest.TestCase):

    def setUp(self):
        self.gateway = OpenAIGateway()

    def test_get_openai_response(self):
        response = self.gateway.transcription_to_action("kubectl get pads")
        print(response)
        self.assertTrue(response)
    

if __name__ == '__main__':
    unittest.main()