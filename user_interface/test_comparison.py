import streamlit as st
import plotly.express as px

import dbConnectionModule as db

# Content for Test Comparison Tab
sensor_options = db.get_distinct_sensor_names()
if not sensor_options.empty:
    selected_sensor = st.selectbox(
        "Select a Sensor:",
        options=sensor_options["name"],
        key="sensor_test_comparison_select",
    )

    # fetch here all config ids for sesnors with dates
    config_date_options = db.get_config_ids_for_sensor_with_dates(selected_sensor)
    if not config_date_options.empty:
        selected_config_dates = st.multiselect(
            "Select Config IDs with Dates to Compare:",
            options=config_date_options["config_id_date"],
            key="config_date_select",
        )
        selected_configs = [
            cd.split(" - ")[0] for cd in selected_config_dates
        ]  # Extract config IDs from selections

        if selected_configs:
            df_comparison = db.get_sensor_data_for_multiple_tests(
                selected_sensor, selected_configs
            )
            if not df_comparison.empty:
                fig_comparison = px.line(
                    df_comparison,
                    x="normalized_timestamp",
                    y="value",
                    color="config_id",
                    title="Test Comparison for Selected Sensor",
                    labels={
                        "value": "Sensor Value",
                        "normalized_timestamp": "Minutes Since Start",
                        "config_id": "Configuration ID",
                    },
                )

                st.plotly_chart(fig_comparison, use_container_width=True)
            else:
                st.error("No data found for the selected tests.")
    else:
        st.error("No configuration IDs found for the selected sensor.")
else:
    st.error("No sensors found.")
