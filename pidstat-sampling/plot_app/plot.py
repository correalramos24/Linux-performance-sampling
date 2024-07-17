
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Turbo256

def plot_with_bokeh(df: pd.DataFrame, title: str):
    pids = df['PID'].unique()
    p = figure( title=title, 
                x_axis_label='Time', 
                y_axis_label='CPU Usage (%) blue - SYS Time (%) red - WAIT %',
                sizing_mode="stretch_width")
    
    

    for i, pid in enumerate(pids):
        pid_data = df[df['PID'] == pid]
        command = df[df['PID'] == pid]["Command"].iloc[0]
        source = ColumnDataSource(pid_data)
        p.line('Timestamp', '%CPU', source=source, line_width=2, color="blue")
#        p.line('Timestamp', '%system', source=source, line_width=2, color="red")
#        p.line('Timestamp', '%wait', source=source, line_width=2, color="orange")

    hover = HoverTool()
    hover.tooltips = [
        ("Timestamp", "@Timestamp"),
        ("PROC", "@Command")
    ]
    p.add_tools(hover)
    #show(p)
    return p




def plot_pidstat(num_cpus : int, df: pd.DataFrame):
    pivot_df = df.pivot(index='Timestamp', columns='PID', values="%CPU")
    pid_to_command = df.drop_duplicates(subset=['PID'])[['PID', 'Command']].set_index('PID')['Command']

    # Graficar
    plt.figure(figsize=(10, 6))

    for pid in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[pid], label=pid_to_command[pid])

    plt.title('Variación de %CPU por PID')
    plt.xlabel('Timestamp')
    plt.ylabel('%CPU')
    plt.legend(title='PID')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.show()
