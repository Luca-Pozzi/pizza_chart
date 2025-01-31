'''
Generate an image with summary graphs of pizza orders.
TODO.
    - [x] create light and dark mode images
    - [ ] add titles w/ dates
    - [ ] paste the images together in a single image 
'''

import os
import datetime
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

from pizza_chart import plot_pizza_chart

SHOW = False # set to True for debugging

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
    now = datetime.datetime.now()
    
    # Plot pizza chart of last order
    df_last_time = df[['Pizza', '#']].loc[df['Date']==df['Date'].max()]
    title=df['Date'].max().strftime("%d/%m/%Y")
    order = [(row['Pizza'], row['#'])
            for __, row in df_last_time.iterrows()
            ]
    for dark_theme in [True, False]:
        fig_last_time = plot_pizza_chart(order, show=False,
                                         title=title,
                                         dark_theme=dark_theme
                                        )
        suffix = 'dark' if dark_theme else 'light'
        fpath = os.path.join(charts_dir, 
                             'last_time_{}.png'.format(suffix)
                             )
        plt.savefig(fpath,
                    transparent=True,
                    bbox_inches='tight'
                    )
    
    # Plot pizza chart of last month
    df_last_month = df[['Pizza', '#']].loc[df['Date']>(now-pd.DateOffset
    (months=1))]
    title="{} - {}".format((now-pd.DateOffset(months=1)).strftime("%d/%m/%Y"),
                           now.strftime("%d/%m/%Y")
                           )
    order = []
    for p in df_last_month['Pizza'].unique(): 
        order.append((p, 
                     sum(df_last_month['#'].loc[df_last_month['Pizza']==p])
                     ))
    for dark_theme in [True, False]:
        fig_last_time = plot_pizza_chart(order, show=False,
                                         title=title,
                                         dark_theme=dark_theme
                                        )
        suffix = 'dark' if dark_theme else 'light'
        fpath = os.path.join(charts_dir, 
                             'last_month_{}.png'.format(suffix)
                             )
        plt.savefig(fpath,
                    transparent=True,
                    bbox_inches='tight'
                    )
        
    # TODO. Add 'last year' graph when data will span more than one year.
    
    # Plot pizza chart of all times
    title="{} - {}".format(df['Date'].min().strftime("%d/%m/%Y"),
                           now.strftime("%d/%m/%Y")
                           )    
    order = []
    for p in df['Pizza'].unique(): 
        order.append((p, 
                     sum(df['#'].loc[df['Pizza']==p])
                     ))
    for dark_theme in [True, False]:
        fig_last_time = plot_pizza_chart(order, show=False,
                                         title=title,
                                         dark_theme=dark_theme
                                        )
        suffix = 'dark' if dark_theme else 'light'
        fpath = os.path.join(charts_dir, 
                             'all_time_{}.png'.format(suffix)
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
    for dark_theme in [True, False]:
        suffix = 'dark' if dark_theme else 'light'
        images = [Image.open(os.path.join(charts_dir, img))
                  for img in ['last_time_{}.png'.format(suffix), 
                              'last_month_{}.png'.format(suffix), 
                              'all_time_{}.png'.format(suffix)]]
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
                        'summary_{}.png'.format(suffix))
                        )

