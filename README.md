# QBR Data Generator

A synthetic data generator for Quarterly Business Review (QBR) analysis, simulating integrated data from:
- HubSpot (Deals data)
- Jira (Product usage data)
- Zendesk (Support ticket data)

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

## Data Sources

### HubSpot (Deals Data)
* company_id
* company_name
* industry
* size
* contract_value
* deal_stage
* renewal_probability
* upsell_opportunity

### Zendesk (Support Data)
* ticket_volume
* avg_resolution_time_hours
* csat_score
* sla_compliance_rate

### Jira (Product Usage/Development)
* active_users
* feature_adoption_rate
* custom_integrations
* pending_feature_requests

### Additional Fields
* date
* quarter
* year
* health_score (calculated metric)

## Running the Generator

Generate sample data:
```bash
python src/data_generator.py
```

The generated CSV file will be saved in the `output` directory at:
```plaintext
~/Documents/GitHub/qbr-data-generator/output/qbr_sample_data.csv
```

## Sample Output

The generator creates a CSV file with 750 records. Here's how a single row looks as an unstructured document:

```plaintext
This review is for Company 0000. The customer identifier is COMP0000. They operate in the 
Healthcare industry and are classified as a Medium business. The relationship began on 
2023-01-04 and this review covers Q1 during the year 2023. Their annual contract value 
is $71,538 and the current stage of their partnership is Implementation. Based on current 
indicators, their likelihood of renewal is 88.8%. There is a potential upsell opportunity 
of $19,000. The platform is actively used by 19 users with a feature adoption rate of 
79.5%. They have implemented 1 custom integration and have submitted 1 feature request. 
Over this period, they have opened 19 support tickets. Their average ticket resolution 
time is 39.0 hours. Customer satisfaction is measured at 4.3 out of 5, and our SLA 
compliance rate with this customer is 83.0%. The overall customer health score is 72.8.
```

## Project Location
Your project will be located at:
```plaintext
~/Documents/GitHub/qbr-data-generator/
```

## Dependencies

### Core Dependencies
```plaintext
pandas==2.1.0
numpy==1.24.3
```

### Visualization Dependencies (Optional)
```plaintext
plotly==5.18.0
```

## Version Control

### Committing Changes
1. Open GitHub Desktop
2. Review changes
3. Add commit message
4. Click "Commit to main"
5. Click "Push origin" to push to GitHub

### Finding Output Files
1. Open GitHub Desktop
2. Right-click on repository
3. Select "Show in Finder"
4. Navigate to the `output` folder

## Source Code

### data_generator.py
The main script for generating synthetic QBR data can be found at:
```plaintext
src/data_generator.py
```

## Next Steps
* Review generated data for accuracy
* Customize data ranges if needed
* Add additional metrics
* Integrate with visualization tools
* Set up automated data generation pipelines

## Support
For issues or questions, please open an issue in the GitHub repository.
