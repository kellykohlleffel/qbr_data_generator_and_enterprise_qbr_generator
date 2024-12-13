import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from pathlib import Path

class QBRDataGenerator:
    def __init__(self, num_records=750):
        self.num_records = num_records
        np.random.seed(42)
        
    def generate_dates(self, start):
        date_list = []
        current = start
        for _ in range(self.num_records):
            current += timedelta(days=random.randint(0, 3))
            date_list.append(current)
        return date_list

    def generate_company_data(self):
        companies = []
        industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail']
        sizes = ['Small', 'Medium', 'Enterprise']
        
        for i in range(self.num_records):
            company = {
                'company_id': f'COMP{i:04d}',
                'company_name': f'Company {i:04d}',
                'industry': random.choice(industries),
                'size': random.choice(sizes),
                'contract_value': random.randint(10000, 100000)
            }
            companies.append(company)
        return companies

    def generate_data(self):
        start_date = datetime(2023, 1, 1)
        dates = self.generate_dates(start_date)
        companies = self.generate_company_data()
        
        data = []
        for i in range(self.num_records):
            # Base company info
            record = companies[i].copy()
            
            # Time period
            quarter = (dates[i].month - 1) // 3 + 1
            record['date'] = dates[i].strftime('%Y-%m-%d')
            record['quarter'] = f'Q{quarter}'
            record['year'] = dates[i].year
            
            # HubSpot deal metrics
            record['deal_stage'] = random.choice(['Implementation', 'Live', 'At Risk', 'Stable'])
            record['renewal_probability'] = random.randint(60, 100)
            record['upsell_opportunity'] = random.choice([0, 5000, 10000, 15000, 20000])
            
            # Jira product usage metrics
            record['active_users'] = random.randint(5, 100)
            record['feature_adoption_rate'] = round(random.uniform(0.4, 0.95), 2)
            record['custom_integrations'] = random.randint(0, 5)
            record['pending_feature_requests'] = random.randint(0, 10)
            
            # Zendesk support metrics
            record['ticket_volume'] = random.randint(5, 50)
            record['avg_resolution_time_hours'] = round(random.uniform(1, 48), 1)
            record['csat_score'] = round(random.uniform(3.5, 5.0), 1)
            record['sla_compliance_rate'] = round(random.uniform(0.8, 1.0), 2)
            
            # Calculated metrics
            record['health_score'] = round(
                (record['renewal_probability'] * 0.3 +
                 record['feature_adoption_rate'] * 100 * 0.3 +
                 record['sla_compliance_rate'] * 100 * 0.2 +
                 (record['csat_score'] / 5 * 100) * 0.2),
                1
            )
            
            data.append(record)
            
        return pd.DataFrame(data)

    def save_data(self, df, filename='qbr_sample_data.csv'):
        # Create output directory if it doesn't exist
        output_dir = Path(__file__).parent.parent / 'output'
        output_dir.mkdir(exist_ok=True)
        
        # Save the file
        output_path = output_dir / filename
        df.to_csv(output_path, index=False)
        return output_path

def main():
    # Create generator and generate data
    generator = QBRDataGenerator(num_records=750)
    df = generator.generate_data()
    
    # Save data
    output_path = generator.save_data(df)
    print(f"Data has been saved to {output_path}")
    
    # Display info about the dataset
    print("\nFirst few rows of the dataset:")
    print(df.head())
    print("\nDataset info:")
    print(df.info())

if __name__ == "__main__":
    main()