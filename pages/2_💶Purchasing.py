import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import load_and_process_finance_data
from utils.data_loader import load_suppliers_data
from utils.data_loader import read_main_table_tabs

from utils.constants_passer import COMPONENT_COLORS, SITE_EMOJI

# :::::::::::::::::::::::::::::::::: PAGE CONFIGURATION :::::::::::::::::::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Purchasing",
    layout = "wide",
    page_icon = SITE_EMOJI,

)

# Title for the page
st.title("💶 Purchasing")
st.divider()

# ::::::::: READING THE DATAFRAME FROM data_loader.py AND CONSTANTS :::::::::::
# SOME REASON INCLUDED THIS PROBABLY IMPORTANT
RAW_FINANCE_DF = load_and_process_finance_data()[0]
PROCESSED_FINANCE_DF = load_and_process_finance_data()[1]

# FOR THE WORLDWIDE SUPPLIERS SECTION
MANUAL_SUPPLIER_DF = load_suppliers_data()

# FOR IMPORTANT KPI'S SECTION
SUPPLIER_COMPONENT_DF = read_main_table_tabs('Supplier - Component')
COMPONENT_DF = read_main_table_tabs('Component')

# FOR THE COMPONENT KPI'S SECTION
SUPPLIER_DF = read_main_table_tabs('Supplier')

component_colors = COMPONENT_COLORS
supply_colors = component_colors

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 

# :::::::::::::::: WORLD MAP AND ROUND SUPPLIER REPORT ::::::::::::::::
def wrld_map_and_suplr_report_section():
    
