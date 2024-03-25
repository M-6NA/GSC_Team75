import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from utils.data_loader import load_and_process_finance_data
from utils.data_loader import read_main_table_tabs

from utils.constants_passer import SITE_EMOJI, COMPONENT_COLORS, PRODUCT_COLORS, SUPPLY_CHAIN_STOCK_COMPONENTS_WEEKS_DATA, SUPPLY_CHAIN_STOCK_PRODUCT_WEEKS_DATA

# ::::::::::::::::: PAGE CONFIGURATION ::::::::::::::::: 

# Settings for the webpage
st.set_page_config(
    page_title = "Supply Chain",
    layout = "wide",
    page_icon = SITE_EMOJI,

)

# Title for the page
st.title("🔗 Supply Chain")
st.divider()

# ::::::::: READING THE DATAFRAME FROM data_loader.py :::::::::::

COMPONENT_DF = read_main_table_tabs('Component')
PRODUCTS_DF = read_main_table_tabs('Product')
FINANCE_DF = load_and_process_finance_data()[0]

ROUND_TEXT = ['-2', '-1', '0', '1', '2', '3', '4', '5', '6']

component_colors = COMPONENT_COLORS
product_colors = PRODUCT_COLORS
stock_components_weeks_data = SUPPLY_CHAIN_STOCK_COMPONENTS_WEEKS_DATA
stock_product_weeks_data = SUPPLY_CHAIN_STOCK_PRODUCT_WEEKS_DATA

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 

