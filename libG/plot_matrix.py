import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models import FuncTickFormatter, FixedTicker, ColumnDataSource, LogColorMapper, LinearColorMapper, HoverTool
from bokeh.embed import components
from bokeh.layouts import gridplot, row, column, widgetbox
from bokeh.palettes import Viridis256, Magma256, Inferno256, Magma7
from sklearn.preprocessing import MinMaxScaler
from bokeh.io import output_notebook
output_notebook()


def plot_matrix(df, title='', log_color=False, palette=Viridis256, width=600, height=600, normalize=False):
    df_orig = df.copy()
    if normalize:
        scaler = MinMaxScaler((0.01,1.))
        scaled_values = scaler.fit_transform(df)
        df.loc[:,:] = scaled_values
    else:
        df = df.copy()
 

    index_Names = df.index.tolist()
    column_Names = df.columns.tolist()
    df.index.name, df.columns.name = 'Index', 'Column'
    df.reset_index(inplace=True)


    melted = pd.melt(df, id_vars=df.columns[0])
    melted['x'] = melted.Column.map({v:k+0.5 for k, v in enumerate(melted.Column.unique().tolist())})
    melted['y'] = melted.Index.map({v:df.shape[0] - k - 0.5 for k, v in enumerate(melted.Index.unique().tolist())})

 
    plot_options = dict(plot_width=width, plot_height=height,
                        x_axis_location="above",
                        x_axis_label = "Column",
                        y_axis_label = "Index",
                        x_range = [str(x) for x in column_Names],
                        y_range = list(reversed([str(x) for x in index_Names])))

 
    source = ColumnDataSource(melted)
    df_orig.reset_index(inplace=True)
    melted_orig = pd.melt(df_orig, id_vars=df_orig.columns[0])
    source.add(melted_orig['value'], 'original_value')

    hover = HoverTool(tooltips=[('Index', '@Index'),

                                ('Column', '@Column'),

                                ('Value','@original_value')])


    if log_color:
        color_mapper = LogColorMapper(palette=palette)
    else:
        color_mapper = LinearColorMapper(palette=palette)

   
    p = figure(tools= ["reset", "box_zoom", "wheel_zoom", "pan"] + [hover], title=title, **plot_options)
    p.rect(x="x", y="y",width=1, height=1, source = source,
           color={'field': 'value', 'transform': color_mapper})
 

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3


    show(p)