# :::::::::::::::: WORLD MAP ::::::::::::::::
    def world_map(data_df):
        # Create a DataFrame
        map_df = pd.DataFrame(data_df)


        # Plotly figure setup
        fig = go.Figure()

        # Update geos and layout
        fig.update_geos(
            showcountries=True,
            projection_type="equirectangular",
            showcoastlines=True,
            countrycolor="rgba(0, 0, 0, 0.2)", 
            coastlinecolor="rgba(0, 0, 0, 0.2)",
            showland=True,
            landcolor = "rgba(218, 223, 233, 0.4)"

        )
        fig.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 10})

        fig.update_layout(
            legend=dict(
                orientation='h',    # Horizontal orientation
                yanchor='bottom',   # Anchor to bottom of the plot
                y=0,             # Adjust this value to position the legend further down
                xanchor='left',     # Anchor to right side
                x=0                 # Anchor to right side of the plot
            )
        )

        # Add a dot for the Netherlands
        fig.add_trace(
            go.Scattergeo(
                lon=[4.8952],  # Longitude of the Netherlands
                lat=[52.3676],  # Latitude of the Netherlands
                text="Netherlands",
                mode="markers",
                marker=dict(
                    size=10,
                    color='blue',  # Color of the Netherlands dot
                    opacity=0.7,
                    symbol="circle"
                ),
                name="Netherlands"
            )
        )

        # Plot each product on the map and add arrows to the Netherlands
        for index, row in map_df.iterrows():

            # Add arrows from each location to the Netherlands
            fig.add_trace(
                go.Scattergeo(
                    lon=[row['Longitude'], 4.8952],
                    lat=[row['Latitude'], 52.3676],
                    mode='lines',
                    line=dict(
                        width=2, 
                        color='rgb(249, 190, 71, 0.5)', 
                        dash='dashdot'
                    ),
                    showlegend=False
                )
            )

            
        added_supplies = {}

        for index, row in map_df.iterrows():
            supply = row['Supply']
            
            text_sup = f"Name: {row['Name']}<br>" \
                f"Supply: {row['Supply']}<br>" \
                f"Country: {row['Country']}<br>" \
                f"Qlty: {row['Qlty']} <br>"\
                f"Deliveries: {row['Deliveries']}<br>"\
                f"AVG order size: {row['AVG_order_size']}<br>"\
                f"TansP mode: {row['TransP_mode']}<br>"\
                f"Trade unit: {row['Trade_unit']}<br>"

            # Check if the supply has already been added to the legend
            if supply not in added_supplies:
                added_supplies[supply] = True  # Mark the supply as added
                
                fig.add_trace(
                    go.Scattergeo(
                        lon=[row['Longitude']],
                        lat=[row['Latitude']],
                        text=text_sup,
                        mode="markers",
                        marker=dict(
                            size=10,
                            color=supply_colors.get(row['Supply'], "grey"),
                            opacity=0.8,
                            symbol="circle",
                            line=dict(color='black', width=1)
                        ),
                        name=row['Supply']  # Use the supply instead of row['Name']
                    )
                )
            else:
                # Add a trace without adding to the legend for subsequent occurrences of the same supply
                fig.add_trace(
                    go.Scattergeo(
                        lon=[row['Longitude']],
                        lat=[row['Latitude']],
                        text=text_sup,
                        mode="markers",
                        marker=dict(
                            size=10,
                            color=supply_colors.get(row['Supply'], "grey"),
                            opacity=0.7,
                            symbol="circle",
                                line=dict(color='black', width=1)
                        ),
                        showlegend=False  # Do not add to legend
                    )
                )


        # Display the map
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# :::::::::::::::: ROUND SUPPLIER REPORT ::::::::::::::::
    def supplier_report(df):
        css_styles = """
                <style>
                    .column1 {
                        background-color: rgb(244, 245, 247);
                        text-align: left;
                        border-radius: 10px;
                        padding-left: 20px;
                        margin-top: 40px;
                        padding-bottom: 10px;
                    }

                    .column1 h4 {
                        color: rgb(0, 0, 0, 1);
                        padding-top: 10px;
                    }

                    table {
                        width: 100%;
                        border: none!important;
                    }


                    th {
                        text-align: center;
                        font-size: 14px;
                    }

                    tr {
                        height: 10px;
                        font-size: 14px;
                    }

                    table, td, th{
                        border: none!important;
                    }

                    td, th {
                        border: none;
                        padding-top: 1px!important;

                    }

                    p {
                        margin: 0;
                    }

                    .right-align {
                        text-align: right;
                    }

                    .left-align {
                        text-align: left;
                    }

                    .center-align {
                        text-align: center;
                    }

                    .bold {
                        font-weight: bold;
                    }

                    .monospace {
                        font-family: 'Consolas', monospace;
                    }

                </style>
            """

        table_header = "<div class='column1'><div style='margin-bottom: -35px;'><h4 class='bold monospace'>Round supplier report</h4></div><br><div style='margin-bottom:-10px; margin-top: -4px; padding-right: 20px; padding-top: -5px;'><table cellspacing='0' cellpadding='0'><tr><th class='bold left-align'>Trade unit</th><th class='bold right-align'>Order size</th><th class='bold right-align'>Purchases</th><th class='bold right-align'>Purchase value</th><th class='bold right-align'>Transport costs</th></tr>"

        color_mapping = {
            'Pack1L': 'rgb(135, 110, 168)',
            'PET': 'rgb(92, 154, 207)',
            'Orange': 'rgb(245, 158, 52)',
            'Mango': 'rgb(165, 213, 89)',
            'Vitamin C': 'rgb(249, 121, 125)',
            'Açaí': 'rgb(199, 146, 234)'
        }

        #  Adding the "," to the numbers for better readability
        df['AVG_order_size'] = df['AVG_order_size'].apply(lambda x: f"{x:,}")
        df['Deliveries'] = df['Deliveries'].apply(lambda x: f"{x:,}")
        df['Purchase value'] = df['Purchase value'].apply(lambda x: f"{x:,}")
        df['Transport costs'] = df['Transport costs'].apply(lambda x: f"{x:,}")

        table_rows = ""
        current_trade_unit = None
        for index, row in df.iterrows():
            if row['Trade_unit'] != current_trade_unit:
                table_rows += f"<tr><th class='bold left-align'>{row['Trade_unit']}</th></tr>"
                item_info = df.loc[df['Trade_unit'] == row['Trade_unit'], ['Supply', 'AVG_order_size', 'Deliveries', 'Purchase value', 'Transport costs']]
                for _, item_row in item_info.iterrows():
                    item_color = color_mapping.get(item_row['Supply'], 'black')  # Default color if not found in the mapping
                    table_rows += f"<tr><td class='right-align monospace' style='font-weight: bold; color: {item_color};'>{item_row['Supply']}</td><td class='right-align monospace'>{item_row['AVG_order_size']}</td><td class='right-align monospace'>{item_row['Deliveries']}</td><td class='right-align monospace'>{item_row['Purchase value']}</td><td class='right-align monospace'>{item_row['Transport costs']}</td></tr>"
                current_trade_unit = row['Trade_unit']
 
        table_footer = "</table></div></div>"

        # # Construct the complete HTML table
        table_html = f"{css_styles}{table_header}{table_rows}{table_footer}"

        # Display the HTML table in Streamlit using markdown
        st.markdown(table_html, unsafe_allow_html=True)
    
    def display_quant_per_unit():
        st.markdown(
        f"""
        <div class="column1" style="background-color: #f4f5f7; text-align: center; border-radius: 10px; padding-left: 10px; padding-top: 5px; margin-top: 10px;">
            <p style="text-align: left; font-weight: bold; font-family: 'Consolas', monospace;">Quantities per Unit: </p>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 10px;">
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 15px; text-align: left;">Content drum (liter): <span style="color: #5eb889;">250</span></div>
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 15px; text-align: left;">Content IBC (liter): <span style="color: #5eb889;">1,000</span></div>
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 14px; text-align: left;">Content tank truck (liter): <span style="color: #5eb889;">30,000</span></div>
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 15px; text-align: left;">Pallets per FTL: <span style="color: #5eb889;">30</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Worldwide Suppliers")
    # ::::::::::: DYNAMIC TABS :::::::::::
    # Suppose you have a variable that determines the number of rounds
    number_of_rounds = MANUAL_SUPPLIER_DF['Round'].nunique()  

    # Create a list of tab labels dynamically
    tab_labels = [f"Round {i}" for i in range(number_of_rounds)]

    # Use a list comprehension to create tabs dynamically
    tabs = st.tabs(tab_labels)

    for i, tab in enumerate(tabs):
        with tab:
            
            col1, col2 = st.columns(2, gap = "small")

            with col1:
                round_data = MANUAL_SUPPLIER_DF[MANUAL_SUPPLIER_DF['Round'] == i]
                world_map(round_data)

            with col2:
                round_report_data = MANUAL_SUPPLIER_DF[MANUAL_SUPPLIER_DF['Round'] == i]
                supplier_report(round_report_data)
                display_quant_per_unit()
                
wrld_map_and_suplr_report_section()

# :::::::::::::::: IMPORTANT KPIS ::::::::::::::::
def important_kpi_section():
    
    st.divider()
    st.subheader("Important KPI's")

    def raw_material_costs_plot():
        main_df = RAW_FINANCE_DF.copy().T.reset_index()
        main_df.columns = main_df.iloc[0]
        main_df = main_df.drop(main_df.index[0])

        # Filter duplicate columns based on the first occurrence
        main_df = main_df.loc[:, ~main_df.columns.duplicated()]

        filt_df = main_df[['Round', 'Gross margin - Cost of goods sold - Purchase value', 'Realized revenue']]
        
        filt_df['Raw_mat_costs'] = (filt_df['Gross margin - Cost of goods sold - Purchase value'] / filt_df['Realized revenue']) * 100

        # st.write(filt_df)

        fig = go.Figure()

        # Add a scatter plot with Round on the x-axis and Raw_mat_costs on the y-axis
        fig.add_trace(go.Scatter(
            x=filt_df['Round'],
            y=filt_df['Raw_mat_costs'],
            mode='lines+markers',  # You can use 'lines+markers' if you want lines connecting the markers
            line = dict(
                width = 4,
                color = 'orange',
            ),
            marker=dict(
                color='grey',
                size = 8,
            ),  
            name='Raw Material Costs'
        ))

        # Add horizontal line at y=32
        fig.add_shape(type="line",
                    x0=min(filt_df['Round'] - 0.5),
                    y0=32,
                    x1=max(filt_df['Round'] + 0.5),
                    y1=32,
                    line=dict(color="rgba(255,0,0,0.5)", width=2, dash="dashdot"),  # Modify color and style as needed
                    )

        # Update layout options (optional)
        fig.update_layout(
            title='Raw Material Costs (%) by Round (\u2193)',
            xaxis=dict(title='Round'),
            yaxis=dict(title='Raw Material Costs %'),
            height = 400
        )

        annotations = []
        for i, row in filt_df.iterrows():
            raw_mat_costs_rounded = round(row['Raw_mat_costs'], 1)
            annotations.append(
                dict(
                    x=row['Round'],
                    y=row['Raw_mat_costs'],
                    xref='x',
                    yref='y',
                    text=f'<b>{str(raw_mat_costs_rounded)}%</b>',
                    showarrow=False,
                    font=dict(
                        size=12,
                    ),  
                    xanchor='center',  # Center text horizontally on marker
                    yanchor='bottom',  # Position text above the marker
                    yshift=10  # Adjust vertical position
                )
            )

        # Add annotations to the plot
        for annotation in annotations:
            fig.add_annotation(annotation)

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    def line_plot(col_name, plot_name):
        main_df = COMPONENT_DF.copy()

        df_agg = main_df.groupby(['Component','Round'], as_index = False)[col_name].sum()
        
        # Calculate the average delivery reliability per round
        avg_per_round = df_agg.groupby('Round')[col_name].mean().reset_index()
        avg_per_round.columns = ['Round', 'AVG']
        avg_per_round['AVG'] *= 100

        # st.write(avg_per_round)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x = avg_per_round['Round'],
            y = avg_per_round['AVG'],
            mode='lines+markers',  # You can use 'lines+markers' if you want lines connecting the markers
            line = dict(
                width = 4,
                color = 'orange',
            ),
            marker=dict(
                color='grey',
                size = 8,
            ),  
        ))

        
        if col_name == 'Delivery reliability (%)':
            fig.update_layout(
                title=f"{plot_name}",
                xaxis=dict(title='Round'),
                yaxis=dict(title='AVG Delivery reliability %'),
                height = 400
            )

            # Add horizontal line at y=12
            fig.add_shape(type="line",
                        x0=min(avg_per_round['Round'] - 0.5),
                        y0=95,
                        x1=max(avg_per_round['Round'] + 0.5),
                        y1=95,
                        line=dict(
                            color="rgba(255,0,0,0.5)", 
                            width=2, 
                            dash="dashdot"
                            ),  # Modify color and style as needed
            )

        elif col_name == "Rejection (%)":
            fig.update_layout(
                title=f"{plot_name}",
                xaxis=dict(title='Round'),
                yaxis=dict(title='AVG Rejection %'),
                height = 400
            )

            # Add horizontal line at y=12
            fig.add_shape(type="line",
                        x0=min(avg_per_round['Round'] - 0.5),
                        y0=2.1,
                        x1=max(avg_per_round['Round'] + 0.5),
                        y1=2.1,
                        line=dict(
                            color="rgba(255,0,0,0.5)", 
                            width=2, 
                            dash="dashdot"
                            ),  # Modify color and style as needed
            )
        
        annotations = []
        for i, row in avg_per_round.iterrows():
            avg_rounded = round(row['AVG'], 2)
            annotations.append(
                dict(
                    x=row['Round'],
                    y=row['AVG'],
                    xref='x',
                    yref='y',
                    text=f'<b>{str(avg_rounded)}%</b>',
                    showarrow=False,
                    font=dict(
                        size=12,
                    ),  
                    xanchor='center',  # Center text horizontally on marker
                    yanchor='bottom',  # Position text above the marker
                    yshift=10  # Adjust vertical position
                )
            )

        # Add annotations to the plot
        for annotation in annotations:
            fig.add_annotation(annotation)

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    def avg_transport_costs():
        main_df = SUPPLIER_COMPONENT_DF.copy()
        
        def calculate_transport_percentage(row):
            if row['Purchase value previous round'] == 0:
                return 0
            else:
                return row['Transport costs previous round'] / row['Purchase value previous round']

        
        # Apply the function row-wise to create a new column 'Transport%'
        main_df['Transport%'] = main_df.apply(calculate_transport_percentage, axis=1)

        # Group by 'Round' and calculate the average 'Transport%' per round
        avg_transport_per_round = main_df.groupby('Round')['Transport%'].mean().reset_index()
        avg_transport_per_round.columns = ['Round', 'Transport%']
        avg_transport_per_round['Transport%'] *= 100

        # st.write(avg_transport_per_round)
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x = avg_transport_per_round['Round'],
            y = avg_transport_per_round['Transport%'],
            mode='lines+markers',  # You can use 'lines+markers' if you want lines connecting the markers
            line = dict(
                width = 4,
                color = 'orange',
            ),
            marker=dict(
                color='grey',
                size = 8,
            ),  
        ))

        fig.update_layout(
                title="AVG Transport costs per order (%) by Round (\u2193)",
                xaxis=dict(title='Round'),
                yaxis=dict(title='AVG of transport %'),
                height = 400
        )

        fig.add_shape(type="line",
                        x0=min(avg_transport_per_round['Round'] - 0.5),
                        y0=12,
                        x1=max(avg_transport_per_round['Round'] + 0.5),
                        y1=12,
                        line=dict(
                            color="rgba(255,0,0,0.5)", 
                            width=2, 
                            dash="dashdot"
                            ),  # Modify color and style as needed
        )

        annotations = []
        for i, row in avg_transport_per_round.iterrows():
            avg_rounded = round(row['Transport%'], 2)
            annotations.append(
                dict(
                    x=row['Round'],
                    y=row['Transport%'],
                    xref='x',
                    yref='y',
                    text=f'<b>{str(avg_rounded)}%</b>',
                    showarrow=False,
                    font=dict(
                        size=12,
                    ),  
                    xanchor='center',  # Center text horizontally on marker
                    yanchor='bottom',  # Position text above the marker
                    yshift=10  # Adjust vertical position
                )
            )

        # Add annotations to the plot
        for annotation in annotations:
            fig.add_annotation(annotation)

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    
    col1, col2 = st.columns(2, gap = "small") 

    with col1:
        raw_material_costs_plot()
        avg_transport_costs()

    with col2:
        line_plot('Delivery reliability (%)', 'AVG Delivery reliability (%) by Round (\u2191)')
        line_plot('Rejection (%)', 'AVG Rejection (%) by Round (\u2193)')
    
important_kpi_section()

# :::::::::::::::: COMPONENT KPIS PER ROUND ::::::::::::::::

def component_kpi_section():

    st.divider()
    st.subheader("Component KPI's per round")

    def plot_bar_charts_group(data, col_name, plot_name, mode):
        df = data.copy()

        df_agg = df.groupby(['Component', 'Round'], as_index = False)[col_name].sum()

        if col_name == 'Rejection  (%)':
            df_agg['Rejection  (%)'] = df_agg['Rejection  (%)'] * 100
            # st.write(df_agg)
        else:
            pass

        df_agg['Color'] = df_agg['Component'].map(lambda x: component_colors.get(x))


        # Grouped bar plot
        fig = go.Figure()
        for component, data in df_agg.groupby('Component'):
            fig.add_trace(go.Bar(
                    x=data['Round'],
                    y=data[col_name],
                    name=component,
                    marker=dict(color=component_colors[component])
                )
            )

        fig.update_layout(
                title=plot_name,
                xaxis_title='Round',
                yaxis_title= col_name,
                legend_title='Component',
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1,
                    title = '',
                ),
                showlegend=True,
                barmode='stack'
        )

        if mode == 'stacked':
            fig.update_layout(
                barmode = 'stack'
            )
        elif mode == 'grouped': 
            fig.update_layout(
                barmode = 'group'
            )

        if col_name == 'Order lines previous round':
            fig.update_traces(
                texttemplate='<b>%{y:.1f}</b>',
                textposition='outside',
                marker=dict(
                    line=dict(
                        width=1, color='DarkSlateGray'
                        )
                    )
            )
        
        elif col_name == 'Rejection  (%)':
            fig.update_traces(
                texttemplate='<b>%{y:.2f}%</b>',
                textposition='inside',
                textfont=dict(size=13),
                marker=dict(
                    line=dict(
                        width=1, color='DarkSlateGray'
                        )
                    )
            )

        elif col_name == 'Stock (pieces or liters)':
            top_line = df_agg.groupby('Round')['Stock (pieces or liters)'].sum()

            fig.update_traces(
                texttemplate='<b>%{y:.3s}</b>',
                textposition='inside',
                textfont=dict(size=13),
                marker=dict(
                    line=dict(
                        width=1, color='DarkSlateGray'
                        )
                    )
            )

            fig.add_trace(go.Scatter(
                x=top_line.index,
                y=top_line.values,
                mode='lines',
                name='Top Line',
                    line=dict(
                        color='red',
                        width=3,
                        dash = 'dashdot',
                    ),
                hoverinfo='none'
            ))

        elif col_name == 'Stock (weeks)':
            fig.update_traces(
                texttemplate='<b>%{y:.1f}</b>',
                textposition='inside',
                textfont=dict(size=13),
                marker=dict(
                    line=dict(
                        width=1, color='DarkSlateGray'
                        )
                    )
            )


        elif col_name == 'Purchase  value previous round' or 'Transport costs by Rounds':
            fig.update_traces(
                texttemplate='<b>%{y:.3s}</b>',
                textposition='outside',
                marker=dict(
                    line=dict(
                        width=1, color='DarkSlateGray'
                        )
                    )
            )
        

        

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def plot_bar_charts_group2(data, col_name, plot_name, mode):
        df = data.copy()

        df_agg = df.groupby(['Component', 'Round']).agg({col_name: 'mean'}).reset_index()
        df_agg[col_name] *= 100

        # Grouped bar plot
        fig = go.Figure()
        for component, data in df_agg.groupby('Component'):
            fig.add_trace(go.Bar(
                    x=data['Round'],
                    y=data[col_name],
                    name=component,
                    marker=dict(color=component_colors[component])
                )
            )

        if col_name == 'Delivery reliability (%)': 
            fig.add_shape(
                type="line",
                x0=df_agg['Round'].min()-0.5,
                y0=95,
                x1=df_agg['Round'].max()+0.5,
                y1=95,
                line=dict(
                    color="rgba(0,0,0,0.5)", 
                    width=2, 
                    dash="dashdot"
                ),
            )
        elif col_name == 'Rejection  (%)':
            fig.add_shape(
                type="line",
                x0=df_agg['Round'].min()-0.5,
                y0=2,
                x1=df_agg['Round'].max()+0.5,
                y1=2,
                line=dict(
                    color="rgba(0,0,0,0.5)", 
                    width=2, 
                    dash="dashdot"
                ),
            )


        fig.update_layout(
                title=plot_name,
                xaxis_title='Round',
                yaxis_title= col_name,
                legend_title='Component',
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1,
                    title = ''
                ),
                showlegend=True,
        )

        if mode == 'stacked':
            fig.update_layout(
                barmode = 'stack'
            )
        elif mode == 'grouped': 
            fig.update_layout(
                barmode = 'group'
            )


        fig.update_traces(
            texttemplate='<b>%{y:.0f}%</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )


        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    def order_lines_by_rounds_section():
        plot_bar_charts_group(SUPPLIER_DF, 'Order lines previous round', 'Order lines by Rounds', 'grouped')

    def purchase_value_by_rounds_section():
        plot_bar_charts_group(SUPPLIER_DF, 'Purchase  value previous round', 'Purchase value by Rounds', 'grouped')

    def transport_costs_by_rounds_section():
        plot_bar_charts_group(SUPPLIER_DF, 'Transport costs previous round', 'Transport costs by Rounds', 'grouped')

    def sum_rejection_section():
        plot_bar_charts_group(SUPPLIER_DF, 'Rejection  (%)', 'Sum of Rejection(%) by Round and Component', 'stacked')

    def sum_of_stock_section():
        plot_bar_charts_group(COMPONENT_DF, 'Stock (pieces or liters)', 'Sum of Stock (pieces or liters) by Round and Component', 'stacked')

    def sum_of_stock_weeks_section():
        plot_bar_charts_group(COMPONENT_DF, 'Stock (weeks)', 'Sum of Stock (weeks) by Round and Component', 'stacked')

    order_lines_by_rounds_section()
    st.divider()
    purchase_value_by_rounds_section()
    st.divider()
    transport_costs_by_rounds_section()
    st.divider()
    sum_rejection_section()
    st.divider()
    sum_of_stock_section()
    st.divider()
    sum_of_stock_weeks_section()

component_kpi_section()

# :::::::::::::::::::::::: TABLES UTILIZED :::::::::::::::::::::::: 
st.divider()
with st.expander("Finance Table"):
    st.write(RAW_FINANCE_DF)

with st.expander("Supplier Table"):
    st.write(SUPPLIER_DF)

with st.expander("Component Table"):
    st.write(COMPONENT_DF)

with st.expander("Supplier - Component Table"):
    st.write(SUPPLIER_COMPONENT_DF)
