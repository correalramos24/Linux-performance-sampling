
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import viridis

def plot_with_bokeh(df: pd.DataFrame, title: str, mode="cpu"):
    pids = df['PID'].unique()
    names= df['Command'].unique()

    if mode == "cpu":
        y_axis="CPU Usage (%)"
    if mode == 'io':
        y_axis="kB_rd/s"

    print(df.head(6))

    p = figure( title=title, 
                x_axis_label='Time', 
                y_axis_label=y_axis,
                sizing_mode="stretch_width")
    #print(f"Found {len(pids)}  unique PIDs")
    #print(f"Found {len(names)} unique PID names")
    
    color_palette = viridis(len(pids))
    #colors = dict(zip(names, color_palette))

    for i, pid in enumerate(pids):
        pid_data = df[df['PID'] == pid]
        command = df[df['PID'] == pid]["Command"].iloc[0]
        source = ColumnDataSource(pid_data)
        if mode == "cpu":
            p.line('Timestamp', '%CPU', source=source, line_width=2, color=color_palette[i])
        if mode == 'io':
            p.line('Timestamp', "kB_rd/s", source=source, line_width=2, color=color_palette[i])
            #p.line('Timestamp','kB_wr/s', source=source, line_width=2, color=color_palette[i])
            #p.line('Timestamp','kB_ccwr/s', source=source, line_width=2, color=color_palette[i])
            #p.line('Timestamp','iodelay', source=source, line_width=2, color=color_palette[i])           
            

    hover = HoverTool()
    hover.tooltips = [
        ("Timestamp", "@Timestamp"),
        ("PROC", "@Command")
    ]
    p.add_tools(hover)
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
