import unittest
from unittest.mock import patch
from CloudManager import CloudManager

class TestCloudManager(unittest.TestCase):

    @patch('CloudManager.CloudManager.connect')
    @patch('CloudManager.CloudManager.retrieve_data')
    @patch('CloudManager.CloudManager.close')
    def test_retrieve_data(self, mock_close, mock_retrieve_data, mock_connect):
        mock_retrieve_data.return_value = [{'id': '123', 'store': 'Brussels', 'date': '2020-01-01', 'total_price': 4.5, 'products': [{'id': '123', 'name': 'Banana', 'price': 1.5, 'category': 'Fruit'}]}] * 1000
        
        cloud_manager = CloudManager()
        cloud_manager.connect()
        data = cloud_manager.retrieve_data()
        cloud_manager.close()
        
        self.assertEqual(len(data), 1000)
        mock_connect.assert_called_once()
        mock_retrieve_data.assert_called_once()
        mock_close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
