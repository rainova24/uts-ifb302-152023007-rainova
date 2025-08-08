"""
Unit tests for Flask Product Catalog Application
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

class TestProductCatalog(unittest.TestCase):
    """Test cases for the product catalog application"""

    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'DB_HOST': 'localhost',
            'DB_USER': 'testuser',
            'DB_PASS': 'testpass',
            'DB_NAME': 'testdb',
            'FLASK_ENV': 'testing'
        })
        self.env_patcher.start()
        
        # Import app after setting environment variables
        from app import app
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()

    def test_index_route_returns_200(self):
        """Test that the main route returns status 200"""
        with patch('app.get_products') as mock_get_products:
            mock_get_products.return_value = []
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Product Catalog', response.data)

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)

    def test_api_products_endpoint(self):
        """Test API products endpoint"""
        with patch('app.get_products') as mock_get_products:
            mock_products = [
                {'id': 1, 'name': 'Test Product', 'price': 19.99, 'image_url': 'test.jpg'}
            ]
            mock_get_products.return_value = mock_products
            response = self.client.get('/api/products')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Product', response.data)

    def test_404_error_handling(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    @patch('app.get_db_connection')
    def test_products_display_with_data(self, mock_db_connection):
        """Test products display with mock data"""
        # Mock database connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'Test Product 1', 'price': 29.99, 'image_url': 'http://example.com/image1.jpg'},
            {'id': 2, 'name': 'Test Product 2', 'price': 39.99, 'image_url': 'http://example.com/image2.jpg'}
        ]
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_db_connection.return_value = mock_connection

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product 1', response.data)
        self.assertIn(b'Test Product 2', response.data)
        self.assertIn(b'29.99', response.data)

    @patch('app.get_db_connection')
    def test_database_connection_failure(self, mock_db_connection):
        """Test handling of database connection failure"""
        mock_db_connection.return_value = None
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Should still render template even with no products
        self.assertIn(b'Product Catalog', response.data)

if __name__ == '__main__':
    unittest.main()
