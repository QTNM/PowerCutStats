import sys
sys.path.append("../")

from __init__ import *
from data_tools import *
from testing import *

path_to_dir = '../data/simulations_truth/' # Path to data
file_name = 'He0HAtomicScatters.pkl'

path = path_to_dir + file_name

# save = True # Change this to not save

def validate_events(path):
    """ Generates histograms of all the values in the data frame to validate event data by eye

    Args:
        path (str): path to the data frame (.pkl file)
    """
    
    data_frame = pd.read_pickle(path)
    
    print(data_frame.columns)
    
    # delete the file name column
    del data_frame['File_name']
    
    # iterate through data_frame columns and plot histograms of all the values
    for column in data_frame.columns:
        plt.hist(data_frame[column])
        plt.title(column)
        plt.show()