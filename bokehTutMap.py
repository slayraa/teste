#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:39:38 2019

@author: imatos
"""

#from pathlib import Path
import pandas as pd
import numpy as np
#import json

from bokeh.io import output_file, show, curdoc
from bokeh.models import HoverTool
from bokeh.models.widgets import Toggle, Slider
from bokeh.layouts import widgetbox, column, row
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors


# transform coordinates into bokeh understandable measurements
def merc(r):
    lat = float(r['lat'])
    lon = float(r['long'])
    
    r_major = 6378137.000
    x = r_major * np.radians(lon)
    scale = x/lon
    y = 180.0/np.pi * np.log(np.tan(np.pi/4.0 + lat * (np.pi/180.0)/2.0)) * scale
    return x,y

dataGeo = pd.DataFrame(data = [['loc1','a','39.19501252187821','-8.9154052734375','red','2016'],
                               ['loc2','b','39.23331686919235','-8.817901611328125','blue','2017'],
                               ['loc3','c','39.175852513006284','-8.837127685546875','green','2016']
                               ],
                       columns=['name','type','lat','long','color','year'])

dataGeo['merc_x'], dataGeo['merc_y'] = zip(*dataGeo[['lat','long']].apply(merc, axis=1))

dataElli = pd.DataFrame(data = [[-992458.3752547285, 4749644.06358428, 3500, 2000, 10, ['a','b','c'], 'c', '#CAB2D6','2016']],
                       columns=['merc_x','merc_y','height','width','angle','sites','type','color','year'])


output_file("mapTryout.html")

#Build map
p = figure(plot_height=600, plot_width=950, x_range=(-1100000, -970000),
           y_range=(4650000, 4699000), x_axis_type="mercator", y_axis_type="mercator")

p.add_tile(get_provider(Vendors.CARTODBPOSITRON))

p.xaxis.visible = False
p.yaxis.visible = False

el = p.ellipse(x='merc_x', y='merc_y', width='width', height='height', angle='angle', source=dataElli,
          alpha=0.7, color='color')

#add hover to ellipses
hover = HoverTool(tooltips = [
        ('Sites','@sites'), ('Type', '@type')], renderers=[el])

p.add_tools(hover)

cr = p.inverted_triangle(x='merc_x', y='merc_y', source=dataGeo, size=20, alpha=0.7,
         fill_color='color', line_color=None)

#add hover to circles
hover2 = HoverTool(tooltips = [
        ('Name','@name'), ('Type', '@type')], renderers=[cr])

p.add_tools(hover2)
p.toolbar.autohide = True

#add buttons
def updateMarkers(old):
    if old == 0:
        toggleMarkers.label="Show Markers"
        cr.visible = False
    else:
        toggleMarkers.label="Hide Markers"
        cr.visible = True

toggleMarkers = Toggle(label="Hide Markers", active=True)
toggleMarkers.on_click(updateMarkers)

def updateEllipses(old):
    if old == 0:
        toggleEllipses.label="Show Ellipses"
        el.visible = False
    else:
        toggleEllipses.label="Hide Ellipses"
        el.visible = True

toggleEllipses = Toggle(label="Hide Ellipses", active=True)
toggleEllipses.on_click(updateEllipses)

layout2 = row(toggleMarkers, toggleEllipses)
layout = column(p, widgetbox(layout2))
curdoc().add_root(layout)

show(layout)