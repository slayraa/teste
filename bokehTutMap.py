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
from bokeh.models import ColumnDataSource, HoverTool, CustomJS
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

def updateMarkers(old):
    if old == 0:
        toggleMarkers.label="Show Markers"
        cr.visible = False
    else:
        toggleMarkers.label="Hide Markers"
        cr.visible = True

def updateEllipses(old):
    if old == 0:
        toggleEllipses.label="Show Ellipses"
        el.visible = False
    else:
        toggleEllipses.label="Hide Ellipses"
        el.visible = True

def update_plot(attr, old, new):
    tm = slider.value
    
    dataEl = dataElli[dataElli['year']==tm]
    dataCr = dataGeo[dataGeo['year']==tm]

    el_source.data = ColumnDataSource(data=dataEl).data
    cr_source.data = ColumnDataSource(data=dataCr).data

    p.title.text = 'Data for day and time, %d' %tm

def animate_update():
        tm = slider.value + 1
        
        if tm > maxTime:
            tm = minTime
        
        slider.value = tm

def automateMap(old):
    global callback_id

    if old == 0:
        bPlay.label="Play"
        curdoc().remove_periodic_callback(callback_id)
    else:
        bPlay.label="Pause"
        callback_id = curdoc().add_periodic_callback(animate_update, 200) 


dataGeo = pd.DataFrame(data = [['loc1','a','39.19501252187821','-8.9154052734375','red',2016],
                               ['loc2','b','39.23331686919235','-8.817901611328125','blue',2017],
                               ['loc3','c','39.175852513006284','-8.837127685546875','green',2016],
                               ['loc4','d','39.23332006919235','-8.817901611328800','black',2017]
                               ],
                       columns=['name','type','lat','long','color','year'])

dataGeo['merc_x'], dataGeo['merc_y'] = zip(*dataGeo[['lat','long']].apply(merc, axis=1))

dataElli = pd.DataFrame(data = [[-992458.3752547285, 4749644.06358428, 3550, 2010, 10, ['a','c'],'c','#CAB2D6',2016],
                                [-992460.3752547285, 4749648.06358428, 3500, 2000, 20, ['b'],'b','red',2017]
                                ],
                       columns=['merc_x','merc_y','height','width','angle','sites','type','color','year'])


links = {
    0: [2],
    1: [3],
    2: [0],
    3: [1]
}

output_file("mapTryout.html")

#define ranges of the map
minTime = dataGeo['year'].min()
maxTime = dataGeo['year'].max()

#Build map
p = figure(plot_height=800, plot_width=1100, x_range=(-1100000, -970000), title = 'Having fun',
           y_range=(4650000, 4699000), x_axis_type="mercator", y_axis_type="mercator")

p.add_tile(get_provider(Vendors.CARTODBPOSITRON))

p.xaxis.visible = False
p.yaxis.visible = False

#create circles and add hover
cr_source = ColumnDataSource(data=dataGeo[dataGeo['year'] == minTime])
cr = p.inverted_triangle(x='merc_x', y='merc_y', source=cr_source, size=20, alpha=0.7,
         fill_color='color', line_color=None)

#create ellipses and add hover
el_source = ColumnDataSource(data=dataElli[dataElli['year'] == minTime])
el = p.ellipse(x='merc_x', y='merc_y', width='width', height='height', angle='angle', source=el_source,
          alpha=0.6, color='color', hover_color='orange', hover_alpha=0.5)

seg_source = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})
sr = p.segment(x0='x0', y0='y0', x1='x1', y1='y1', color='blue', alpha=0.6, line_width=3, source=seg_source, )

code = """
var links = %s;
var data = {'x0': [], 'y0': [], 'x1': [], 'y1': []};
var cdata = circle.data;
var indices = cdata.index;
for (var i = 0; i < indices.length; i++) {
    var ind0 = indices[i]
    for (var j = 0; j < links[ind0].length; j++) {
        var ind1 = links[ind0][j];
        data['x0'].push(cdata.merc_x[ind0]);
        data['y0'].push(cdata.merc_y[ind0]);
        data['x1'].push(cdata.merc_x[ind1]);
        data['y1'].push(cdata.merc_y[ind1]);
    }
}
segment.data = data;
""" % links

callback = CustomJS(args={'circle': cr_source, 'segment': sr.data_source}, code=code)
hover = HoverTool(tooltips = [('Sites','@sites'), ('Type', '@type'), ('Year', '@year')], callback=callback, renderers=[el])
p.add_tools(hover)

hover2 = HoverTool(tooltips = [('Name','@name'), ('Type', '@type'), ('Year', '@year')], renderers=[cr])
p.add_tools(hover2)

#add toggle buttons for ellipses and markers
toggleEllipses = Toggle(label="Hide Ellipses", active=True)
toggleEllipses.on_click(updateEllipses)

toggleMarkers = Toggle(label="Hide Markers", active=True)
toggleMarkers.on_click(updateMarkers)

#add slider
slider = Slider(title = 'Time',start=minTime, end=maxTime, step=1, value=minTime)
slider.on_change('value', update_plot)

#add play button
bPlay = Toggle(label="Play", active=False, button_type="success")
bPlay.on_click(automateMap)

callback_id = None

p.toolbar.autohide = True

#format the layout of the page
layout2 = row(toggleMarkers, toggleEllipses, bPlay)
#layout3 = row(slider)
layout = column(p, widgetbox(layout2, slider))
curdoc().add_root(layout)

show(layout)