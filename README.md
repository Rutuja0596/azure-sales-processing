# azure-sales-processing

```azure-sales-processing/
├── .github/workflows/
│   └── deploy.yml           # GitHub Actions workflow
├── infrastructure/
│   ├── main.bicep           # Azure infrastructure code
│   └── parameters.json      # Deployment parameters
├── src/
│   ├── function/            # Azure Function code
│   │   └── validate_sales.py
│   ├── adf/                 # Data Factory pipeline
│   │   └── pipeline.json
│   └── logicapp/            # Logic App definition
│       └── workflow.json
├── scripts/
│   ├── simulate.py          # Local simulation
│   └── test_data.csv        # Sample data
├── docs/
│   ├── architecture.md
│   └── deployment.md
├── README.md
└── requirements.txt
```


# Azure Sales Data Processing Solution

## Overview
Complete implementation of daily sales data processing using Azure services. This solution automates the validation and processing of CSV sales files.

## Architecture
CSV Files → Azure Blob Storage → Azure Data Factory → Azure Functions → Logic Apps → Email Notifications
↓
Azure Monitor (Logging)


## Components
1. **Azure Blob Storage** - Stores CSV files in `sales-files` container
2. **Azure Data Factory** - Orchestrates the ETL pipeline
3. **Azure Functions** - Validates data quality
4. **Azure Logic Apps** - Sends email notifications
5. **Azure Monitor** - Tracks execution and errors

## Local Simulation
Run the simulation locally to test the logic:


# Install requirements
```pip install pandas```

# Run simulation
`python scripts/simulate.py`
