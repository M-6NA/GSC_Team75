import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_and_process_finance_data
from utils.constants_passer import SITE_EMOJI

# :::::::::::::::::::::::::::::::::: PAGE CONFIGURATION :::::::::::::::::::::::::::::::::: 
# test
# Settings for the webpage
st.set_page_config( 
    page_title = "Home",
    layout = "wide",
    page_icon = SITE_EMOJI,

)

# Title for the page
st.title(":tangerine: GQR2 Team 75 Dashboard")
st.divider()

# ::::::::: READING THE DATAFRAME FROM data_loader.py :::::::::::
RAW_FINANCE_DF = load_and_process_finance_data()[0]
PROCESSED_FINANCE_DF = load_and_process_finance_data()[1]

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 
st.subheader("Finance")

def finance_info_section():

    # Helper function to format the annotation text with "k" for thousands and "M" for millions
    def format_value(value):
        # Determine if the original value is negative
        sign = "-" if value < 0 else ""
        # Work with the absolute value and then reapply the sign if necessary
        abs_value = abs(value)
        if abs_value >= 1_000_000:
            value_text = f"{sign}{abs_value/1_000_000:.1f}M"  # Format in millions
        elif abs_value >= 1_000:
            value_text = f"{sign}{abs_value/1_000:.1f}k"  # Format in thousands
        else:
            value_text = f"{sign}{abs_value:.1f}"  # No formatting needed for values less than 1000
        return value_text

    def line_plot(val):

        # ::::::::: FILTERING THE DATAFRAME :::::::::
        main_df = PROCESSED_FINANCE_DF.copy()
        main_df['Round'] = pd.to_numeric(main_df['Round'])
        main_df[val] = pd.to_numeric(main_df[val])

        # ::::::::: PLOTTING THE VALUE IN A LINE PLOT :::::::::::
        if val == "ROI":
            main_df[val] = main_df[val] * 100

        fig = px.line(
            main_df,
            x = 'Round',
            y = val,
            title = f'{val} over Rounds',
            line_shape = 'linear',
        )

        fig.update_layout(height=300)
        fig.update_xaxes(tickvals=sorted(main_df['Round']))
        fig.update_traces(line=dict(width=4, color='orange'), mode='lines+markers', marker=dict(size=8, color='grey'))

        # Annotations with rounded values
        annotations = []
        for i, row in main_df.iterrows():
            # Use the helper function to format the annotation text
            value_text = f"<b>{format_value(row[val])}</b>"
            annotations.append(
                dict(
                    x=row['Round'],
                    y=row[val],
                    xref='x',
                    yref='y',
                    text=value_text,
                    showarrow=False,
                    font=dict(size=12),
                    xanchor='center',
                    yanchor='bottom',
                    yshift=10
                )
            )
        fig.update_layout(annotations=annotations)

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

        # st.write(main_df.columns)
        # st.write(main_df)

    col1, col2 = st.columns(2, gap = "small")

    with col1:
        line_plot('ROI')
        line_plot('Operating profit')

    with col2:
        line_plot('Gross margin')
        line_plot('Investment')

finance_info_section()

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 
st.divider()
st.subheader("Current Investment Breakdown")

def investment_brakedown_section():
    
    columns_to_select = [
        "Round",
        "Investment",
        "Investment - Investment - Fixed",
        "Investment - Investment - Stock",
        "Investment - Investment - Machines",
        "Investment - Investment - Payment terms",
    ]

    def sankey_chart():

        # ::::::::: FILTERING THE DATAFRAME :::::::::
        main_df = PROCESSED_FINANCE_DF.copy()
        
        # Find the maximum value in the "Round" column
        max_round_value = main_df["Round"].max()

        # Filter the DataFrame for rows where "Round" equals max_round_value
        main_df = main_df[main_df["Round"] == max_round_value]
        
    
        # ::::::::: PLOTTING THE VALUES IN A SANKEY CHART :::::::::::
        labels = ["Investment"] + columns_to_select[2:]
 
        source = []
        target = []
        values = []

        for i, col in enumerate(columns_to_select[2:], start = 1):
            source.append(0)
            target.append(i)
            values.append(main_df[col].sum())
                
        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
                node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
            ),
                link=dict(
                source=source,
                target=target,
                value=values,
            )
           
        )])

        fig.update_layout(
            title_text="Investment Breakdown", 
            font_size=15
        )


        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    sankey_chart()

investment_brakedown_section()

# :::::::::::::::::::::::: TABLES UTILIZED :::::::::::::::::::::::: 
st.divider()
with st.expander("Finance Report data preview"):
    st.write(RAW_FINANCE_DF)