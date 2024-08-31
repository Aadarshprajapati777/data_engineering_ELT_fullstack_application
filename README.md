
# ELT Process Application

This project is a robust, modular, and scalable ELT (Extract, Load, Transform) process application. It is designed to handle and process data from two datasets: a Payment Report and a Merchant Tax Report (MTR). The application is built using Next.js for the front-end and FastAPI for the back-end, with a PostgreSQL database for storing the processed data.


# Setup Instructions
## Prerequisites
- Docker and Docker Compose
- Git
## Installation

Clone the Repository

```bash
git clone https://github.com/Aadarshprajapati777/data_engineering_ELT_fullstack_application.git
cd data_engineering_ELT_fullstack_application
```
Build and Run the Application
```bash
 docker-compose up -d
```
Access the Application:

- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8000/api/v1/health

## Environment Variables
Ensure the following environment variables are set in a .env file in the project root:

- look into .env.sample file and make your own .env file with your credentials similar to sample file

## Database Schema
The database consists of the following tables:

- processed_payment: Stores the refined payment data.
- processed_mtr: Stores the processed MTR file.

- merged_data: Stores the merged data of both payment and mtr files.

## API Design
 ```bash
POST /upload/: Upload and process datasets.
GET /summary/: Retrieve the summary of processed data.
GET /grouped_data/: Retrieve detailed processed data of merged table.
```

# ELT Pipeline

The ELT pipeline consists of the following steps:


## Extraction: 
Upload the Payment Report (CSV) and Merchant Tax Report (XLSX) datasets and extract the data.

## Transformation:
- Merchant Tax Report (MTR):
     -  Remove rows with Transaction Type as Cancel.
     - Rename Refund and FreeReplacement to Return
- Payment Report:
     - Remove rows with Type as Transfer.
     - Rename Type to Payment Type.
     - Assign Transaction Type as Payment.
- Merge Datasets:
     - Combine the MTR and Payment Report datasets.
## Loading
- Store the data processed payment Report to processed_payment table
- Store the data of processed MTR Report to processed_mtr table
- Store the merged data to merged_data table


## Known Issues
 - No comprehensive error handling for malformed data files.

##  Future Improvements
- Error Handling: Enhance error handling and validation for uploaded datasets.
- Performance Optimization: Optimize the ELT pipeline for larger datasets.
- Additional Features: Add more filters and data transformation options based on user feedback.

## Contact
mail to: 
```bash
geekaadarsh.dev@gmail.com
```
for any suggestion or help

# Screenshots
