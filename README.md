# QBR Data Generator

This project generates synthetic data for testing QBR (Quarterly Business Review) analysis systems. The generated data includes:
- 750 randomly generated records with industry-specific company names
- 5 control records for testing
- Data representing integration from multiple systems and MEDDICC sales qualification

## Project Setup

### Initial Setup with GitHub Desktop
1. Open GitHub Desktop
2. Click "File" > "New Repository"
3. Fill in:
   - Name: `qbr-data-generator`
   - Add a description (optional)
   - Choose your local path
   - Initialize with a README
   - Click "Create Repository"
4. Click "Open in Visual Studio Code"

### Directory Structure in VS Code
Create the following structure:
```plaintext
qbr-data-generator/
├── venv/
├── src/
│   ├── __init__.py
│   └── data_generator.py
├── output/
├── requirements.txt
└── README.md
```

Create directories and files using terminal commands:
```bash
mkdir src output
touch src/__init__.py
touch src/data_generator.py
touch requirements.txt
```

### Virtual Environment Setup
In VS Code's terminal:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Mac/Linux)
source venv/bin/activate
# OR for Windows
# .\venv\Scripts\activate

# Install required packages
pip install pandas numpy

# Save requirements
pip freeze > requirements.txt
```

### Create .gitignore
Create a new file called `.gitignore` and add:
```plaintext
venv/
__pycache__/
*.pyc
output/*.csv
.DS_Store
```

Then run:
```bash
git rm -r --cached .
git add .
git commit -m "Remove files that should be ignored"
```

## Data Sources & Fields

### Company Information
* company_id (Primary Key, format: 'COMPxxxx')
* company_name (Industry-specific naming convention)
* industry (Technology, Healthcare, Finance, Manufacturing, Retail)
* size (Small, Medium, Enterprise)
* contract_value
* contract_start_date
* contract_expiration_date

### Deal/Financial Data (HubSpot)
* deal_stage (Implementation, Live, At Risk, Stable)
* renewal_probability
* upsell_opportunity
* qbr_quarter (Based on Fiscal Year: Feb 1 - Jan 31)
* qbr_year

### Product Usage Data (Jira)
* active_users
* feature_adoption_rate
* custom_integrations
* pending_feature_requests

### Support Data (Zendesk)
* ticket_volume
* avg_resolution_time_hours
* csat_score
* sla_compliance_rate

### MEDDICC Fields

#### Metrics
* success_metrics_defined (boolean)
* roi_calculated (boolean)
* estimated_roi_value (numeric)

#### Economic Buyer
* economic_buyer_identified (boolean)
* executive_sponsor_engaged (boolean)
* decision_maker_level (C-Level, VP, Director, Manager)

#### Decision Process
* decision_process_documented (boolean)
* next_steps_defined (boolean)
* decision_timeline_clear (boolean)

#### Decision Criteria
* technical_criteria_met (boolean)
* business_criteria_met (boolean)
* success_criteria_defined (text)

#### Identified Pain
* pain_points_documented (text)
* pain_impact_level (High, Medium, Low)
* urgency_level (High, Medium, Low)

#### Champion
* champion_identified (boolean)
* champion_level (C-Level, VP, Director, Manager)
* champion_engagement_score (1-5)

#### Competition
* competitive_situation (Single, Multiple, None)
* competitive_position (Leader, Strong, Weak)

### Calculated Metrics
* health_score (Weighted calculation based on key metrics)

## Control Records
The dataset includes 5 specific control records:
1. Kohlleffel Inc
2. Hrncir Inc
3. Millman Inc
4. Tony Kelly Inc
5. Kai Lee Inc

All control records have:
- Technology industry
- Small company size
- Specific contract values
- Q4 2024 QBR period
- Contract expiration date of 2025-01-31
- All other fields randomly generated

## Running the Generator

Generate sample data:
```bash
python3 src/data_generator.py
```

The generated CSV file will be saved in the `output` directory at:
```plaintext
~/Documents/GitHub/qbr-data-generator/output/qbr_sample_data.csv
```

## Dependencies

### Core Dependencies
```plaintext
pandas==2.1.0
numpy==1.24.3
```

## Notes
- The project uses a fiscal year that begins February 1 and ends January 31
- Company names are generated based on industry for more realistic data
- Health score is calculated using weighted metrics from various sources
- Generated data includes a mix of boolean, numeric, and categorical fields
- All metric ranges are set to realistic values based on typical business scenarios

## Support
For issues or questions, please open an issue in the GitHub repository.