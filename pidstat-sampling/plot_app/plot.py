
import pandas as pd
import matplotlib.pyplot as plt


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
    plt.tight_layout()
    plt.show()