import sys
sys.path.append("../")

from __init__ import *
from data_tools import *
from testing import *


save_dir = '../data/simulations_truth/'
save_name = 'GoldenSample'

# path_to_dir = '/Users/nathan/Desktop/HeFractionScatters/TrueHeliumScatters/' # Path to data, this needs to be changed for your local data


path_to_dir = "../../../../Desktop/GoldenSample/" # Path to data, this needs to be changed for your local data


save_csv = '.csv'
save_pkl = '.pkl'
save_pq = '.pq'

save_path_csv = save_dir + save_name + save_csv
save_path_pkl = save_dir + save_name + save_pkl
save_path_pq = save_dir + save_name + save_pq

save = True # Change this to not save



if __name__ == "__main__":

    # Insert path to file directory here:

    file_list = glob.glob(path_to_dir + '*.h5', recursive=True) # List of Files
    file_list = glob.glob(path_to_dir + '**/*.h5', recursive=True) # List of Files for within subdirectories
    
    data_container = []
    
    data_dict = None
    initialised = False

    for i, f in enumerate(file_list):
  
     
        try:
            signal_strings, keys, data = get_attributes(f, full_path=True)
            filename = f.split('/')[-1]
            trap_type = f.split('/')[-3]
            
            keys.insert(0, 'File_name')
            
               
            if not initialised : # Initialise dictionary
            
                data_dict = {key: [] for key in keys}
                initialised = True
            
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
            
            if data_dict is not None:
                for key in keys:
                    data_dict[key].append(np.nan)
        
    df = pd.DataFrame(data_dict)
    
    if save == True:
        
        df.to_csv(save_path_csv, index=False)
        df.to_pickle(save_path_pkl)
        df.to_parquet(save_path_pq)
        print('Data saved to csv and pickle')
        

