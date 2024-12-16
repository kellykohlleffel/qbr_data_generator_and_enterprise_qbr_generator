import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

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
    
    def generate_expiration_date(self, start_date):
        # Typically 1-year contract
        return start_date + timedelta(days=365)

    def generate_company_data(self):
        companies = []
        
        # Industry-specific company name lists
        tech_names = [
            'Cloud Nexus', 'Digital Frontier', 'Quantum Systems', 'Cyber Logic', 
            'Data Dynamics', 'Tech Matrix', 'AI Solutions', 'Silicon Bridge',
            'Network Atlas', 'Binary Systems', 'Cloud Forge', 'Cyber Peak',
            'Data Sphere', 'Edge Computing', 'Future Stack'
        ]
        
        healthcare_names = [
            'MediCare Plus', 'Health Dynamics', 'Care Solutions', 'Wellness Systems',
            'Med Analytics', 'Health Innovations', 'Care Matrix', 'Vitality Group',
            'Medical Dynamics', 'Health Metrics', 'Patient Care Pro', 'BioTech Solutions',
            'Health Catalyst', 'Care Connect', 'Wellness Partners'
        ]
        
        finance_names = [
            'Capital Partners', 'Wealth Metrics', 'Finance Direct', 'Investment Logic',
            'Asset Analytics', 'Wealth Dynamics', 'Capital Forge', 'Finance Focus',
            'Investment Core', 'Wealth Systems', 'Capital Matrix', 'Finance Analytics',
            'Asset Partners', 'Wealth Logic', 'Investment Direct'
        ]
        
        manufacturing_names = [
            'Industrial Systems', 'Manufacturing Plus', 'Production Pro', 'Factory Focus',
            'Industrial Dynamics', 'Manufacturing Logic', 'Production Systems', 'Assembly Tech',
            'Industrial Solutions', 'Manufacturing Core', 'Production Analytics', 'Factory Systems',
            'Industrial Matrix', 'Manufacturing Edge', 'Production Dynamics'
        ]
        
        retail_names = [
            'Retail Solutions', 'Commerce Pro', 'Market Systems', 'Retail Dynamics',
            'Commerce Logic', 'Market Focus', 'Retail Analytics', 'Commerce Direct',
            'Market Plus', 'Retail Core', 'Commerce Systems', 'Market Dynamics',
            'Retail Matrix', 'Commerce Analytics', 'Market Solutions'
        ]
        
        # Create mapping of industries to their name lists
        industry_names = {
            'Technology': tech_names,
            'Healthcare': healthcare_names,
            'Finance': finance_names,
            'Manufacturing': manufacturing_names,
            'Retail': retail_names
        }
        
        # Track used names per industry to avoid duplicates
        used_names = {industry: [] for industry in industry_names.keys()}
        
        for i in range(self.num_records):
            # Select industry first
            industry = random.choice(list(industry_names.keys()))
            
            # Get available names for this industry
            available_names = [n for n in industry_names[industry] if n not in used_names[industry]]
            
            # If we've used all names, reset the used names for this industry
            if not available_names:
                used_names[industry] = []
                available_names = industry_names[industry]
            
            # Select and mark name as used
            company_name = random.choice(available_names)
            used_names[industry].append(company_name)
            
            company = {
                'company_id': f'COMP{i:04d}',
                'company_name': company_name,
                'industry': industry,
                'size': random.choice(['Small', 'Medium', 'Enterprise']),
                'contract_value': random.randint(10000, 100000)
            }
            companies.append(company)
            
        return companies

    def generate_meddicc_data(self):
        """Generate MEDDICC-related fields"""
        return {
            # Metrics
            'success_metrics_defined': random.choice([True, False]),
            'roi_calculated': random.choice([True, False]),
            'estimated_roi_value': random.randint(50000, 500000) if random.random() > 0.3 else 0,
            
            # Economic Buyer
            'economic_buyer_identified': random.choice([True, False]),
            'executive_sponsor_engaged': random.choice([True, False]),
            'decision_maker_level': random.choice(['C-Level', 'VP', 'Director', 'Manager']),
            
            # Decision Process
            'decision_process_documented': random.choice([True, False]),
            'next_steps_defined': random.choice([True, False]),
            'decision_timeline_clear': random.choice([True, False]),
            
            # Decision Criteria
            'technical_criteria_met': random.choice([True, False]),
            'business_criteria_met': random.choice([True, False]),
            'success_criteria_defined': random.choice([
                'Cost Reduction', 'Revenue Growth', 'Efficiency Gains', 
                'Risk Mitigation', 'Customer Satisfaction', 'Time Savings'
            ]),
            
            # Identified Pain
            'pain_points_documented': random.choice([
                'Manual Processes', 'Data Accuracy', 'Reporting Delays',
                'Customer Churn', 'Resource Constraints', 'Compliance Risk'
            ]),
            'pain_impact_level': random.choice(['High', 'Medium', 'Low']),
            'urgency_level': random.choice(['High', 'Medium', 'Low']),
            
            # Champion
            'champion_identified': random.choice([True, False]),
            'champion_level': random.choice(['C-Level', 'VP', 'Director', 'Manager']),
            'champion_engagement_score': random.randint(1, 5),
            
            # Competition
            'competitive_situation': random.choice(['Single', 'Multiple', 'None']),
            'competitive_position': random.choice(['Leader', 'Strong', 'Weak'])
        }

    def add_control_records(self, data):
        control_records = [
            {
                'company_id': 'COMP0750',
                'company_name': 'Kohlleffel Inc',
                'industry': 'Technology',
                'size': 'Small',
                'contract_value': 150000,
                'contract_start_date': '2024-02-01',
                'contract_expiration_date': '2025-01-31',
                'qbr_quarter': 'Q4',
                'qbr_year': 2024
            },
            {
                'company_id': 'COMP0751',
                'company_name': 'Hrncir Inc',
                'industry': 'Technology',
                'size': 'Small',
                'contract_value': 160000,
                'contract_start_date': '2024-02-01',
                'contract_expiration_date': '2025-01-31',
                'qbr_quarter': 'Q4',
                'qbr_year': 2024
            },
            {
                'company_id': 'COMP0752',
                'company_name': 'Millman Inc',
                'industry': 'Technology',
                'size': 'Small',
                'contract_value': 170000,
                'contract_start_date': '2024-02-01',
                'contract_expiration_date': '2025-01-31',
                'qbr_quarter': 'Q4',
                'qbr_year': 2024
            },
            {
                'company_id': 'COMP0753',
                'company_name': 'Tony Kelly Inc',
                'industry': 'Technology',
                'size': 'Small',
                'contract_value': 180000,
                'contract_start_date': '2024-02-01',
                'contract_expiration_date': '2025-01-31',
                'qbr_quarter': 'Q4',
                'qbr_year': 2024
            },
            {
                'company_id': 'COMP0754',
                'company_name': 'Kai Lee Inc',
                'industry': 'Technology',
                'size': 'Small',
                'contract_value': 190000,
                'contract_start_date': '2024-02-01',
                'contract_expiration_date': '2025-01-31',
                'qbr_quarter': 'Q4',
                'qbr_year': 2024
            }
        ]
        
        # Generate random data for all fields not specified above for all control records
        for record in control_records:
            record.update({
                'deal_stage': random.choice(['Implementation', 'Live', 'At Risk', 'Stable']),
                'renewal_probability': random.randint(60, 100),
                'upsell_opportunity': random.choice([0, 5000, 10000, 15000, 20000]),
                'active_users': random.randint(5, 100),
                'feature_adoption_rate': round(random.uniform(0.4, 0.95), 2),
                'custom_integrations': random.randint(0, 5),
                'pending_feature_requests': random.randint(0, 10),
                'ticket_volume': random.randint(5, 50),
                'avg_resolution_time_hours': round(random.uniform(1, 48), 1),
                'csat_score': round(random.uniform(3.5, 5.0), 1),
                'sla_compliance_rate': round(random.uniform(0.8, 1.0), 2),
            })
            
            # Add MEDDICC data
            record.update(self.generate_meddicc_data())
            
            # Calculate health score
            record['health_score'] = round(
                (record['renewal_probability'] * 0.3 +
                 record['feature_adoption_rate'] * 100 * 0.3 +
                 record['sla_compliance_rate'] * 100 * 0.2 +
                 (record['csat_score'] / 5 * 100) * 0.2),
                1
            )
            
        return data + control_records

    def generate_data(self):
        start_date = datetime(2023, 2, 1)  # Starting with fiscal year 2023
        dates = self.generate_dates(start_date)
        companies = self.generate_company_data()
        
        data = []
        for i in range(self.num_records):
            # Base company info
            record = companies[i].copy()
            
            # Contract dates
            contract_start_date = dates[i]
            record['contract_start_date'] = contract_start_date.strftime('%Y-%m-%d')
            record['contract_expiration_date'] = self.generate_expiration_date(contract_start_date).strftime('%Y-%m-%d')
            
            # QBR Period (using fiscal year)
            month = dates[i].month
            # Adjust month for fiscal year (Feb = 1, Jan = 12)
            fiscal_month = (month - 2) % 12 + 1
            fiscal_quarter = (fiscal_month - 1) // 3 + 1
            fiscal_year = dates[i].year if month >= 2 else dates[i].year - 1
            
            record['qbr_quarter'] = f'Q{fiscal_quarter}'
            record['qbr_year'] = fiscal_year
            
            # Other metrics
            record['deal_stage'] = random.choice(['Implementation', 'Live', 'At Risk', 'Stable'])
            record['renewal_probability'] = random.randint(60, 100)
            record['upsell_opportunity'] = random.choice([0, 5000, 10000, 15000, 20000])
            
            record['active_users'] = random.randint(5, 100)
            record['feature_adoption_rate'] = round(random.uniform(0.4, 0.95), 2)
            record['custom_integrations'] = random.randint(0, 5)
            record['pending_feature_requests'] = random.randint(0, 10)
            
            record['ticket_volume'] = random.randint(5, 50)
            record['avg_resolution_time_hours'] = round(random.uniform(1, 48), 1)
            record['csat_score'] = round(random.uniform(3.5, 5.0), 1)
            record['sla_compliance_rate'] = round(random.uniform(0.8, 1.0), 2)
            
            # Add MEDDICC data
            record.update(self.generate_meddicc_data())
            
            # Calculate health score
            record['health_score'] = round(
                (record['renewal_probability'] * 0.3 +
                 record['feature_adoption_rate'] * 100 * 0.3 +
                 record['sla_compliance_rate'] * 100 * 0.2 +
                 (record['csat_score'] / 5 * 100) * 0.2),
                1
            )
            
            data.append(record)
            
        # Add control records
        data = self.add_control_records(data)
        
        return pd.DataFrame(data)

def main():
    # Create generator and generate data
    generator = QBRDataGenerator(num_records=750)
    df = generator.generate_data()
    
    # Save to CSV
    output_filename = 'qbr_sample_data.csv'
    df.to_csv(f'output/{output_filename}', index=False)
    print(f"Data has been saved to output/{output_filename}")
    
    # Display info about the dataset
    print("\nFirst few rows of the dataset:")
    print(df.head())
    print("\nLast few rows (control records):")
    print(df.tail())
    print("\nDataset info:")
    print(df.info())

if __name__ == "__main__":
    main()