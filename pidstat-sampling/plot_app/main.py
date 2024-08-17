from arguments import *

from pathlib import Path
from parsers import *
from plot import *
from bokeh.plotting import output_file, save
from bokeh.layouts import column



def main():

    plots = []

    for pidstat_file in files:
        fName = pidstat_file.stem
        # Parse file:
        print(f"Parsing {pidstat_file}...")
        num_cpus, df = parse_pidstat_file(pidstat_file, mode, rel_ts)
        print(f"Completed! Found {len(df)} records for {num_cpus} CPU!")

        if save_csv:
            print("Storing csv file for", fName)
            df.to_csv(f'{fName}.csv')

        if split_plot is not None:
            for app_name in split_plot:
                if app_name not in df.columns:
                    print(f"WARNING!: {app_name} not found at {fName}")
                else:
                    df_aux = df[df['Command'] == app_name]
                    plots.append(plot_with_bokeh(df_aux, f"{pidstat_file} : {app_name} PIDs"))
        else:
            plots.append(plot_with_bokeh(df, f"{pidstat_file}", mode))


    layout = column(*plots, sizing_mode="stretch_width")

    # SAVE or SHOW PLOT?
    save_name = input("save plot (NO/NAME)?\n")
    if save_name != "NO":
        output_file(save_name+".html", save_name)
        save(layout)
    else:
        show(layout)


if __name__ == "__main__":
    main()
