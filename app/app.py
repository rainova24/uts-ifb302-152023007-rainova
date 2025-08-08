"""
Flask Product Catalog Application
Displays products from RDS MySQL database with S3 images
"""

import os
import logging
from flask import Flask, render_template, jsonify
import pymysql
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', ''),
    'database': os.environ.get('DB_NAME', 'products_db'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True,
    'connect_timeout': 10
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def get_products() -> List[Dict]:
    """Retrieve all products from database"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, price, image_url FROM products ORDER BY id")
            products = cursor.fetchall()
            logger.info(f"Retrieved {len(products)} products")
            return products
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return []
    finally:
        connection.close()

@app.route('/')
def index():
    """Display products page"""
    products = get_products()
    return render_template('products.html', products=products)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'product-catalog'})

@app.route('/api/products')
def api_products():
    """API endpoint for products data"""
    products = get_products()
    return jsonify(products)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('products.html', products=[], error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return render_template('products.html', products=[], error="Internal server error"), 500

if __name__ == '__main__':
    # Validate required environment variables
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASS', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        exit(1)
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
