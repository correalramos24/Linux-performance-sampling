import sys
from pathlib import Path
from parsers import *
from plot import *
from bokeh.plotting import figure, show
from bokeh.layouts import column

USE_REALTIVE_TS=True
DROP_PIDS=False
DROP_PIDS_AGRESIVE=True

def main():

    #Argument parsing:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <pidstat-log-file>")
        sys.exit(1)
    
    
    plots = []

    for pidstat_file in sys.argv[1:]:
        # Parse file:
        #pidstat_file = Path(sys.argv[1])
        print(f"Parsing {pidstat_file}...")
        num_cpus, df = parse_pidstat_file(pidstat_file)
        print(f"Completed! Found {len(df)} records for {num_cpus} CPU!")

        # Convert timestamp to human-readable:
        if USE_REALTIVE_TS:
            min_timestamp = df['Timestamp'].min()
            df['Timestamp'] = df['Timestamp'] - min_timestamp
        else:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

        if DROP_PIDS:
            orinal_size=len(df)
            # DROP PIDS that ! any >= 5% CPU usage
            ids_to_keep = df.groupby('PID').filter(lambda x: (x['%CPU'] >= 5).any())['PID'].unique()
            df = df[df['PID'].isin(ids_to_keep)]
            
            # DROP PIDs that more than /2 are NaN
            threshold = len(df.columns) / 3
            df = df.dropna(thresh=threshold)

            print(f"DROP ENABLE!: FROM {orinal_size} to {len(df)}")

    #print(df)
    #plot_pidstat(num_cpus, df)
        df_nemo = df[df['Command'] == 'nemo']
        df_mmfsd = df[df['Command'] == 'mmfsd']
        df_others = df[df['Command'] != 'nemo']
        plots.append(plot_with_bokeh(df_nemo, f"{pidstat_file} : nemo PIDs"))
        plots.append(plot_with_bokeh(df_mmfsd, f"{pidstat_file} : mfsd PIDs"))
        plots.append(plot_with_bokeh(df_others, f"{pidstat_file} : others PIDs"))


    layout = column(*plots, sizing_mode="stretch_width")
    show(layout)
    


if __name__ == "__main__":
    main()
