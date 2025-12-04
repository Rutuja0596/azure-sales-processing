import azure.functions as func
import pandas as pd
import json
import logging
import io

app = func.FunctionApp()

@app.function_name(name="validateSalesData")
@app.route(route="validate", methods=["POST"])
def validate_sales_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get CSV from request
        req_body = req.get_body().decode('utf-8')
        
        # Parse CSV
        df = pd.read_csv(io.StringIO(req_body))
        
        # Validate required fields
        required_fields = ['TransactionID', 'ProductName', 'Amount']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            return func.HttpResponse(
                json.dumps({
                    "validationResult": "Invalid Data",
                    "message": f"Missing required fields: {missing_fields}",
                    "timestamp": pd.Timestamp.now().isoformat()
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate amounts
        if 'Amount' in df.columns:
            # Check for non-numeric values
            try:
                df['Amount'] = pd.to_numeric(df['Amount'])
            except:
                return func.HttpResponse(
                    json.dumps({
                        "validationResult": "Invalid Data",
                        "message": "Amount contains non-numeric values",
                        "timestamp": pd.Timestamp.now().isoformat()
                    }),
                    status_code=400,
                    mimetype="application/json"
                )
            
            # Check for negative values
            negative_rows = df[df['Amount'] < 0]
            if not negative_rows.empty:
                return func.HttpResponse(
                    json.dumps({
                        "validationResult": "Invalid Data",
                        "message": f"Found {len(negative_rows)} rows with negative amounts",
                        "invalid_transactions": negative_rows['TransactionID'].tolist(),
                        "timestamp": pd.Timestamp.now().isoformat()
                    }),
                    status_code=400,
                    mimetype="application/json"
                )
        
        # Success response
        return func.HttpResponse(
            json.dumps({
                "validationResult": "Validation Passed",
                "message": f"Successfully validated {len(df)} records",
                "timestamp": pd.Timestamp.now().isoformat(),
                "summary": {
                    "total_transactions": len(df),
                    "total_amount": df['Amount'].sum() if 'Amount' in df.columns else 0,
                    "unique_products": df['ProductName'].nunique() if 'ProductName' in df.columns else 0
                }
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Validation error: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "validationResult": "Invalid Data",
                "message": f"Error processing file: {str(e)}",
                "timestamp": pd.Timestamp.now().isoformat()
            }),
            status_code=500,
            mimetype="application/json"
        )
