"""
Generate an heatmap with summary of pizza orders per day in the last year.
"""

import os
import datetime
from PIL import Image
import numpy as np
import pandas as pd
import plotly

SHOW = False # set to True for debugging
SOURCE = 'default'  # `default` or `custom`
                
if __name__ == '__main__':
    root = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..'
        )
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
    #plotly.offline.init_notebook_mode()
    # Create the heatmap
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
                # TODO. Use the secondary box to display the order for days with >0 pizzas.
                hovertemplate=("We had %{z} pizzas on this day" +
                               "<extra></extra>" # remove the secondary box
                               ),
                colorscale=[[0.00, "rgb(128, 128, 128)"],
                            [0.10, "rgb(250, 244, 220)"],
                            [0.25, "rgb(250, 244, 220)"],
                            [0.40, "rgb(199, 113,   4)"],
                            [0.65, "rgb(215, 118,   3)"],
                            [0.80, "rgb(231,  48,  45)"],
                            [1.00, "rgb(231,  48,  45)"]]
            ))
    # Customize the layout
    aspect=0.275
    width=1200
    height=width*aspect
    # Get indexes of month changes
    xticks_idx = np.diff(heatmap_df['Date'].dt.month.to_numpy(),
                         prepend=heatmap_df['Date'].dt.month.to_numpy()[0]
                        ) != 0
    xticks_labels = heatmap_df['month'].to_numpy()[xticks_idx]
    xticks_values = heatmap_df['week'].to_numpy()[xticks_idx]
    fig.update_layout(
        #title='GitHub-like Contribution Calendar (Last Year)',
        #xaxis_title='Week of Year',
        #yaxis_title='Day of Week',
        xaxis_tickvals=xticks_values,
        xaxis_ticktext=xticks_labels,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_showgrid=False,    # hide x-axis grid lines
        yaxis_showgrid=False,    # hide y-axis grid lines
        width=width,             # adjust width
        height=height,           # adjust height
        yaxis_scaleanchor="x",   # square tiles (i.e. x:y aspect ratio 1:1)
        xaxis_fixedrange=False,  # enable scrolling in x-axis
        yaxis_fixedrange=True    # disable scrolling in y-axis
    )
    # Update axes styling
    # TODO. Consider creating dark and light themes. So far, a dark-themed background is assumed, as it is the only option in GitHub Pages.
    fig.update_yaxes(autorange="reversed")  # y-axis from top to bottom 
    fig.write_html('docs/heatmap' + ".html",
                   #include_plotlyjs=False,
                   full_html=False,
                   config = {'displayModeBar': False} # disable the toolbar
                   )
    '''
    plotly.offline.plot(fig,
                        config={'displayModeBar':False}, # disable the toolbar
                        include_plotlyjs=False,
                        full_html=False,
                        output_type='div',
                        filename= 'docs/heatmap' + ".html")'
    '''