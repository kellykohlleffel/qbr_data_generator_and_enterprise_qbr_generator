#
# Fivetran Snowflake Cortex Streamlit Lab
# Build a QBR Generator Application
#

import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import time

# Configuration Constants
MODELS = [
    "llama3.2-3b",
    "claude-3-5-sonnet",
    "mistral-large2",
    "llama3.1-8b",
    "llama3.1-405b",
    "llama3.1-70b",
    "mistral-7b",
    "jamba-1.5-large",
    "mixtral-8x7b",
    "reka-flash",
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
        FROM QBR_DATA
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
                    (SELECT QBR_EMBEDDINGS FROM QBR_DATA_VECTORS WHERE company_name = ?)
                ) as similarity
            FROM QBR_DATA_VECTORS
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
        FROM QBR_DATA
        ORDER BY COMPANY_NAME
        """
        companies_df = session.sql(company_query).to_pandas()
        selected_company = st.selectbox(
            "Select Company",
            options=[""] + companies_df['COMPANY_NAME'].tolist(),
            help="Type to search for a specific company"
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