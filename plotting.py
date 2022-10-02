import pandas
from detecting import df
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import HoverTool, ColumnDataSource

df["Start_str"] = pandas.to_datetime(df["Start"], format="%Y-%m-%d %H:%M:%S")
df["Start_str"] = df["Start_str"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_str"] = pandas.to_datetime(df["End"], format="%Y-%m-%d %H:%M:%S")
df["End_str"] = df["End_str"].dt.strftime("%Y-%m-%d %H:%M:%S")
print(df["Start_str"])

cds = ColumnDataSource(df)

p = figure(width=500, height=250, x_axis_type="datetime", title="Motion Graph", sizing_mode="stretch_both")
p.yaxis.minor_tick_line_color = None
p.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start", "@Start_str"), ("End", "@End_str")])
p.add_tools(hover)

q = p.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

output_file("Graph.html")
show(p)