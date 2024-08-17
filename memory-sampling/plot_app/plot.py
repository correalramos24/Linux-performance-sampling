
import pandas as pd

def plot_plt_mem_perc(results: list[pd.DataFrame], 
                      hostnames: list[str],
                      plot_swap: bool,
                      output_units: str = "KiB",
                      plot_perc: bool = False,
                      plot_total: bool = False,
                      plot_legend : bool = False,
                      save_plot = None,
                      avail_mode: bool = False,
                      plot_title : str = "Memory usage"
                      
):
    import matplotlib.pyplot as plt

    # PLOT SETUP:
    fig, ax = plt.subplots(figsize=(20,10))
    ax.set_title(plot_title)
    ax.set_xlabel('Time [s]')
    if plot_perc:
        print("Plotting % of memory")
        ax.set_ylabel(f'Memory [%]')
        ax.set_ylim(-1,100)
    elif avail_mode:
        print("Ploting available memory statistic!")
        ax.set_ylabel(f'Memory [{output_units}]')
    else:
        print("Plotting used memory statistic")
        ax.set_ylabel(f'Memory [{output_units}]')

    # PLOT EACH MEM_INFO:
    for host, mem_info in zip(hostnames, results):
        if plot_perc:
            ax.plot(mem_info["timing"], mem_info["used_perc"], 
                    label=f"{host} used mem %")
        elif avail_mode:
            ax.plot(mem_info["timing"], mem_info["available"], 
                    label=f"{host} avail mem", color="orange")
        else:
            ax.plot(mem_info["timing"], mem_info["used"], 
                    label=f"{host} used mem")
        if plot_total and not plot_perc:
            ax.plot(mem_info["timing"], mem_info["total"], 
                    label=f"{host} total mem", color="black")

        if plot_swap:
            if plot_perc:
                ax.plot(mem_info["timing"], mem_info["used_swap_perc"], 
                        label=f"{host} used swap %")
            else:
                ax.plot(mem_info["timing"], mem_info["used_swap"], 
                        label=f"{host} used swap")
            if plot_total and not plot_perc:
                ax.plot(mem_info["timing"], mem_info["total"], 
                        label=f"{host} total swap", color="grey")
    
    # SHOW/SAVE/RESIZE:
    fig.set_tight_layout(True)
    if plot_legend:
        ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    if save_plot is not None:
        print(save_plot+ " generated")
        fig.savefig(save_plot)
    else:
        plt.show()