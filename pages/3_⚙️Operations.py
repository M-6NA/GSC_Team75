import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import read_main_table_tabs
from utils.constants_passer import SITE_EMOJI

# ::::::::::::::::: PAGE CONFIGURATION ::::::::::::::::: 

# Settings for the webpage
st.set_page_config(
    page_title = "Operations",
    layout = "wide",
    page_icon = SITE_EMOJI,

)

# Title for the page
st.title("⚙️ Operations")
st.divider()

# ::::::::: READING THE DATAFRAME FROM data_loader.py :::::::::::
WAREH_SALES_AREA_DF = read_main_table_tabs('Warehouse, Salesarea')
PRODUCT_WAREH_DF = read_main_table_tabs('Product - Warehouse')
MIXERS_DF = read_main_table_tabs('Mixers')
BOTTLING_LINE_DF = read_main_table_tabs('Bottling line')
PRODUCTS_DF = read_main_table_tabs('Product')

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 

# :::::::::::::::: WAREHOUSING SECTION ::::::::::::::::
def warehousing_section():
    
    st.subheader("Warehousing")

    def cube_util_plot():
        main_df = WAREH_SALES_AREA_DF.copy()
        main_df['Cube utilization (%)'] = main_df['Cube utilization (%)'] * 100

        fig = go.Figure()

        for warehouse, data in main_df.groupby('Warehouse'):
            fig.add_trace(
                go.Scatter(
                    x=data['Round'],
                    y=data['Cube utilization (%)'],
                    mode='lines+markers',
                    name=warehouse,
                    line=dict(width=4),
                    marker=dict(size=8)
                )
            )

        fig.update_layout(
            xaxis_title='Round',
            yaxis_title='Cube Utilization (%)',
            title='Cube Utilization per Round for Each Warehouse',
            showlegend=True,
            barmode = 'group',
            legend=dict(
                orientation='h',
                yanchor='top',
                y=1.15,
                xanchor='left',
                x=0,
            )
        )

        # Show the plot
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def plot_stock_vs_demand_bars():
        main_df = PRODUCT_WAREH_DF.copy()

        # Grouping by 'Round' and summing the values
        grouped_df = main_df.groupby('Round').agg({'Demand per week (value)': 'sum', 'Stock value': 'sum'}).reset_index()

        custom_palette = ['#ef233c', '#8d99ae', '#2ca02c', '#d62728']

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=grouped_df['Round'],
                y=grouped_df['Demand per week (value)'],
                name='Demand per week (value)',
                marker_color=custom_palette[0],  # Setting color for the first bar
            )
        )

        fig.add_trace(
            go.Bar(
                x=grouped_df['Round'],
                y=grouped_df['Stock value'],
                name='Stock value',
                marker_color=custom_palette[1],  # Setting color for the second bar
            )
        )

        fig.update_traces(
            texttemplate='<b>%{y:.0s}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        fig.update_layout(
            barmode='group',
            xaxis_title='Round',
            yaxis_title='Value',
            title='Total Demand vs Stock Value by Round',
            legend=dict(
                orientation="h",  # Set the orientation to horizontal
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.6
            ),
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Function for plotting the gauge plot for warehouses
    def plot_cube_util_gauge(round_val, wh_name):
        
        main_df = WAREH_SALES_AREA_DF.copy()
        
        # st.code(wh_name)
        # Filter the DataFrame for the specified warehouse and round
        filtered_df = main_df[(main_df['Warehouse'] == wh_name) & (main_df['Round'] == round_val)]

        # Extract cube utilization percentage
        cube_utilization = filtered_df['Cube utilization (%)'].values[0]
        cube_utilization = cube_utilization * 100 

        # Extracting the capacity and usage values
        capacity = filtered_df['Capacity'].values[0]
        usage = round(filtered_df['Usage'].values[0], 2)
        order_lines_per_week = round(filtered_df['Orderlines per week'].values[0],2)
        pallets_tanks_per_week = round(filtered_df['Pallets/Tanks per week'].values[0],2)
        flexible_manpower = round(filtered_df['Flexible manpower (FTE)'].values[0], 2)


        # Create a Plotly gauge plot
        fig = go.Figure(go.Indicator( 
            mode = "gauge+number",
            value = cube_utilization,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{wh_name}"},
            gauge = {
                'axis': {'range': [0, 100], 'visible': False},
                'bar': {'color': "#52b788"},
                'steps' : [
                    {'range': [0, 25], 'color': "white"},
                    {'range': [25, 50], 'color': "white"},
                    {'range': [50, 75], 'color': "white"},
                    {'range': [75, 100], 'color': "white"}],
                },
            number = {'suffix': '%'}
            )
        )
 
        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)


        st.markdown(
                f"""
                <div class="column1" style="background-color: rgba(233, 236, 239, 0.5); text-align: left; border-radius: 10px; padding-left: 20px; margin-top: -95px;">
                    <div style="margin-bottom: -35px;"><h4 style = "color: rgba(0, 0, 0, 1); padding-top: 10px;">Other information</h4></div>
                    <hr class="solid" style = "margin-right: 20px;">
                    <div style="margin-bottom: -35px; margin-top: -40px;"><h6 style = "color: rgba(0, 0, 0, 1); padding-top: 20px; font-weight: normal; font-family: 'Consolas', monospace;">- Capacity: {capacity}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Usage: {usage}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Orderlines/week: {order_lines_per_week}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Pallets/Tanks/week: {pallets_tanks_per_week}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Flexible manpower: {flexible_manpower}</h6></div>
                    <div style="margin-top: 0;"><h2 style="margin-top: -15px; font-weight: bold; color: black;"></h2></div>
                </div>
                """,
            unsafe_allow_html=True
        )

    number_of_rounds = WAREH_SALES_AREA_DF['Round'].nunique()

    unique_values = WAREH_SALES_AREA_DF['Round'].unique()

    tab_labels = ["Overview"] + [f"Round {round_val}" for round_val in unique_values]

    tabs = st.tabs(tab_labels)

    with tabs[0]:
        
        col1, col2 = st.columns(2, gap = "small")

        with col1:
            cube_util_plot()

        with col2:
            plot_stock_vs_demand_bars()

    for round_val, tab, in zip(unique_values, tabs[1:]):
        
        with tab:    
            # Cube utilization text
            st.markdown(
                f"""
                <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                    <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) |  Round {round_val}</h4></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3, gap = "small")

            with col1:
                plot_cube_util_gauge(round_val, 'Raw materials warehouse')

            with col2:
                plot_cube_util_gauge(round_val, 'Tank yard')

            with col3:
                plot_cube_util_gauge(round_val, 'Finished goods warehouse')

warehousing_section()


# :::::::::::::::: BOTTLING AND MIXING SECTION ::::::::::::::::

def mixers_fillers_section():
    
    st.divider()
    st.subheader("Bottling and mixing")

    def plot_bottling_line_usage(round_number, bottling_line):

        main_df = BOTTLING_LINE_DF.copy()
        filtered_data = main_df[(main_df['Bottling line'] == bottling_line) & (main_df['Round'] == round_number)]

        # st.write(filtered_data)  # Display filtered DataFrame

        if filtered_data.empty:
            st.write(f"No data found for Round {round_number}")
            return
        
        usage_columns = ['Run time (%)', 'Changeover time (%)', 'Breakdown time (%)', 'Unused capacity (%)']
        # Extracting the data
        usage_data = filtered_data.iloc[0][usage_columns]
        # Convert decimal to percentage
        usage_data = usage_data * 100
        
        # Now, the values should sum to approximately 100 (or slightly over due to rounding in the data)
        total_usage = usage_data.sum()

        overtime_value = filtered_data.iloc[0]['Overtime (%)'] * 100

        # st.write("Usage data for pie chart:", usage_data)
        # st.write("Sum of usage data:", total_usage)

        # Pie chart creation
        fig = px.pie(
            values=usage_data.values,
            names=usage_data.index,
            title=f'{bottling_line} Usage for Round {round_number}'
        )

        fig.update_layout(
            title_font=dict(size=20), 
            font=dict(size=17)
        )

        # Add overtime value to the legend
        fig.add_annotation(
            text=f'- Overtime: {overtime_value}%',
            x=1.25,
            y=0.6,
            showarrow=False,
            font=dict(size=17, color='black')
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def plot_avg_lot_size_per_round():
        main_df = MIXERS_DF.copy()
        avg_lot_size_per_round = main_df.groupby('Round')['Average lot size'].mean().reset_index()

        fig = go.Figure( 
            data=[
                go.Bar(
                    x=avg_lot_size_per_round['Round'],
                    y=avg_lot_size_per_round['Average lot size'],
                    marker=dict(color='#ff4d6d'),
                )
            ],
            layout=go.Layout(
                title='Mixer Average Lot Size per Round',
                xaxis=dict(title='Round'),
                yaxis=dict(title='Average Lot Size'),
            )
            
        )

        fig.update_traces(
            texttemplate='<b>%{y:.3s}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        fig.update_layout(barmode='group')

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    col1, col2 = st.columns(2, gap = "small")

    with col1:
        
        number_of_rounds = BOTTLING_LINE_DF['Round'].nunique()

        unique_values = BOTTLING_LINE_DF['Round'].unique()
        tab_labels = [f"Round {round_val}" for round_val in unique_values]
        
        tabs = st.tabs(tab_labels)

        for round_val, tab, in zip(unique_values, tabs):
            with tab:
                plot_bottling_line_usage(round_val, 'Swiss Fill 1')
                
                if round_val == 3:
                    plot_bottling_line_usage(round_val, 'Cup Canon 1.3 TDX')

    with col2:
        plot_avg_lot_size_per_round()

mixers_fillers_section()

# :::::::::::::::::::::::: TABLES UTILIZED :::::::::::::::::::::::: 
st.divider()

with st.expander("Warehouse, Salesarea Table"):
    st.write(WAREH_SALES_AREA_DF)

with st.expander("Product - Warehouse Table"):
    st.write(PRODUCT_WAREH_DF)

with st.expander("Mixers Table"):
    st.write(MIXERS_DF)

with st.expander("Bottling line Table"):
    st.write(BOTTLING_LINE_DF)

with st.expander("Product Table"):
    st.write(PRODUCTS_DF)