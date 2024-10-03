# Salary_Calculation
## Overview

The Salary Calculation System is a robust web application built using FastAPI and MongoDB, designed to streamline employee management and automate salary calculations for telesales teams. The system implements role-based access control (RBAC) to provide secure and efficient handling of employee data and payroll processing. Administrators can manage employee records, generate daily work reports, configure salary parameters, and export salary slips in PDF format, while users can access their own daily reports and salary information.

This system leverages Docker for containerization and GitHub Actions for continuous integration and deployment (CI/CD), ensuring efficient and reliable updates across development and production environments. Comprehensive testing practices using Pytest ensure that the application is secure and functions reliably.

## Features

1. User Management:

Role-based Authorization: Users can sign up with different roles (e.g., admin, user), and the system restricts access to certain features based on the user's role.

User Endpoints: Provides routes for user management such as /signup and /login.



2. Employee Management:

CRUD Operations: Administrators can create, retrieve, update, and delete employee records.

Employee Daily Reports: Daily reports can be added and retrieved for specific employees, and they include key data such as adherence, appointments, compensation, etc.



3. Daily Reports and Salary Calculations:

Static Values: Includes static values (e.g., compensation rules) that can be configured and used in salary calculations.

PDF Export: Provides a service to export salary information in PDF format, using a salary template for rendering.

Salary Template: An HTML-based template is used to generate salary slips for employees.



4. CI/CD Pipeline:

Docker Integration: The project uses Docker for containerization, ensuring consistent environments across development, testing, and production.

GitHub Actions: A CI/CD pipeline is set up with GitHub Actions, automating the process of testing and deploying the application.



5. MongoDB Database:

Collections: The database includes collections for users, employees, and daily reports.

Beanie ODM: The project uses Beanie for ODM (Object-Document Mapping) with MongoDB, allowing easy interaction with database models.



6. Unit Testing:

The project contains test cases using Pytest, ensuring functionality for the key components such as daily reports, users, employees, and the PDF export feature.



7. Configuration:

Environment Variables: Critical configuration details (e.g., MongoDB URI, email server credentials) are stored in environment variables, improving security and flexibility across different environments (development, testing, production).

## Technologies Used:

* Backend: FastAPI (Python)

* Database: MongoDB with Beanie ODM

* Authentication: JWT (JSON Web Tokens) for secure authentication and session management

* Authorization: Role-based access control with customizable user roles

* Containerization: Docker for consistent environment management

* CI/CD: GitHub Actions for automated testing, building, and deployment

* PDF Generation: HTML to PDF rendering for salary slip export

* Testing Framework: Pytest for unit and integration testing

