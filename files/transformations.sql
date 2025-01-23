/** Transformation #1 - Create the qbr_data_single_string table and the qbr_information column using concat and prefixes for columns (creates an "unstructured" doc for each account) **
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
    FROM QBR_DATA;

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