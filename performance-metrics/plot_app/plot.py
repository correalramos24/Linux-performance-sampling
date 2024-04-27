import pandas as pd
import matplotlib.pyplot as plt

def plot_results(df: pd.DataFrame):
    for column in df.columns:
        df[column].plot(kind='bar', title=column)
        plt.tight_layout()
        plt.show()