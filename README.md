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
└── requirements.txt```
