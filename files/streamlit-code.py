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
    "llama3.2-3b", "claude-3-5-sonnet", "mistral-large2", "llama3.1-8b", "llama3.1-405b",
    "llama3.1-70b", "mistral-7b", "jamba-1.5-large", "mixtral-8x7b", "reka-flash", "gemma-7b"
]

CHUNK_NUMBER = [4,6,8,10,12,14,16]

QBR_TEMPLATES = ["Standard QBR", "Executive Summary Only", "Technical Deep Dive", "Customer Success Focus"]
VIEW_TYPES = ["Sales View", "Executive View", "Technical View", "Customer Success View"]

CONTEXT_CHUNKS = [4, 6, 8, 10, 12]

# Initialize Snowflake session
try:
    session = get_active_session()
except:
    st.error("Could not get active Snowflake session. Please check your connection.")
    st.stop()

def build_prompt(company_data, similar_contexts, template_type, view_type):
    """Builds a prompt with RAG context using template modifications and view-specific emphasis."""

    template_instructions = {
        "Standard QBR": """
        This is a full Quarterly Business Review (QBR) covering all key aspects, including health score analysis, adoption metrics, customer satisfaction, and strategic recommendations.
        """,
        "Executive Summary Only": """
        This QBR should be concise and high-level, focusing only on key insights, major wins, critical challenges, and high-level recommendations.
        Exclude deep technical details, adoption trends, and granular product feature analysis.
        """,
        "Technical Deep Dive": """
        This QBR should focus on technical aspects such as system architecture, integrations, API usage, performance metrics, and technical challenges.
        Prioritize technical success metrics, potential optimizations, and engineering recommendations.
        Minimize business-level overviews and executive summaries.
        """,
        "Customer Success Focus": """
        This QBR should emphasize customer engagement, product adoption, support trends, and user satisfaction.
        Focus on training needs, adoption blockers, support ticket patterns, and customer success strategies.
        Minimize in-depth technical or executive-level details.
        """
    }

    view_type_instructions = {
        "Sales View": """
        This QBR should focus on revenue impact, upsell opportunities, contract value, expansion potential, and risk mitigation.
        Prioritize key financial metrics, deal health, and strategic recommendations for account growth.
        Minimize highly technical discussions unless relevant for deal positioning.
        """,
        "Executive View": """
        This QBR should provide a high-level strategic overview, emphasizing business outcomes, financial impact, and alignment with company goals.
        Keep details concise, use bullet points, and focus on key wins, challenges, and high-level recommendations.
        Minimize operational or highly technical details.
        """,
        "Technical View": """
        This QBR should provide a deep dive into system performance, architecture, integrations, and product adoption from a technical perspective.
        Prioritize API usage, reliability metrics, infrastructure considerations, and upcoming technical improvements.
        Minimize business-oriented insights unless relevant to product engineering.
        """,
        "Customer Success View": """
        This QBR should focus on customer satisfaction, adoption trends, support tickets, training needs, and customer engagement.
        Prioritize recommendations for improving retention, reducing churn, and addressing adoption blockers.
        Minimize purely financial or highly technical content unless relevant for success strategy.
        """
    }

    view_based_sections = {
        "Sales View": """
        1. Account Health Summary  
        2. Revenue & Expansion Opportunities  
        3. Usage Trends & Adoption Insights  
        4. Competitive Positioning  
        5. Strategic Sales Recommendations  
        """,
        "Executive View": """
        1. Key Business Outcomes  
        2. ROI & Financial Impact  
        3. Adoption & Customer Engagement  
        4. Strategic Roadmap Alignment  
        5. High-Level Recommendations  
        """,
        "Technical View": """
        1. System Performance & API Usage  
        2. Infrastructure & Security Considerations  
        3. Feature Adoption & Implementation Status  
        4. Engineering Challenges & Optimization Strategies  
        5. Technical Roadmap & Upcoming Enhancements  
        """,
        "Customer Success View": """
        1. Customer Engagement & Satisfaction Metrics  
        2. Product Adoption & User Retention  
        3. Support Trends & Resolution Efficiency  
        4. Training & Enablement Opportunities  
        5. Customer Success Strategy & Next Steps  
        """
    }

    qbr_type_instructions = template_instructions.get(template_type, "")
    view_specific_instructions = view_type_instructions.get(view_type, "")
    dynamic_sections = view_based_sections.get(view_type, "1. Executive Summary\n2. Business Impact\n3. Strategic Recommendations")

    prompt = f"""
    You are an expert business analyst creating a Quarterly Business Review (QBR). 
    Generate a {template_type} QBR using the following data and format:

    {qbr_type_instructions}

    {view_specific_instructions}

    Company Data:
    {company_data}

    Historical Context:
    {similar_contexts if similar_contexts else 'No historical context available'}

    Structure the QBR based on {view_type}, prioritizing the most relevant insights.
    
    Use the following section structure:
    {dynamic_sections}

    Format the QBR professionally with clear section headers and bullet points for key insights.
    Prioritize the most relevant information for {view_type} and {template_type}.
    """

    return prompt

def get_company_data(company_name):
    """Retrieve company data from Snowflake."""
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

def generate_qbr_content(company_data, similar_contexts, template_type, view_type, selected_model):
    """Generate QBR content using Snowflake Cortex."""
    try:
        prompt = build_prompt(company_data, similar_contexts, template_type, view_type)
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

import streamlit as st

def main():
    st.set_page_config(layout="wide", page_title="Enterprise QBR Generator")
    
    # Initialize session state
    if 'qbr_history' not in st.session_state:
        st.session_state.qbr_history = []
    
    # Title and Description
    st.title("🎯 Enterprise QBR Generator")
    st.write("""
    Generate comprehensive, data-driven Quarterly Business Reviews using Fivetran and Snowflake Cortex. 
    This Streamlit in Snowflake Gen AI Data App combines sales data, support data, product data, 
    current metrics, and predictive insights to create instant, standardized, and actionable QBRs.
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

        # Add spacing before branding text
        for _ in range(2):
            st.write("")

        # Branding Text (Above the logo)
        st.markdown(
            "<h4 style='text-align: center; font-weight: normal;'>Fivetran | Snowflake</h4>", 
            unsafe_allow_html=True
        )

        # Add spacing before logo
        for _ in range(1):
            st.write("")

        # Correct logo URL
        logo_url = "https://i.imgur.com/9lS8Y34.png"

        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="{logo_url}" width="150">
            </div>
            """,
            unsafe_allow_html=True
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
                            view_type,
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