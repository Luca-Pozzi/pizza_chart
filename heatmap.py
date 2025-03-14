"""
Generate an heatmap with summary of pizza orders per day in the last year.
"""

import os
import datetime
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly

from pizza_chart import plot_pizza_chart

SHOW = False # set to True for debugging
SOURCE = 'default'  # `default` or `custom`
                
if __name__ == '__main__':
    root = os.path.abspath(os.path.dirname(__file__))
    charts_dir = os.path.join(root, 'assets', 'charts')
    df = pd.read_excel(os.path.join(root, 'data', 'data.xlsx'),
                       sheet_name='Orders',
                       usecols=[0, 1, 2, 3])
    # Order the dataframe by date
    df['Date'] = pd.to_datetime(df['Date'],
                                format='%y-%m-%d')
    df = df.sort_values(by='Date', ascending=False)
    now = datetime.datetime.today()

    # Group data by date to obtain a timeseries of orders
    ts = df.groupby('Date')['#'].sum()
    # Get dates since a year ago until the end of the current week
    dates = pd.date_range(start=now-pd.DateOffset(weeks=51),
                                          end=now,
                                          freq='D').normalize()
    dates = dates.union([dates[-1] + (6-now.weekday())*dates.freq])
    # Reindex the timeseries to a df
    heatmap_df = ts.reindex(dates,
                            fill_value=0
                            ).reset_index().rename(columns={'index':'Date'})
    heatmap_df['month'] = heatmap_df['Date'].dt.month_name()
    heatmap_df['weekday'] = heatmap_df['Date'].dt.day_name()
    heatmap_df['week'] = heatmap_df['Date'].dt.isocalendar().week
    # Create a pivot table for the heatmap
    weeks_ordered = heatmap_df['week'].unique().tolist()
    heatmap_df_pivoted= heatmap_df.pivot_table(index='weekday', 
                           columns='week', 
                           values='#', 
                           aggfunc='sum', 
                           fill_value=0
                          )[weeks_ordered] # preserve weeks order
    # Reorder weekdays (Monday to Sunday)
    heatmap_df_pivoted = heatmap_df_pivoted.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    # Plot the calendar/heatmap to an HTML interactive graph
    plotly.offline.init_notebook_mode()
    # Create the heatmap
    # NOTE. Revert vertical axis from top to 
    fig = plotly.graph_objs.Figure(
            plotly.graph_objs.Heatmap(
                x=[str(w) for w in weeks_ordered],  # weeks on the x-axis, 
                                                    # preserve order
                y=heatmap_df_pivoted.index,     # weekdays on the y-axis
                z=heatmap_df_pivoted.values,    # values for the heatmap
                xgap=5,
                ygap=5,
                showscale=False,        # disable the colorbar
                hoverongaps=False,      # disable hover for missing values
                colorscale='Reds',
                colorscale=[[0.0, "rgb(128, 128, 128)"],
                            [0.3333, "rgb(215,48,39)"],
                            [0.6667, "rgb(244,109,67)"],
                            [1.0, "rgb(49,54,149)"]]
            ))

    # Customize the layout
    fig.update_layout(
        #title='GitHub-like Contribution Calendar (Last Year)',
        #xaxis_title='Week of Year',
        #yaxis_title='Day of Week',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=False,    # hide x-axis grid lines
        yaxis_showgrid=False,    # hide y-axis grid lines
        # TODO. Manually adjust the aspect ratio
        width=1200,              # adjust width
        height=300,              # adjust height
        yaxis_scaleanchor="x",   # square tiles (i.e. x:y aspect ratio 1:1)
    )
    
    plotly.offline.plot(fig,
                        config={'displayModeBar':False}, # disable the toolbar
                        filename= 'heatmap' + ".html")