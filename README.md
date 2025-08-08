# Product Catalog Flask Application

A simple Flask web application that displays products from an AWS RDS MySQL database with images stored in S3.

## Features

- Connects to RDS MySQL database
- Displays products with images, names, and prices
- Responsive design with modern UI
- Docker containerization
- Health check endpoint
- Error handling and logging
- Unit tests with CI/CD pipeline

## Prerequisites

- Python 3.9+
- MySQL database with `products` table
- AWS RDS and S3 access

## Database Schema

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(500)
);
