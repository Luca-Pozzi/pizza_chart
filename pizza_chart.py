# Adapted from: https://stackoverflow.com/questions/44528024/insert-image-into-pie-chart-slice/44529673#44529673

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def plot_pizza_chart(order, title=None, cutoff=7.0, dark_theme=False,
                    show=True, source='default'):
    labels = []
    data = []
    stats = []
    tot_num = sum([v for __, v in order])
    others = 0
    for pizza, value in order:
        if value/tot_num * 100 >= cutoff:
            labels.append(pizza)
            data.append(value)
            stats.append('{:.2f}% ({})'.format(value/tot_num*100, 
                                            value)
                        )
        else:
            others += value
    if others: # if is any pizza in `other` category, save it here
        labels.append('altro')
        data.append(others)
        stats.append('{:.2f}% ({})'.format(others/tot_num*100, 
                                           others)
                        )

    # Create the pie chart
    if dark_theme:
        plt.style.use("dark_background")
        edgecolor = '#0D1117' #'k'
        # NOTE. The above dark grey is used to match the GitHub dark theme background.
    else:
        plt.style.use("default")
        edgecolor = 'w'
    fig, ax = plt.subplots()
    if title:
        plt.title(title, fontdict={'fontsize': 18})
    plt.gca().axis("equal")
    wedges, __ = plt.pie(data, startangle=90, 
                         labels=[lab+'\n'+stat for lab, stat in zip(labels, stats)],
                         explode = [0.1] * len(labels),
                         wedgeprops = { 'linewidth': 2, 
                                        "edgecolor": edgecolor,
                                        "fill":False,
                                        #**wedgeprops
                                        },
                         #textprops={'color':"grey",
                         #           **textprops
                         #           }
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
            _img_to_pie(fn, wedges[i], xy=(0.0, 0.0), zoom=0.45)
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