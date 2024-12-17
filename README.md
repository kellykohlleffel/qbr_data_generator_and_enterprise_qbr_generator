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

### Company Information (SFDC, Hubspot, Dynamics 365)
* company_id (Primary Key, format: 'COMPxxxx')
* company_name (Industry-specific naming convention)
* industry (Technology, Healthcare, Finance, Manufacturing, Retail)
* size (Small, Medium, Enterprise)
* contract_value
* contract_start_date
* contract_expiration_date

### Deal/Financial Data (SFDC, Hubspot, Dynamics 365)
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

## Transformations in Snowflake for QBR Generator
```
/** Transformation #1 - Create the qbr_data_single_string table and the qbr_information column using concat and prefixes for columns (creates an "unstructured" doc for each winery/vineyard)
/** Create each qbr review as a single string vs multiple fields **/
CREATE OR REPLACE TABLE QBR_DATA_SINGLE_STRING AS 
    SELECT company_name, CONCAT(
        'The company name is ', IFNULL(company_name, 'unknown'), '.',
        ' The company ID is ', IFNULL(company_id, 'unknown'), '.',
        ' This is a ', IFNULL(size, 'unknown'), ' ', IFNULL(industry, 'unknown'), ' company.',
        ' The contract started on ', IFNULL(contract_start_date, 'unknown'), ' and expires on ', IFNULL(contract_expiration_date, 'unknown'), '.',
        ' The annual contract value is $', IFNULL(contract_value::STRING, 'unknown'), '.',
        ' The current deal stage is ', IFNULL(deal_stage, 'unknown'), '.',
        ' The renewal probability is ', IFNULL(renewal_probability::STRING, 'unknown'), '%.',
        ' The identified upsell opportunity is $', IFNULL(upsell_opportunity::STRING, 'unknown'), '.',
        ' The number of active users is ', IFNULL(active_users::STRING, 'unknown'), '.',
        ' The feature adoption rate is ', IFNULL(ROUND(feature_adoption_rate * 100, 1)::STRING, 'unknown'), '%.',
        ' The number of custom integrations is ', IFNULL(custom_integrations::STRING, 'unknown'), '.',
        ' The number of pending feature requests is ', IFNULL(pending_feature_requests::STRING, 'unknown'), '.',
        ' The number of support tickets is ', IFNULL(ticket_volume::STRING, 'unknown'), '.',
        ' The average resolution time is ', IFNULL(avg_resolution_time_hours::STRING, 'unknown'), ' hours.',
        ' The CSAT score is ', IFNULL(csat_score::STRING, 'unknown'), ' out of 5.',
        ' The SLA compliance rate is ', IFNULL(ROUND(sla_compliance_rate * 100, 1)::STRING, 'unknown'), '%.',
        ' Success metrics defined: ', IFNULL(success_metrics_defined::STRING, 'unknown'), '.',
        ' ROI calculated: ', IFNULL(roi_calculated::STRING, 'unknown'), '.',
        ' Estimated ROI value: $', IFNULL(estimated_roi_value::STRING, 'unknown'), '.',
        ' Economic buyer identified: ', IFNULL(economic_buyer_identified::STRING, 'unknown'), '.',
        ' Executive sponsor engaged: ', IFNULL(executive_sponsor_engaged::STRING, 'unknown'), '.',
        ' The decision maker level is ', IFNULL(decision_maker_level, 'unknown'), '.',
        ' Decision process documented: ', IFNULL(decision_process_documented::STRING, 'unknown'), '.',
        ' Next steps defined: ', IFNULL(next_steps_defined::STRING, 'unknown'), '.',
        ' Decision timeline clear: ', IFNULL(decision_timeline_clear::STRING, 'unknown'), '.',
        ' Technical criteria met: ', IFNULL(technical_criteria_met::STRING, 'unknown'), '.',
        ' Business criteria met: ', IFNULL(business_criteria_met::STRING, 'unknown'), '.',
        ' The success criteria is defined as ', IFNULL(success_criteria_defined, 'unknown'), '.',
        ' The documented pain points are ', IFNULL(pain_points_documented, 'unknown'), '.',
        ' The pain impact level is ', IFNULL(pain_impact_level, 'unknown'), '.',
        ' The urgency level is ', IFNULL(urgency_level, 'unknown'), '.',
        ' Champion identified: ', IFNULL(champion_identified::STRING, 'unknown'), '.',
        ' The champion level is ', IFNULL(champion_level, 'unknown'), '.',
        ' The champion engagement score is ', IFNULL(champion_engagement_score::STRING, 'unknown'), ' out of 5.',
        ' The competitive situation is ', IFNULL(competitive_situation, 'unknown'), '.',
        ' Our competitive position is ', IFNULL(competitive_position, 'unknown'), '.',
        ' The overall health score is ', IFNULL(health_score::STRING, 'unknown'), '.',
        ' This QBR covers ', IFNULL(qbr_quarter, 'unknown'), ' ', IFNULL(qbr_year::STRING, 'unknown'), '.'
    ) AS qbr_information
    FROM HOL_DATABASE.A_QBR_TEST_SALES.QBR_DATA;

/** Transformation #2 - Using the Snowflake Cortex embed_text_768 LLM function, creates embeddings from the newly created qbr_information column and create a vector table called qbr_embeddings.
/** Create the vector table from the qbr_information column **/
      CREATE or REPLACE TABLE qbr_data_vectors AS 
            SELECT company_name, qbr_information, 
            snowflake.cortex.EMBED_TEXT_768('e5-base-v2', qbr_information) as QBR_EMBEDDINGS 
            FROM qbr_data_single_string;

/** Select a control record to see the LLM-friendly "text" document table and the embeddings table **/
    SELECT *
    FROM qbr_data_vectors
    WHERE qbr_information LIKE '%company_name is Kohlleffel Inc%';
```