# :::::::::::::::: FINANCES ::::::::::::::::
def finances_section():
    
    def investment_expenses_plot(keyword):
        main_df = FINANCE_DF.copy().T.reset_index()
        main_df.columns = main_df.iloc[0]   # Setting the first row as column names
        main_df = main_df.drop(0)           # Drop the first two rows
        
        # Filter duplicate columns based on the first occurrence
        main_df = main_df.loc[:, ~main_df.columns.duplicated()]

        selected_cols = [col for col in main_df.columns if keyword in col]

        # Filter the DataFrame to get columns associated with the keyword
        keyword_data = main_df[selected_cols]
        # Remove 'Investment - Investment - Fixed' from the keyword_data DataFrame
        keyword_data = keyword_data.drop(columns=['Investment - Investment - Fixed'])

        # Remove 'Investment' column from keyword_data for visualization but keep it for calculations
        keyword_data_for_viz = keyword_data.drop(columns=['Investment'])

        # Calculate percentage contribution of each investment type to the total investment
        total_investment = keyword_data['Investment'].values.astype(float)
        percentage_data = keyword_data_for_viz.div(total_investment, axis=0) * 100

        # Extracting legend labels based on the characters after the last '-' character
        legend_labels = [col.split(' - ')[-1] for col in keyword_data_for_viz.columns]

        # Define a custom color palette for the bars
        custom_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  #

        # Create a stacked bar chart
        fig = go.Figure()

        for i, col in enumerate(percentage_data.columns):
            fig.add_trace(go.Bar(
                x=percentage_data.index,
                y=percentage_data[col],
                name=legend_labels[i],
                marker=dict(
                    color=custom_palette[i % len(custom_palette)] # Loop through colors
                ),  
                hovertemplate='%{y:.2f}%<extra></extra>',
            ))
         
        fig.update_xaxes(
            tickvals=percentage_data.index, 
            ticktext=ROUND_TEXT
        )

        fig.update_layout(
            barmode='stack',
            title='Investment expenses (without fixed)',
            xaxis=dict(title='Round'),
            yaxis=dict(title='Percentage of Total Investment'),
            legend=dict(
                title='',
                orientation='h', 
                yanchor='bottom', 
                y=1.02, 
                xanchor='right', x=1),
            template='plotly_white'
        )

        fig.update_traces(
            texttemplate='<b>%{y:.0f}%</b>',
            textposition='inside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    def stock_value_components_vs_products_plot():
        
        main_df = COMPONENT_DF.copy()
        main_df_2 = PRODUCTS_DF.copy()

        round_values = main_df['Round'].tolist()
        round_values = sorted(list(set(round_values)))
        # st.write(round_values)

        df_agg = main_df.groupby(['Component', 'Round'], as_index = False)['Stock value'].sum()
        df_agg = df_agg.groupby(['Round'], as_index = False)['Stock value'].sum()
        df_agg['Category'] = 'Component' 

        df_agg_2 = main_df_2.groupby(['Product', 'Round'], as_index = False)['Stock value'].sum()
        df_agg_2 = df_agg_2.groupby(['Round'], as_index = False)['Stock value'].sum()
        df_agg_2['Category'] = 'Product' 

        combined_df = pd.concat([df_agg, df_agg_2], ignore_index=True)

        # st.write(combined_df)
        custom_palette = ['#ef233c', '#8d99ae', '#2ca02c', '#d62728']

        # Create a grouped bar chart using Plotly
        fig = px.bar(
            combined_df, 
            x='Round', 
            y='Stock value', 
            color='Category', 
            barmode='group',
            labels={'Round': 'Round', 'Stock value': 'Stock Value', 'Category': 'Category'},
            color_discrete_sequence=custom_palette 
        )

         # Update x-axis ticks
        fig.update_xaxes(
            tickvals=round_values, 
            ticktext=round_values
        )

 
        # Update layout for better visualization
        fig.update_layout(
            title='Stock Value Components vs Products (\u2193)',
            xaxis_title='Round',
            yaxis_title='Stock Value',
            legend=dict(
                orientation="h",  # Set legend orientation to horizontal
                yanchor="bottom",
                y=0.89,
                xanchor="right",
                x=0.3,
                title = ''
            ),
            title_y = 0.91
        )

        fig.add_shape(
            type="line",
            x0=df_agg['Round'].min()-0.5,
            y0=220000,
            x1=df_agg['Round'].max()+0.5,
            y1=220000,
            line=dict(
                color="rgba(0,0,0,0.5)", 
                width=2, 
                dash="dashdot"
            ),
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

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)
    
    col1, col2 = st.columns(2, gap = "small")

    with col1:
        investment_expenses_plot('Investment')
        
    with col2:
        stock_value_components_vs_products_plot()


st.subheader("Finances")
with st.expander("Finances Section"):    
    finances_section()

st.divider()


# :::::::::::::::: COMPONENTS ::::::::::::::::

def components_section():
    
    def stock_value_components():
        main_df = COMPONENT_DF.copy()

    
        df_agg = main_df.groupby(['Component', 'Round'], as_index = False)['Stock value'].sum()
        df_agg['Color'] = df_agg['Component'].map(lambda x: component_colors.get(x))
        # st.write(df_agg)

        raw_total_per_round = main_df.groupby(['Round'], as_index = False)['Stock value'].sum()
        # st.write(raw_total_per_round)

        # Merge the DataFrames on the 'Round' column
        merged_df = df_agg.merge(raw_total_per_round, on='Round', suffixes=('_component', '_total'))

        # Calculate the percentage
        merged_df['Stock value %'] = (merged_df['Stock value_component'] / merged_df['Stock value_total']) * 100

        # Display the resulting DataFrame
        # st.write(merged_df)

        fig = go.Figure()
        for component, data in merged_df.groupby('Component'):
            fig.add_trace(go.Scatter(
                    x=data['Round'],
                    y=data['Stock value %'],
                    mode='lines',
                    # stackgroup='zero',  # Adding stackgroup for stacking the areas
                    fill='tozeroy',   # Filling the area to the x-axis
                    name=component,
                    line=dict(color=component_colors[component])
                )
            )

        fig.update_layout(
                title='Stock value of Components (% of total)',
                xaxis_title='Round',
                yaxis_title='Stock value (%)',
                legend_title='Component',
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1,
                    title = '',
                ),
                showlegend=True
        )

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    def stock_components_weeks():
        
        data = stock_components_weeks_data

        # Create a trace for the line chart
        trace = go.Scatter(
            x=data['rounds'], 
            y=data['values'], 
            mode='lines+markers',
            # text=data['values'],  # Set the text to display on markers
            # textposition='top center',
        )

        # Create a layout for the chart
        layout = go.Layout(
            title='Stock components (weeks)',
            xaxis=dict(title='Rounds'),
            yaxis=dict(title='Values')
        )

        # Create annotations to display values next to markers
        annotations = []
        for i, value in enumerate(data['values']):
            annotations.append(
                dict(
                    x=data['rounds'][i],
                    y=value,
                    xref='x',
                    yref='y',
                    text=f'<b>{str(value)}</b>',
                    showarrow=False,
                    font=dict(
                        size=12,
                    ),  
                    xanchor='center',  # Center text horizontally on marker
                    yanchor='bottom',  # Position text above the marker
                    yshift=10  # Adjust vertical position
                )
            )

        layout['annotations'] = annotations

        # Combine trace and layout to create the figure
        fig = go.Figure(
            data=[trace], 
            layout=layout
        )

        fig.update_traces(
            line=dict(width=4, color = 'orange'), 
            marker=dict(size=8, color = 'grey')
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def line_plot():
        main_df = COMPONENT_DF.copy()

        df_agg = main_df.groupby(['Component', 'Round'], as_index = False)['Stock value'].sum()
        df_agg['Color'] = df_agg['Component'].map(lambda x: component_colors.get(x))

        # sum_stock_weeks = df_agg.groupby(['Round'])

        # st.write(df_agg)

        # Line plot
        fig = go.Figure()
        for component, data in df_agg.groupby('Component'):
            fig.add_trace(go.Scatter(
                    x=data['Round'],
                    y=data['Stock value'],
                    mode='lines+markers',  # To display both lines and markers
                    name=component,
                    line=dict(color=component_colors[component], width = 4),
                    marker=dict(color=component_colors[component], size = 8)
                )
            )

        fig.update_layout(
            title='Stock value of Components',
            xaxis_title='Round',
            yaxis_title='Stock value',
            legend_title='Component',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            showlegend=True
        )

        fig.update_traces(
            texttemplate='<b>%{y:.3s}</b>',
            textposition='top center',  # Adjust text position if needed
            textfont=dict(size=13)
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def combined_plot():
        main_df = COMPONENT_DF.copy()

        df_agg_bar = main_df.groupby(['Component', 'Round'], as_index=False)['Stock (weeks)'].sum()
        df_agg_bar['Color'] = df_agg_bar['Component'].map(lambda x: component_colors.get(x))

        df_agg_line = main_df.groupby(['Component', 'Round'], as_index=False)['Stock value'].sum()
        df_agg_line['Color'] = df_agg_line['Component'].map(lambda x: component_colors.get(x))

        # Create the grouped bar plot
        fig = go.Figure()
        for component, data in df_agg_bar.groupby('Component'):
            fig.add_trace(go.Bar(
                x=data['Round'],
                y=data['Stock (weeks)'],
                name=component,
                marker=dict(color=component_colors[component]),
                text=data['Stock (weeks)'],
                # textposition='inside',
                texttemplate='<b>%{y:.3s}</b>',
                offsetgroup=component  # Use a separate offset group for bars
            ))

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
        
        # Add the line plot with a secondary y-axis
        for component, data in df_agg_line.groupby('Component'):
            fig.add_trace(go.Scatter(
                x=data['Round'],
                y=data['Stock value'],
                mode='lines+markers',
                name=component,
                line=dict(
                    color=component_colors[component], 
                    width=4),
                marker=dict(
                    color='#4a4e69', 
                    size=8),
                text=data['Stock value'],
                textposition='top center',
                texttemplate='<b>%{y:.3s}</b>',
                yaxis='y2',  # Plot line chart on secondary y-axis
            ))

        fig.update_layout(
            title='Combined Stock Analysis',
            xaxis_title='Round',
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
            yaxis=dict(title='Stock', side='left'),  # Primary y-axis for bars
            yaxis2=dict(title='Stock value', side='right', overlaying='y', showgrid=False),  # Secondary y-axis for line chart
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def avg_cost_of_delivery_plot():
        main_df = COMPONENT_DF.copy()

        trans_df = main_df.groupby(['Component', 'Round'], as_index = False)[['Transport costs previous round', 'Order lines previous round']].sum()
        trans_df['Delivery cost'] = trans_df['Transport costs previous round'] / trans_df['Order lines previous round']

        # st.write(trans_df)
        color_map = {component: component_colors.get(component, '#000000') for component in trans_df['Component'].unique()}

        fig = px.line(
            trans_df, 
            x='Round', 
            y='Delivery cost', 
            color='Component',
            color_discrete_map=color_map, 
            title='Average Costs of Delivery',
        )

        # Customize line width and marker size
        fig.update_traces(
            mode='lines+markers',
            line=dict(width=4), 
            marker=dict(size=8)
        )


        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def component_table_section():
        def component_info_table(component):
            
            SELECTED_THRESHOLD = slider_threshold
            main_df = COMPONENT_DF.copy()
            main_df = main_df.round(2)

            # st.write(main_df)

            df_agg = main_df.groupby(['Component', 'Round'], as_index = False)[[
                'Order lines previous round',
                'Purchase value previous round',
                'Transport costs previous round',
                'Purchase price',
                'Order size',
                'Stock (weeks)',
                'Stock value',
                'Component availability (%)',
                'Bias']].sum()
            
            component_df = df_agg.loc[df_agg['Component'] == component].T.reset_index()
            component_df = component_df.drop(0) 
            component_df.columns = component_df.iloc[0]
            component_df = component_df.drop(1)

            # Get the length of the DataFrame
            num_rows = len(component_df)

            # Replace all values in 'Round' column except for the last row
            component_df.loc[:num_rows, 'Round'] = '(\u2193) ' + component_df.loc[:num_rows, 'Round']
            component_df['Round'] = component_df['Round'].replace(['Bias'], '(\u2191\u2193) Bias')

            numeric_columns = component_df.columns[1:]
            component_df[numeric_columns] = component_df[numeric_columns].astype(float)

            def change_color(value, previous_value):
                if pd.isnull(previous_value) or not isinstance(value, (int, float)):
                    return ''

                try:
                    value = float(value)
                    previous_value = float(previous_value)

                    if previous_value == 0:
                        return 'background-color: rgba(0, 255, 0, 0.4)'

                    percentage = ((value - previous_value) / previous_value) * 100

                    if percentage > SELECTED_THRESHOLD:
                        return 'background-color: rgba(255, 77, 109, 0.4)'  # Red color
                    elif percentage < -SELECTED_THRESHOLD:
                        return 'background-color: rgba(0, 255, 0, 0.4)'  # Green color

                # st.write(f"Percentage: `{percentage}` | Value: `{value}` | Previous value: `{previous_value}`")
                except ValueError:
                    pass  # Handles non-convertible values without causing an error

                return ''

            
            styler = component_df.style.apply(
                lambda row: [
                    change_color(value, previous) for value, previous in zip(row, row.shift(1))
                ], 
                axis=1
            )

            st.dataframe(
                styler.format({-2: '{:.10}', -1: '{:.10}', 0: '{:.10}', 1: '{:.10}', 2: '{:.10}', 3: '{:.10}'}),
                use_container_width=True
            ) 

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            'Orange',
            'Mango',
            'PET',
            'Pack 1L',
            'Vitamin C',
            'Açaí',
            'Bag',
            'Capsule (orange)',
            'Capsule (red)'
        ])

        slider_threshold = st.select_slider(
            'Select a threshold',
            options = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
            value = 15
        )

        with tab1:
            component_info_table('Orange') 

        with tab2:
            component_info_table('Mango')

        with tab3:
            component_info_table('PET')
        
        with tab4:
            component_info_table('Pack 1L')

        with tab5:
            component_info_table('Vitamin C') 

        with tab6:
            component_info_table('Açaí')

        with tab7:
            component_info_table('Bag')

        with tab8:
            component_info_table('Capsule (orange)')
        
        with tab9:
            component_info_table('Capsule (red)')


    col1, col2 = st.columns(2, gap = "small")

    with col1:
        stock_components_weeks()
        pass

    with col2:
        stock_value_components()

    combined_plot()
    avg_cost_of_delivery_plot()
    component_table_section()

st.subheader("Components")
with st.expander("Components Section"):    
    components_section()

st.divider()

# :::::::::::::::: PRODUCTION ::::::::::::::::

def production_section():

    def stock_products_weeks():
        
        data = stock_product_weeks_data

        # Create a trace for the line chart
        trace = go.Scatter(
            x=data['rounds'], 
            y=data['values'], 
            mode='lines+markers',
            # text=data['values'],  # Set the text to display on markers
            # textposition='top center',
        )

        # Create a layout for the chart
        layout = go.Layout(
            title='Stock products (weeks)',
            xaxis=dict(title='Rounds'),
            yaxis=dict(title='Values')
        )

        # Create annotations to display values next to markers
        annotations = []
        for i, value in enumerate(data['values']):
            annotations.append(
                dict(
                    x=data['rounds'][i],
                    y=value,
                    xref='x',
                    yref='y',
                    text=f'<b>{str(value)}</b>',
                    showarrow=False,
                    font=dict(
                        size=12,
                    ),  
                    xanchor='center',  # Center text horizontally on marker
                    yanchor='bottom',  # Position text above the marker
                    yshift=10  # Adjust vertical position
                )
            )

        layout['annotations'] = annotations

        # Combine trace and layout to create the figure
        fig = go.Figure(
            data=[trace], 
            layout=layout
        )

        fig.update_traces(
            line=dict(width=4, color = 'orange'), 
            marker=dict(size=8, color = 'grey')
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def stock_value_products():
        main_df = PRODUCTS_DF.copy()

        df_agg = main_df.groupby(['Product', 'Round'], as_index = False)['Stock value'].sum()
        df_agg['Color'] = df_agg['Product'].map(lambda x: product_colors.get(x))

        raw_total_per_round = main_df.groupby(['Round'], as_index = False)['Stock value'].sum()
        # st.write(raw_total_per_round)

        merged_df = df_agg.merge(raw_total_per_round, on='Round', suffixes=('_product', '_total'))

        # Calculate the percentage
        merged_df['Stock value %'] = (merged_df['Stock value_product'] / merged_df['Stock value_total']) * 100

        # st.write(merged_df)

        fig = go.Figure()
        for product, data in merged_df.groupby('Product'):
            fig.add_trace(go.Scatter(
                    x=data['Round'],
                    y=data['Stock value %'],
                    mode='lines',
                    # stackgroup='zero',  # Adding stackgroup for stacking the areas
                    fill='tozeroy',   # Filling the area to the x-axis
                    name=product,
                    line=dict(color=product_colors[product])
                )
            )

        fig.update_layout(
                title='Stock value of Products (% of total)',
                xaxis_title='Round',
                yaxis_title='Stock value (%)',
                legend_title='Product',
                legend=dict(
                    orientation='h', 
                    yanchor='top',
                    y=-0.2,
                    xanchor='right',
                    x=1, 
                    title = '',
                    itemwidth=30,  # Adjust itemwidth to fit legend items horizontally
                    # traceorder='normal'
                ),
                showlegend=True
        )

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    def combined_plot_2():
        main_df = PRODUCTS_DF.copy()

        df_agg_bar = main_df.groupby(['Product', 'Round'], as_index = False)['Production plan adherence (%)'].sum()
        df_agg_bar['Production plan adherence (%)'] *= 100
        df_agg_bar['Color'] = df_agg_bar['Product'].map(lambda x: product_colors.get(x))

        df_agg_line = main_df.groupby(['Product', 'Round'], as_index = False)['Production batches previous round'].sum()
        df_agg_line['Color'] = df_agg_line['Product'].map(lambda x: product_colors.get(x))


        # Grouped Bar plot
        fig = go.Figure()
        for product, data in df_agg_bar.groupby('Product'):
            fig.add_trace(go.Bar(
                    x=data['Round'],
                    y=data['Production plan adherence (%)'],
                    name=product,
                    marker=dict(color=product_colors[product])
                )
            )

        fig.update_traces(
            texttemplate='<b>%{y:.3s}</b>',
            textposition='inside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        # Add the line plot with a secondary y-axis
        for product, data in df_agg_line.groupby('Product'):
            fig.add_trace(go.Scatter(
                    x=data['Round'],
                    y=data['Production batches previous round'],
                    mode='lines+markers',  # To display both lines and markers
                    name=product,
                    line=dict(
                        color=product_colors[product], 
                        width = 4),
                    marker=dict(
                        color='#4a4e69', 
                        size = 8),
                    text = data['Production batches previous round'],
                    textposition='top center',
                    texttemplate='<b>%{y:.1s}</b>',
                    yaxis='y2', 
                )
            )

        fig.update_layout(
            title='Combined Production Analysis',
            xaxis_title='',
            yaxis_title= 'Production plan adherence (%)',
            legend_title='',
            legend=dict(
                orientation='h',
                yanchor='top',
                y=-0.2,
                xanchor='right',
                x=0.9,
            ),
            showlegend=True,
            yaxis=dict(title='Product plan adherence (%)', side='left'),  # Primary y-axis for bars
            yaxis2=dict(title='Product batches previous round', side='right', overlaying='y', showgrid=False), 
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def gross_margin_week_plot():
        main_df = PRODUCTS_DF.copy()

        df_agg = main_df.groupby(['Product', 'Round'], as_index = False)['Gross margin per week'].sum()
        df_agg['Color'] = df_agg['Product'].map(lambda x: product_colors.get(x))

        fig = go.Figure()
        for product, data in df_agg.groupby('Product'):
            fig.add_trace(go.Scatter(
                    x=data['Round'],
                    y=data['Gross margin per week'],
                    mode='lines+markers', 
                    name=product,
                    line=dict(color=product_colors[product], width = 4),
                    marker=dict(color='#4a4e69', size = 8)
                )
            )

        fig.update_layout(
            title='Gross margin per week',
            xaxis_title='Round',
            yaxis_title='Gross margin per week',
            legend_title='',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            showlegend=True
        )

        fig.update_traces(
            texttemplate='<b>%{y:.3s}</b>',
            textposition='top center',  # Adjust text position if needed
            textfont=dict(size=13)
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def obsoletes_per_week_plot():
        main_df = PRODUCTS_DF.copy()

        df_agg = main_df.groupby(['Product', 'Round'], as_index = False)['Obsoletes per week (value)'].sum()
        df_agg['Color'] = df_agg['Product'].map(lambda x: product_colors.get(x))

        fig = go.Figure()
        for product, data in df_agg.groupby('Product'):
            fig.add_trace(go.Bar(
                    x=data['Round'],
                    y=data['Obsoletes per week (value)'],
                    name=product,
                    marker=dict(color=product_colors[product])
                )
            )

        fig.update_layout(
            title='Obsoletes per week',
            xaxis_title='Round',
            yaxis_title= 'Obsoletes per week (value)',
            legend_title='',
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

        fig.update_traces(
            texttemplate='<b>%{y:.2s}</b>',
            textposition='inside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def demand_units_per_orderline_plot():
        main_df = PRODUCTS_DF.copy()

        df_agg = main_df.groupby(['Product', 'Round'], as_index = False)[['Demand per week (units)', 'Order lines per week']].sum()
        df_agg['Demand units per orderline'] = df_agg['Demand per week (units)'] / df_agg['Order lines per week']
        df_agg['Color'] = df_agg['Product'].map(lambda x: product_colors.get(x))

        fig = go.Figure(
            data=[go.Pie(
                labels=df_agg['Product'], 
                values=df_agg['Demand units per orderline'],
                marker=dict(colors=df_agg['Color'], line=dict(color='#000000', width=1)),
            )]
        )

        fig.update_layout(
            title='Demand Units per Order Line',
            title_font=dict(size=20),
            font=dict(size=14)
        )

        fig.update_traces(
            # texttemplate='<b>{y:.3f}</b>',
            textposition='inside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    col1, col2 = st.columns(2, gap = "small")

    with col1:
        stock_products_weeks()
    
    with col2:
        stock_value_products()

    combined_plot_2()
    gross_margin_week_plot()
    obsoletes_per_week_plot()
    demand_units_per_orderline_plot()

st.subheader("Production")
with st.expander("Production Section"):    
    production_section()

st.divider()

# :::::::::::::::: TABLES UTILIZED ::::::::::::::::

with st.expander("Component Table"):
    st.write(COMPONENT_DF)

with st.expander("Product Table"):
    st.write(PRODUCTS_DF)

with st.expander("Finances Table"):
    st.write(FINANCE_DF)