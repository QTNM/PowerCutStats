import sys
sys.path.append("../")

from __init__ import *
from data_tools import *
from testing import *


save_dir = '../data/simulations_truth/'
save_name = 'TrueHeliumScatters_test'

path_to_dir = '/Users/nathan/Desktop/HeFractionScatters/TrueHeliumScatters/' # Path to data




save_csv = '.csv'
save_pkl = '.pkl'

save_path_csv = save_dir + save_name + save_csv
save_path_pkl = save_dir + save_name + save_pkl

save = True # Change this to not save

if __name__ == "__main__":

    # Insert path to file directory here:

    file_list = glob.glob(path_to_dir + '*.h5', recursive=True) # List of Files
    file_sim_list = [] # New List of Files

    path_prefix = '../../../../' # Path Prefix

    for f in file_list: # Iterate through list of Files
        suffix = f.split('nathan/')[-1] # Get the suffix of the file
        true_path = path_prefix + suffix # Get the true path of the file
        file_sim_list.append(true_path) # Append the true path to the new list




    data_container = []

    for i, f in enumerate(file_sim_list):
     
        try:
            signal_strings, keys, data = get_attributes(f, full_path=True)
            filename = f.split('/')[-1]
            trap_type = f.split('/')[-3]
            
            keys.insert(0, 'File_name')
            
                
            
            if i == 0: # Initialise dictionary
            
                data_dict = {key: [] for key in keys}
            
            for j, key in enumerate(keys):
                if j == 0:
                    value = filename
                else:
                    value = data[0][j-1]
                
                # if isinstance(value, np.ndarray):
                #     value = list(value)
        
                    
                data_dict[key].append(value)
                
            if i % 100 == 0:
                print(f'{i} files processed')

        except:
            print(f'Error in file {f}')

        
        
            
        
    df = pd.DataFrame(data_dict)
    
    if save == True:
        
        df.to_csv(save_path_csv, index=False)
        df.to_pickle(save_path_pkl)
        print('Data saved to csv and pickle')
        

