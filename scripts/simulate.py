import pandas as pd
import json
import os
import shutil
from datetime import datetime
import requests

class AzureSalesSimulator:
    def __init__(self):
        self.setup_directories()
        self.create_sample_data()
        
    def setup_directories(self):
        """Create local directories simulating Azure Blob Storage"""
        directories = [
            'data/sales-files',
            'data/success',
            'data/failed',
            'data/processing',
            'logs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
        print(" Created directory structure")
    
    def create_sample_data(self):
        """Create sample CSV files"""
        # Valid data
        valid_data = """TransactionID,ProductName,Quantity,Amount,SaleDate
1001,Laptop,2,1500.00,2025-03-12
1002,Mobile Phone,5,3000.00,2025-03-12
1003,Headphones,3,0,2025-03-12
1004,Monitor,1,250.50,2025-03-12
1005,Keyboard,10,45.99,2025-03-12"""
        
        # Invalid data (negative amount)
        invalid_data = """TransactionID,ProductName,Quantity,Amount,SaleDate
2001,Tablet,1,500.00,2025-03-12
2002,Camera,2,-100.00,2025-03-12
2003,Speaker,3,75.00,2025-03-12"""
        
        # Missing field data
        missing_field_data = """TransactionID,ProductName,Quantity,SaleDate
3001,Charger,5,2025-03-12
3002,Cable,10,2025-03-12"""
        
        with open('data/sales-files/valid_data.csv', 'w') as f:
            f.write(valid_data)
        
        with open('data/sales-files/invalid_data.csv', 'w') as f:
            f.write(invalid_data)
            
        with open('data/sales-files/missing_field_data.csv', 'w') as f:
            f.write(missing_field_data)
            
        print(" Created sample CSV files")
    
    def simulate_azure_function(self, file_path):
        """Simulate Azure Function validation"""
        print(f"\n🔍 [Azure Function] Validating: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            required_fields = ['TransactionID', 'ProductName', 'Amount']
            
            # Check required fields
            missing_fields = [field for field in required_fields if field not in df.columns]
            if missing_fields:
                return {
                    "validationResult": "Invalid Data",
                    "message": f"Missing fields: {missing_fields}",
                    "isValid": False
                }
            
            # Check amounts
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            negative_amounts = df[df['Amount'] < 0]
            
            if not negative_amounts.empty:
                return {
                    "validationResult": "Invalid Data",
                    "message": f"Found {len(negative_amounts)} negative amounts",
                    "invalidTransactions": negative_amounts['TransactionID'].tolist(),
                    "isValid": False
                }
            
            return {
                "validationResult": "Validation Passed",
                "message": f"Validated {len(df)} records successfully",
                "isValid": True,
                "summary": {
                    "totalTransactions": len(df),
                    "totalAmount": df['Amount'].sum(),
                    "uniqueProducts": df['ProductName'].nunique()
                }
            }
            
        except Exception as e:
            return {
                "validationResult": "Invalid Data",
                "message": f"Error: {str(e)}",
                "isValid": False
            }
    
    def simulate_data_factory_pipeline(self):
        """Simulate ADF Pipeline execution"""
        print("\n" + "="*60)
        print("Azure Data Factory Pipeline Simulation")
        print("="*60)
        
        source_files = os.listdir('data/sales-files')
        
        for file in source_files:
            if file.endswith('.csv'):
                print(f"\n Processing: {file}")
                
                # Step 1: Copy Activity
                source_path = f'data/sales-files/{file}'
                processing_path = f'data/processing/{file}'
                shutil.copy(source_path, processing_path)
                print("   [ADF Copy Activity] File copied to processing")
                
                # Step 2: Azure Function Activity
                validation_result = self.simulate_azure_function(processing_path)
                print(f"    [ADF Function Activity] Validation: {validation_result['validationResult']}")
                
                # Step 3: If Condition Activity
                if validation_result['isValid']:
                    destination = f'data/success/{file}'
                    print(f"   [ADF If Condition] Validation passed → moving to success")
                    
                    # Step 4: Logic Apps Notification
                    self.simulate_logic_apps_notification(success=True, file=file)
                else:
                    destination = f'data/failed/{file}'
                    print(f"   [ADF If Condition] Validation failed → moving to failed")
                    
                    # Step 4: Logic Apps Notification
                    self.simulate_logic_apps_notification(success=False, file=file)
                
                # Move file
                shutil.move(processing_path, destination)
                print(f"   [ADF Move Activity] File moved to: {destination}")
                
                # Log to Azure Monitor
                self.log_to_monitor(file, validation_result)
        
        print("\n" + "="*60)
        print("Pipeline execution completed")
        print("="*60)
    
    def simulate_logic_apps_notification(self, success=True, file=""):
        """Simulate Logic Apps email notification"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if success:
            subject = " Daily sales data successfully processed."
            body = f"""Sales Data Processing Report - SUCCESS

File: {file}
Processed at: {timestamp}
Status: All records validated successfully

The file has been moved to the success folder.

Next steps: Data will be loaded into the data warehouse.

---
This is an automated message from Sales Processing System."""
        else:
            subject = " Error: Sales data validation failed."
            body = f"""Sales Data Processing Report - FAILURE

File: {file}
Processed at: {timestamp}
Status: Validation failed

The file has been moved to the failed folder for manual review.

Action required: Please check the file for data quality issues.

---
This is an automated message from Sales Processing System."""
        
        print(f"   [Logic Apps] Email sent:")
        print(f"     Subject: {subject}")
        print(f"     To: operations@company.com")
    
    def log_to_monitor(self, file, validation_result):
        """Simulate Azure Monitor logging"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file": file,
            "validationResult": validation_result['validationResult'],
            "message": validation_result['message'],
            "component": "SalesProcessingPipeline"
        }
        
        log_file = 'logs/azure_monitor.json'
        
        # Load existing logs
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Add new log
        logs.append(log_entry)
        
        # Save logs
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"   [Azure Monitor] Logged: {validation_result['validationResult']}")

def main():
    print("Starting Azure Sales Processing Simulation")
    print("-" * 50)
    
    simulator = AzureSalesSimulator()
    
    # Run pipeline simulation
    simulator.simulate_data_factory_pipeline()
    
    # Show results
    print("\n Simulation Results:")
    print(f"  Success folder: {len(os.listdir('data/success'))} files")
    print(f"  Failed folder: {len(os.listdir('data/failed'))} files")
    print(f"  Logs saved to: logs/azure_monitor.json")
    
    print("\n Simulation completed successfully!")
    print("This simulates the complete Azure architecture:")

if __name__ == "__main__":
    main()
