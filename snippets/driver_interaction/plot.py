import sys
from pathlib import Path, PurePath
import os

##################################################
#################### SETUP #######################
##################################################

curr_filename = Path(__file__).parts[-1].strip(".py")
currDir = Path(__file__).parents[0]

##################################################
################# SETTINGS #######################
##################################################

folder_name = "iio_server_working"


##################################################
################# CSV LOADING ####################
##################################################

### SAVE IMPEDANCE AND S-PARAMETERS
import csv, shutil

Data_Path = f"{currDir}/{folder_name}/data"
Plot_Path = f"{Data_Path}/plots"

if (not os.path.exists(Data_Path)):
    raise SystemError(f"No data in path: {Data_Path}")

if (os.path.exists(Plot_Path)):
    shutil.rmtree(Plot_Path)
os.mkdir(Plot_Path)

# Load frequency / time-series data to be plotted here

##################################################
################# PLOTTING  ######################
##################################################

from pylab import *
import pandas as pd

csv_file_list = sorted([file for file in os.listdir(Data_Path)])
sam_rx_files = [file for file in csv_file_list if file.startswith("sam_rx")]
sam_tx_files = [file for file in csv_file_list if file.startswith("sam_tx")]

sam_range_min = -5000
sam_range_max = -1

for i in range(len(sam_rx_files)):
    file_rx = os.path.join(Data_Path, f'sam_rx_{i}')
    file_tx = os.path.join(Data_Path, f'sam_tx_{i}')

    df_rx = pd.read_csv(file_rx, delimiter=',', header=1, names=['timestamp', 'I', 'Q'])
    try:
        df_tx = pd.read_csv(file_tx, delimiter=',', header=1, names=['timestamp', 'I', 'Q'])
    except:
        df_tx = pd.read_csv(os.path.join(Data_Path, f'sam_tx_0'), delimiter=',', header=1, names=['timestamp', 'I', 'Q'])
    fig, ax = plt.subplots(2)
    print(f"Data file path: {file_rx}")
    print(df_rx)
    plt.subplot(2, 1, 1)
    ax[0].plot(df_rx['timestamp'][sam_range_min:sam_range_max], df_rx['I'][sam_range_min:sam_range_max], color='r', label="Original Signal (1 kHz)")
    ax[0].plot(df_rx['timestamp'][sam_range_min:sam_range_max], df_rx['Q'][sam_range_min:sam_range_max], color='b', label="Original Signal (1 kHz)")
    ax[0].title.set_text('RX')

    ax[0].set_xticks(np.linspace(df_rx['timestamp'][sam_range_min:sam_range_max].min(), df_rx['timestamp'][sam_range_min:sam_range_max].max(), 10))
    yticks_min = min(df_rx['I'][sam_range_min:sam_range_max].min(), df_rx['Q'][sam_range_min:sam_range_max].min())
    yticks_max = max(df_rx['I'][sam_range_min:sam_range_max].max(), df_rx['Q'][sam_range_min:sam_range_max].max())
    ax[0].set_yticks(np.linspace(yticks_min, yticks_max, 10))

    plt.subplot(2, 1, 2)
    ax[1].plot(df_tx['timestamp'][sam_range_min:sam_range_max], df_tx['I'][sam_range_min:sam_range_max], color='r', label="Original Signal (1 kHz)")
    ax[1].plot(df_tx['timestamp'][sam_range_min:sam_range_max], df_tx['Q'][sam_range_min:sam_range_max], color='b', label="Original Signal (1 kHz)")
    ax[1].title.set_text('TX')

    ax[1].set_xticks(np.linspace(df_tx['timestamp'][sam_range_min:sam_range_max].min(), df_tx['timestamp'][sam_range_min:sam_range_max].max(), 10))
    yticks_min = min(df_tx['I'][sam_range_min:sam_range_max].min(), df_tx['Q'][sam_range_min:sam_range_max].min())
    yticks_max = max(df_tx['I'][sam_range_min:sam_range_max].max(), df_tx['Q'][sam_range_min:sam_range_max].max())
    ax[1].set_yticks(np.linspace(yticks_min, yticks_max, 10))


    plt.suptitle("Time [ms]", size=16)
    plt.tight_layout()
    # plt.show()
    fig.savefig(f"{Plot_Path}/plt_{i}.png")
    plt.close()