## Streamlit in Snowflake QBR Generator Application
```
import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import time

# Configuration Constants
MODELS = [
    "reka-flash",
    "llama3.2-3b",
    "llama3.1-8b",
    "jamba-1.5-large",
    "llama3.1-70b",
    "llama3.1-405b",
    "mistral-7b",
    "mixtral-8x7b",
    "mistral-large2",
    "snowflake-arctic",
    "gemma-7b"
]

CHUNK_NUMBER = [4,6,8,10,12,14,16]

# Configuration Constants
QBR_TEMPLATES = [
    "Standard QBR",
    "Executive Summary Only",
    "Technical Deep Dive",
    "Customer Success Focus"
]

VIEW_TYPES = [
    "Executive View",
    "Technical View",
    "Customer Success View",
    "Sales View"
]

CONTEXT_CHUNKS = [4, 6, 8, 10, 12]

# Initialize Snowflake session
try:
    session = get_active_session()
except:
    st.error("Could not get active Snowflake session. Please check your connection.")
    st.stop()

def get_company_data(company_name):
    """Retrieve company data from Snowflake"""
    try:
        metrics_query = """
        SELECT 
            HEALTH_SCORE, 
            CONTRACT_VALUE, 
            CSAT_SCORE, 
            ACTIVE_USERS,
            FEATURE_ADOPTION_RATE,
            TICKET_VOLUME,
            RENEWAL_PROBABILITY,
            QBR_QUARTER,
            QBR_YEAR
        FROM HOL_DATABASE.A_QBR_TEST_SALES.QBR_DATA
        WHERE COMPANY_NAME = ?
        """
        return session.sql(metrics_query, params=[company_name]).to_pandas()
    except Exception as e:
        st.error(f"Error retrieving company data: {str(e)}")
        return None

def get_similar_contexts(company_name, num_chunks):
    """Retrieve similar QBR contexts using vector similarity"""
    try:
        similarity_query = """
        WITH similarity_cte AS (
            SELECT 
                company_name,
                qbr_information,
                vector_cosine_similarity(
                    QBR_EMBEDDINGS,
                    (SELECT QBR_EMBEDDINGS FROM HOL_DATABASE.A_QBR_TEST_SALES.QBR_DATA_VECTORS WHERE company_name = ?)
                ) as similarity
            FROM HOL_DATABASE.A_QBR_TEST_SALES.QBR_DATA_VECTORS
            WHERE company_name != ?
            QUALIFY ROW_NUMBER() OVER (ORDER BY similarity DESC) <= ?
        )
        SELECT qbr_information
        FROM similarity_cte
        """
        return session.sql(similarity_query, params=[company_name, company_name, num_chunks]).to_pandas()
    except Exception as e:
        st.error(f"Error retrieving similar contexts: {str(e)}")
        return None

def generate_qbr_content(company_data, similar_contexts, template_type, selected_model):
    """Generate QBR content using Snowflake Cortex"""
    try:
        prompt = f"""
        You are an expert business analyst creating a Quarterly Business Review (QBR). 
        Generate a detailed {template_type} QBR using the following data and format:

        Company Data:
        {company_data.to_string()}
        
        Historical Context:
        {similar_contexts.to_string() if similar_contexts is not None else 'No historical context available'}
        
        Please create a comprehensive QBR with these specific sections:

        1. Executive Summary
        - Overall health assessment (use the health score provided)
        - Key wins from this quarter (based on metrics)
        - Critical challenges identified
        - High-priority strategic recommendations

        2. Business Impact Analysis
        - ROI analysis based on current usage
        - Analysis of efficiency gains/losses
        - Identified business problems and their impact
        - Value realization metrics

        3. Product Adoption Review
        - Detailed feature usage analysis
        - Implementation progress report
        - Analysis of adoption rates and trends
        - Identified adoption blockers and solutions

        4. Support and Success Analysis
        - Support ticket trend analysis
        - Resolution efficiency metrics
        - Customer satisfaction analysis
        - Outstanding issues and their business impact

        5. Strategic Recommendations
        - Expansion opportunities
        - Risk mitigation strategies
        - Training and enablement needs
        - Product roadmap alignment recommendations

        6. Action Items
        - Specific tasks for both customer and vendor teams
        - Clear implementation timeline
        - Required resources and owners
        - Expected outcomes and success metrics

        Format the QBR professionally with clear section headers and bullet points for key items.
        Include specific metrics and data points to support all observations and recommendations.
        """
        
        cortex_query = """
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            ?,
            ?
        ) as response
        """
        
        response = session.sql(cortex_query, params=[selected_model, prompt]).collect()[0][0]
        return response
    except Exception as e:
        st.error(f"Error generating QBR content: {str(e)}")
        return None

def display_metrics_dashboard(metrics_df):
    """Display key metrics dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Health Score", 
            f"{metrics_df['HEALTH_SCORE'].iloc[0]:.1f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Contract Value", 
            f"${metrics_df['CONTRACT_VALUE'].iloc[0]:,.2f}",
            delta=None
        )
    
    with col3:
        st.metric(
            "CSAT Score", 
            f"{metrics_df['CSAT_SCORE'].iloc[0]:.1f}",
            delta=None
        )
    
    with col4:
        st.metric(
            "Active Users", 
            int(metrics_df['ACTIVE_USERS'].iloc[0]),
            delta=None
        )

def main():
    st.set_page_config(layout="wide", page_title="Enterprise QBR Generator")
    
    # Initialize session state
    if 'qbr_history' not in st.session_state:
        st.session_state.qbr_history = []
    
    # Title and Description
    st.title("🎯 Enterprise QBR Generator")
    st.write("""
    Generate comprehensive, data-driven Quarterly Business Reviews using advanced analytics 
    and machine learning. This tool combines historical data, current metrics, and predictive
    insights to create actionable QBRs.
    """)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("QBR Configuration")
        
        # Business Settings
        st.subheader("Business Settings")
        # Company Selection
        company_query = """
        SELECT DISTINCT COMPANY_NAME
        FROM HOL_DATABASE.A_QBR_TEST_SALES.QBR_DATA
        ORDER BY COMPANY_NAME
        """
        companies_df = session.sql(company_query).to_pandas()
        selected_company = st.selectbox(
            "Select Company",
            companies_df['COMPANY_NAME'].tolist()
        )
        
        # Template Selection
        template_type = st.selectbox(
            "QBR Template",
            QBR_TEMPLATES
        )
        
        view_type = st.selectbox(
            "View Type",
            VIEW_TYPES
        )
        
        # Admin Settings
        st.subheader("Admin Settings")
        
        # Model Selection
        selected_model = st.selectbox(
            "Select Snowflake Cortex Model:",
            MODELS,
            help="Choose the LLM model for QBR generation"
        )
        
        # Chunk Selection
        selected_chunks = st.selectbox(
            "Select Context Chunks:",
            CHUNK_NUMBER,
            help="Number of context chunks to include (200-400 tokens per chunk)"
        )
        
        # Advanced Options
        with st.expander("Advanced Options"):
            use_historical = st.checkbox(
                "Include Historical Context",
                help="Use similar QBRs for enhanced insights"
            )
            
            include_validation = st.checkbox(
                "Enable Data Validation",
                help="Add validation steps to the QBR process"
            )
    
    # Main Content Area
    tabs = st.tabs(["QBR Generation", "Historical QBRs", "Settings"])
    
    with tabs[0]:
        if selected_company:
            # Get and display company metrics
            company_data = get_company_data(selected_company)
            if company_data is not None:
                display_metrics_dashboard(company_data)
                
                # QBR Generation Button
                if st.button("Generate QBR"):
                    with st.spinner("Generating QBR..."):
                        # Get similar contexts if enabled
                        similar_contexts = None
                        if use_historical:
                            similar_contexts = get_similar_contexts(
                                selected_company,
                                selected_chunks
                            )
                        
                        # Generate QBR content
                        qbr_content = generate_qbr_content(
                            company_data,
                            similar_contexts,
                            template_type,
                            selected_model
                        )
                        
                        if qbr_content:
                            # Display generated QBR
                            st.header(f"Quarterly Business Review: {selected_company}")
                            st.write(qbr_content)
                            
                            # Add download button
                            st.download_button(
                                label="Download QBR",
                                data=qbr_content,
                                file_name=f"QBR_{selected_company}_{pd.Timestamp.now().strftime('%Y%m%d')}.md",
                                mime="text/markdown"
                            )
                            
                            # Save to history
                            st.session_state.qbr_history.append({
                                'company': selected_company,
                                'date': pd.Timestamp.now(),
                                'content': qbr_content,
                                'template': template_type,
                                'view_type': view_type
                            })
    
    with tabs[1]:
        if st.session_state.qbr_history:
            for qbr in reversed(st.session_state.qbr_history):
                with st.expander(f"{qbr['company']} - {qbr['date'].strftime('%Y-%m-%d %H:%M')}"):
                    st.write(qbr['content'])
        else:
            st.info("No QBR history available")
    
    with tabs[2]:
        st.write("QBR Generation Settings")
        st.write("Configure default templates, branding, and other settings here.")

if __name__ == "__main__":
    main()
```