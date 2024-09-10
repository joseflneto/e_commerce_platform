# Project - E-commerce Platform

## Instructions to Run

### Option 1: Run without Docker

1. Navigate to the `/src` directory:

   cd src

2. Run the application with the command:

   python app.py

3. The project will be available at http://localhost:8080/.

### Option 2: Run with Docker

1. In the root directory of the project, build the Docker image:

   docker build -t ecommerce-app .

2. Run the Docker container:

   docker run -p 8080:8080 ecommerce-app

3. The project will be available at http://localhost:8080/.

## Data

User data, cart, orders, and product information are located in the `/src/data` directory.

## Accessing the System

To use the system, you need to be logged in. By default, the system creates an admin user with the following credentials:

- **Username:** admin
- **Password:** admin

This user can add, remove, and edit products.

## Automated Tests

The system includes a series of automated tests. To run them, use the command:

   python3 -m tests.test_app

You can run the tests both inside and outside of Docker, in the `/src` directory.
