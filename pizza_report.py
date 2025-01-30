import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from pizza_chart import plot_pizza_chart

# Generate Markdown report of relevant pizza-stats
# TODO. Create `.md` file with summary.

def _empty_par(n):
    # Write `n` empty paragraph for vertical spacing.
    string = '\n\n'
    for i in range(n):
        string += '&nbsp;\n\n'
    return string

def _align_text(text, header=None, align='right'):
    #assert align in ['right', 'left', 'justify'], "Value of `align` must be `right`, `left` or `justify`."
    header = "<h2>{}\n</h2>".format(header) if header else ""
    return "<div style='text-align: {}'> {}{} </div>".format(align, 
                                                            header,
                                                            text
                                                            )

def _align_img(img, align='right'):
    return "<img style='float: {};' src='{}'>".format(align,
                                                            img
                                                            )


SHOW = False
# Override default line colors according to black or white background
# k: black, w: white
WEDGEPROPS = {'edgecolor': 'k' }
TEXTPROPS = {'color': 'w'}


if __name__ == '__main__':
    root = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_excel(os.path.join(root, 'data', 'data.xlsx'),
                       sheet_name='Orders',
                       usecols=[0, 1, 2, 3])
    # Order the dataframe by date
    df['Date'] = pd.to_datetime(df['Date'],
                                format='%y-%m-%d')
    df = df.sort_values(by='Date', ascending=False)
    now = datetime.datetime.now()
    
    # Create Markdown report
    f = open(os.path.join(root,
                          'assets',
                          'report',
                          'PIZZA_REPORT.md'), 
                          'w+'
            )
    f.write('# Pizza charts @ WE-COBOT\n')
    # Plot pizza chart of last order
    df_last_time = df[['Pizza', '#']].loc[df['Date']==df['Date'].max()]
    order = [(row['Pizza'], row['#'])
             for __, row in df_last_time.iterrows()
            ]
    fig_last_time = plot_pizza_chart(order, show=False,
                                     wedgeprops=WEDGEPROPS,
                                     textprops=TEXTPROPS
                                     )
    plt.savefig(os.path.join(root, 'assets', 'charts', 'last_time.png'),
                transparent=True,
                bbox_inches='tight'
                )
    # Write corresponding report section
    f.write(_align_img('./assets/charts/last_time.png', 
                       align='right'
                       ))
    f.write(_empty_par(4))
    f.write(_align_text(header='Last time',
                        text=df['Date'].max().strftime('%d/%m/%Y'),
                        align='left'
                        ))
    f.write(_empty_par(4))
    
    # Plot pizza chart of last month
    df_last_month = df[['Pizza', '#']].loc[df['Date']>(now-pd.DateOffset(months=1))]
    order = []
    for p in df_last_month['Pizza'].unique(): 
        order.append((p, 
                     sum(df_last_month['#'].loc[df_last_month['Pizza']==p])
                     ))
    fig_last_month = plot_pizza_chart(order, show=False,
                                      wedgeprops=WEDGEPROPS,
                                      textprops=TEXTPROPS
                                      )
    plt.savefig(os.path.join(root, 'assets', 'charts', 'last_month.png'),
                transparent=True,
                bbox_inches='tight'
                )
    # Write corresponding report section
    f.write(_align_img('./assets/charts/last_month.png', 
                       align='left'
                       ))
    f.write(_empty_par(4))
    f.write(_align_text(header='Last month',
                        text=(now-pd.DateOffset(months=1)).strftime('%d/%m/%Y')+ 
                        ' - ' +
                        now.strftime('%d/%m/%Y'),
                        align='right'
                        ))
    f.write(_empty_par(4))

    ''' TODO. Uncomment when data will span more than one year.
    # Plot pizza chart of last year
    df_last_year = df[['Pizza', '#']].loc[df['Date']>(now-pd.DateOffset(years=1))]
    order = []
    for p in df_last_year['Pizza'].unique(): 
        order.append((p, 
                     sum(df_last_year['#'].loc[df_last_year['Pizza']==p])
                     ))
    fig_last_year = plot_pizza_chart(order, show=False)
    plt.savefig(os.path.join(root, 'assets', 'charts', 'last_year.png'),
                transparent=True,
                bbox_inches='tight'
                )
    # Write corresponding report section
    f.write(_align_text(header='Last year',
                        text=(now-pd.DateOffset(years=1)).strftime('%d/%m/%Y')+ 
                             ' - ' +
                             now.strftime('%d/%m/%Y'),
                        align='left'
                        ))
    f.write(_align_img('./assets/charts/last_year.png', 
                       align='left'
                       ))
    '''
    # Plot pizza chart of all times
    order = []
    for p in df['Pizza'].unique(): 
        order.append((p, 
                     sum(df['#'].loc[df['Pizza']==p])
                     ))
    fig_overall = plot_pizza_chart(order, show=False,
                                   wedgeprops=WEDGEPROPS,
                                   textprops=TEXTPROPS
                                  )
    plt.savefig(os.path.join(root, 'assets', 'charts', 'all_time.png'),
                transparent=True,
                bbox_inches='tight'
                )
    # Write corresponding report section
    f.write(_align_img('./assets/charts/all_time.png', 
                       align='right'
                       ))
    f.write(_empty_par(4))
    f.write(_align_text(header='All time',
                        text=df['Date'].min().strftime('%d/%m/%Y')+
                             ' - ' +
                             now.strftime('%d/%m/%Y'),
                        align='left'
                        ))
    f.write(_empty_par(4))

    # Close the Markdown file
    f.close()
    # Show the plots
    if SHOW:
        plt.show()


