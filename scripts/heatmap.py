"""
Generate an heatmap with summary of pizza orders per day in the last year.
"""

import os
import datetime
import numpy as np
import pandas as pd
import plotly

OFFLINE = False # set to True for debugging
# NOTE. Currently not working (see bottom of this script).
                
if __name__ == '__main__':
    root = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..'
        )
    charts_dir = os.path.join(root, 'assets', 'charts')
    csv_path = os.path.join(root, 'data', 'data.csv')
    excel_path = csv_path.replace('.csv', '.xlsx')
    if os.path.exists(csv_path): # data in CSV
        df = pd.read_csv(csv_path)
    elif os.path.exists(excel_path): # data in Excel
        df = pd.read_excel(excel_path, sheet_name='Orders', usecols=[0, 1, 2, 3])
    else:
        raise Exception(f"No data file found at {csv_path} or {excel_path}")
    # Order the dataframe by date
    df['Date'] = pd.to_datetime(df['Date'],
                                format='%d/%m/%Y')
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
    # Create per-day order df
    orders_per_day = (
        df.groupby(['Date', 'Pizza'])['#']
        .sum()
        .reset_index()
    )
    # Convert per-day order summary to a string format for hover display
    orders_per_day['desc'] = (
        "• " + orders_per_day['Pizza'] + " x" + orders_per_day['#'].astype(str)
        )
    orders_summary = (
        orders_per_day.groupby('Date')['desc']
        .apply(lambda x: "<br>".join(x))
    )
    # Attach the per-day order summary to the heatmap df
    heatmap_df['orders'] = heatmap_df['Date'].map(orders_summary).fillna("")
    # Attach a string representation of the date for hover display (e.g. "01-01-2024")
    heatmap_df['date_str'] = heatmap_df['Date'].dt.strftime('%d-%m-%Y')
    # Create a pivot table for the heatmap
    weeks_ordered = heatmap_df['week'].unique().tolist()
    heatmap_df_pivoted= heatmap_df.pivot_table(
        index='weekday', 
        columns='week', 
        values='#', 
        aggfunc='sum', 
        fill_value=0
        )[weeks_ordered] # preserve weeks order
    date_df_pivoted = heatmap_df.pivot_table(
        index='weekday',
        columns='week',
        values='date_str',
        aggfunc='first',
        fill_value=""
    )[weeks_ordered] # preserve weeks order
    orders_df_pivoted = heatmap_df.pivot_table(
        index='weekday',
        columns='week',
        values='orders',
        aggfunc='first',
        fill_value=""
    )[weeks_ordered] # preserve weeks order
    # Reorder weekdays (Monday to Sunday), i.e. preserve days order
    heatmap_df_pivoted = heatmap_df_pivoted.reindex([
        'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
    ])
    date_df_pivoted = date_df_pivoted.reindex([
        'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
    ])
    orders_df_pivoted = orders_df_pivoted.reindex([
        'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
    ])
    # Create the heatmap
    fig = plotly.graph_objs.Figure(
            plotly.graph_objs.Heatmap(
                x=[str(w) for w in weeks_ordered],  # weeks on the x-axis, 
                                                    # preserve order
                y=heatmap_df_pivoted.index,     # weekdays on the y-axis
                z=heatmap_df_pivoted.values,    # values for the heatmap
                customdata = np.dstack((
                    date_df_pivoted.values,
                    orders_df_pivoted.values
                )), # value for hover
                xgap=5,
                ygap=5,
                showscale=False,        # disable the colorbar
                hoverongaps=False,      # disable hover for missing values
                # TODO. Use the secondary box to display the order for days with >0 pizzas.
                #hovertemplate=("We had %{z} pizzas on this day" +
                #               "<extra></extra>" # remove the secondary box
                #               ),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>" +
                    "<extra>" +
                    "We had %{z} pizzas on this day<br>" +
                    "%{customdata[1]}" +
                    "</extra>"
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
    if OFFLINE:
        '''
        # NOTE. The following code is a workaround to display the heatmap in an interactive window, as plotly.offline.iplot() does not work in this script (it works in Jupyter notebooks). Unfortunately, a browser tab is opened, but the heatmap does not show up until the page times out.
        import tempfile
        import plotly.io as pio
        
        pio.renderers.default = "browser"
        tmp_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        fig.write_html(tmp_file.name,
                   include_plotlyjs=True,
                   full_html=True,
                   config = {'displayModeBar': False} # disable the toolbar
                   )
        '''
        
        fig.show()