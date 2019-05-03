import pandas as pd
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.models import ColumnDataSource, HoverTool, CustomJS

output_file("hover_callback.html")

points = pd.DataFrame(data = [['loc1',2,6],
                               ['loc2',3,4],
                               ['loc3',5,3],
                               ['loc4',6,8],
                               ['loc5',8,7],
                               ['loc6',7,5]
                               ],
                       columns=['name','x','y'])

links = {
    'loc1': ['loc2', 'loc3'],
    'loc2': ['loc1', 'loc3'],
    'loc3': ['loc1', 'loc2'],
    'loc4': ['loc6'],
    'loc5': [],
    'loc6': ['loc5'],
}

p = figure(plot_width=400, plot_height=400, tools="", toolbar_location=None, title='Hover over points')

sourceS = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})
sr = p.segment(x0='x0', y0='y0', x1='x1', y1='y1', color='olive', alpha=0.6, line_width=3, source=sourceS)

sourceC = ColumnDataSource(data=points)
cr = p.circle('x', 'y', source=sourceC, color='olive', size=30, alpha=0.4, hover_color='olive', hover_alpha=1.0)

# Add a hover tool, that sets the link data for a hovered circle
code = """
var links = %s;
var data = {'x0': [], 'y0': [], 'x1': [], 'y1': []};
var cdata = circle.data;
var col = 'name';
var indices = cb_data.renderer.data_source.inspected['1d'].indices;
var pointA = cdata[col][indices[0]];

console.log(pointA);
console.log(links[pointA]);

//Loop through links
for (var i = 0; i < links[pointA].length; i++) {
    console.log(links[pointA][i]);
    var pointB = links[pointA][i];
    
    //Loop circle data
    for (var j = 0; j < cdata[col].length; j++) {
        if(cdata[col][j] == pointB) {
            data['x0'].push(cdata['x'][indices[0]]);
            data['y0'].push(cdata['y'][indices[0]]);
            data['x1'].push(cdata['x'][j]);
            data['y1'].push(cdata['y'][j]);
        }
    }
}

segment.data = data;
segment.change.emit();
""" % links

callback = CustomJS(args={'circle': sourceC, 'segment': sourceS}, code=code)
p.add_tools(HoverTool(tooltips=[('Name','@name')], callback=callback, renderers=[cr]))

curdoc().add_root(p)
show(p)