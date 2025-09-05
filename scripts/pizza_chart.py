# Adapted from: https://stackoverflow.com/questions/44528024/insert-image-into-pie-chart-slice/44529673#44529673

import os
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

THEMES = {'dark':  {'plt_style': 'dark_background',
                   'textprops': {'color': 'white'},
                   'wedgeprops': {'fill': False,
                               'edgecolor': '#0d1117', # GitHub dark theme grey
                               'linewidth': 2}
                  },
          'light': {'plt_style': 'default',
                    'textprops': {'color': 'black'},
                    'wedgeprops': {'fill': False,
                                'edgecolor': 'w',
                                'linewidth': 2}
                    }
         }

def plot_pizza_chart(order, title=None, cutoff=7.0, source='default', 
                     show=True, theme='light', plt_style=None, textprops={}, wedgeprops={}):
    # Ensure correct data type
    order = [(pizza, int(value)) for pizza, value in order]
    # Format data for the plot
    labels = []
    data = []
    stats = []
    tot_num = sum(v for __, v in order)
    others = 0
    for pizza, value in order:
        if value/tot_num * 100 >= cutoff:
            labels.append(pizza)
            data.append(value)
            stats.append('{:.2f}% ({})'.format(value/tot_num*100, 
                                            value)
                        )
        else: # if pizza is less than cutoff, add it to `other` category
            others += value
    if others: # if is any pizza in `other` category, save it here
        labels.append('altro')
        data.append(others)
        stats.append('{:.2f}% ({})'.format(others/tot_num*100, 
                                           others)
                        )

    # Define plot style
    if plt_style:
        plt.style.use(plt_style)
    else:
        plt.style.use(THEMES[theme]['plt_style'])
    textprops = textprops if textprops else THEMES[theme]['textprops']
    wedgeprops = wedgeprops if wedgeprops else THEMES[theme]['wedgeprops']    
    
    # Create the pie chart
    fig, ax = plt.subplots()
    if title:
        plt.title(title, fontdict={'fontsize': 18})
    plt.gca().axis("equal")
    wedges, __ = plt.pie(data, startangle=90, 
                         labels=[lab+'\n'+stat for lab, stat in zip(labels, stats)],
                         explode = [0.1] * len(labels),
                         wedgeprops = wedgeprops,
                         textprops = textprops
                            )
    # Display pizza textures in chart sectors
    if not source == 'custom':
        # Default images are prepended with '_'.
        prefix = '_'
    
    for i in range(len(labels)):
        try:
            fn = os.path.join("assets",
                            "pizzas",
                            "{}{}.png".format(prefix,
                                              labels[i].lower().replace(" ",
                                                                        "_")
                                             )
                            )
            _img_to_pie(fn, wedges[i], xy=(0.0, 0.0), zoom=0.225)
            wedges[i].set_zorder(10)
        except FileNotFoundError:
            print("File {} not found, '{}' slice will appear as empty".format(fn, labels[i].lower()))
            continue
    if show:
        # Plot the figure
        plt.show()
    return fig

def _img_to_pie( fn, wedge, xy, zoom=1, ax = None):
    # Fill pie chart sectors with images
    if ax==None: ax=plt.gca()
    im = plt.imread(fn, format='png')
    path = wedge.get_path()
    patch = PathPatch(path, facecolor='none')
    ax.add_patch(patch)
    imagebox = OffsetImage(im, zoom=zoom, clip_path=patch, zorder=-10)
    ab = AnnotationBbox(imagebox, xy, xycoords='data', pad=0, frameon=False)
    ax.add_artist(ab)