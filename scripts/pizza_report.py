"""
Generate an image with summary graphs of pizza orders.
"""

import os
import datetime
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

from pizza_chart import pizza_chart

SHOW = False # set to True for debugging
SOURCE = 'default'  # `default` or `custom`

def get_or_empty_order(df_subset):
    """
    Generate an order from a dataframe subset.
    If no data, returns a mock empty order for display.
    """
    if df_subset.empty:
        return [('No pizza', 1)]
    
    order = []
    for p in df_subset['Pizza'].unique(): 
        order.append((p, 
                     sum(df_subset['#'].loc[df_subset['Pizza']==p])
                     ))
    return order
                
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
    now = datetime.datetime.now()
    
    # Plot pizza chart of last order
    df_last_time = df[['Pizza', '#']].loc[df['Date']==df['Date'].max()]
    title=('Last time\n' +
          df['Date'].max().strftime("%d/%m/%Y"))
    order = [(row['Pizza'], row['#'])
            for __, row in df_last_time.iterrows()
            ]
    for theme in ['dark', 'light']:
        fig_last_time = pizza_chart.plot(order, show=False,
                                         title=title,
                                         theme=theme,
                                         source=SOURCE
                                        )
        fpath = os.path.join(charts_dir, 
                             'last_time_{}.png'.format(theme)
                             )
        plt.savefig(fpath,
                    transparent=True,
                    bbox_inches='tight'
                    )
    
    # Plot pizza chart of last month
    last_month_date = now - pd.DateOffset(months=1) + pd.Timedelta(days=1)
    df_last_month = df[['Pizza', '#']].loc[df['Date']>=last_month_date]
    title=('Last month\n' +
          '{} - {}'.format(last_month_date.strftime("%d/%m/%Y"),
                           now.strftime("%d/%m/%Y")
                            )
           )
    order = get_or_empty_order(df_last_month)
    for theme in ['dark', 'light']:
        fig_last_time = pizza_chart.plot(order, show=False,
                                         title=title,
                                         theme=theme,
                                         source=SOURCE
                                        )
        fpath = os.path.join(charts_dir, 
                             'last_month_{}.png'.format(theme)
                             )
        plt.savefig(fpath,
                    transparent=True,
                    bbox_inches='tight'
                    )
        
    # TODO. Add 'last year' graph when data will span more than one year.
    
    # Plot pizza chart of all times
    title=('All times\n' +
          '{} - {}'.format(df['Date'].min().strftime("%d/%m/%Y"),
                           now.strftime("%d/%m/%Y")
                           )
           )   
    order = []
    for p in df['Pizza'].unique(): 
        order.append((p, 
                     sum(df['#'].loc[df['Pizza']==p])
                     ))
    for theme in ['dark', 'light']:
        fig_last_time = pizza_chart.plot(order, show=False,
                                         title=title,
                                         theme=theme,
                                         source=SOURCE
                                        )
        fpath = os.path.join(charts_dir, 
                             'all_time_{}.png'.format(theme)
                             )
        plt.savefig(fpath,
                    transparent=True,
                    bbox_inches='tight'
                    )
        
    # Show the plots
    if SHOW:
        plt.show()

    # Stack images horizontally into a single image.
    # Adapted from https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
    for theme in ['dark', 'light']:
        images = [Image.open(os.path.join(charts_dir, img))
                  for img in ['last_time_{}.png'.format(theme), 
                              'last_month_{}.png'.format(theme), 
                              'all_time_{}.png'.format(theme)]]
        widths, heights = zip(*(img.size for img in images))
        # Create blank image with size equal to three images
        total_width = sum(widths)
        max_height = max(heights)
        img_hstack = Image.new('RGBA', (total_width, max_height))
        # Fill the blank image with pixel values from individual images
        x_offset = 0
        for img in images:
            img_hstack.paste(img, (x_offset,0))
            x_offset += img.size[0]
        img_hstack.save(os.path.join(charts_dir, 
                        'summary_{}.png'.format(theme))
                        )

