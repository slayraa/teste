#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:50:24 2019

@author: imatos
"""

import numpy as np
from bokeh.io import show
from bokeh.plotting import figure

#Bokeh can draw many types of visual shapes (called glyphs), include lines, bars, patches, hex tiles and more.
#One of the most common visualization tasks is to draw a scatter plot of data using small marker glyphs to 
#represent each point.

p = figure(plot_width=400, plot_height=400, title='Fancy title')
p.title.text_color = "olive"
p.title.text_font = "arial"
p.title.text_font_style = "italic"

# add a circle renderer with x and y coordinates, size, color, and alpha
p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=15, line_color="navy",
         fill_color="orange", fill_alpha=0.5)

#All Bokeh scatter markers accept size (measured in screen space units) as a property
#Circles in particular also have radius (measured in "data" space units)
p.circle([3], [1], line_color="navy", fill_color="green", radius=0.1)
#p.circle_cross([4],[2], size=10, angle=10)

show(p)

#Changing color by selection

from bokeh.models import Circle

p = figure(plot_width=400, plot_height=400, title='Select me!', tools='tap')
p.title.text_color = "olive"
p.title.text_font = "arial"
p.title.text_font_style = "italic"

renderer = p.circle([1, 2, 3, 4, 5], [2, 5, 8, 2, 7], size=50)

selected_circle = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)
nonselected_circle = Circle(fill_alpha=0.2, fill_color="blue", line_color="firebrick")

renderer.selection_glyph = selected_circle
renderer.nonselection_glyph = nonselected_circle

show(p)


#Add hover
#Setting the highlight policy for glyphs that are hovered over is completely analogous to setting the
#selection_glyph or nonselection_glyph, or by passing color or alpha parameters prefixed with "hover_"

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from bokeh.sampledata.glucose import data

output_file("styling_hover.html")

subset = data.loc['2010-10-06']

x, y = subset.index.to_series(), subset['glucose']

# Basic plot setup
plot = figure(plot_width=600, plot_height=300, x_axis_type="datetime", tools="",
              toolbar_location=None, title='Hover over points')

plot.line(x, y, line_dash="4 4", line_width=1, color='gray')

cr = plot.circle(x, y, size=20,
                fill_color="grey", hover_fill_color="firebrick",
                fill_alpha=0.05, hover_alpha=0.3,
                line_color=None, hover_line_color="white")

#plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))
plot.add_tools(HoverTool(tooltips= [('Glucose levels','@y')], renderers=[cr]))

plot.toolbar.autohide = True

show(plot)


#Draw ellipses
from bokeh.plotting import figure, show, output_file

output_file('ellipses.html')

p = figure(plot_width=400, plot_height=400)
p.ellipse(x=[1, 2, 3], y=[1, 2, 3], width=[0.2, 0.3, 0.1], height=0.3, color="#CAB2D6")

show(p)





p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=15, line_color="navy",
         fill_color="orange", fill_alpha=0.5)
show(p)


from bokeh.plotting import figure, output_file, show

output_file("patch.html")

p = figure(plot_width=400, plot_height=400)

p.patches([[1, 3, 2], [3, 4, 6, 6]], [[2, 1, 4], [4, 7, 8, 5]],
          color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=2)

show(p)