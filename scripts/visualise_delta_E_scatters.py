import sys
sys.path.append("../")

from __init__ import *
from data_tools import *
from testing import *

############################################################################################################


path_to_dir = '../data/simulations_truth/' # Path to data
# file_name = 'He0HAtomicScatters.pkl'
file_name = 'TrueHeliumScatters_test.pkl'

file_names = None
file_names = ['TrueHeliumScatters_test.pkl', 'AtomicHydrogenScatters.pkl']

verbose = True
plot = True


path = path_to_dir + file_name

colours = ['blue', 'red', 'green', 'orange', 'purple', 'black', 'yellow', 'pink', 'brown', 'cyan']


def read_file(path):
    frame = pd.read_pickle(path)
    return frame

def get_energies(frame):
    energies = frame['Delta E [eV]']
    energies = energies.values.flatten()
    energies = np.concatenate([arr[arr != -1] for arr in energies])
    return energies

def get_interaction_times(frame):
    times = frame['Time [seconds]']
    times = np.concatenate([arr[arr != 0] for arr in times])
    return times

def get_total_times(frame):
    total_times = []
    NEW_times = frame['Time [seconds]']
    for arr in NEW_times:
        total_times.append(arr[-1])
    return total_times

def get_info(path):
    frame = read_file(path)
    energies = get_energies(frame)
    file_name = frame['File_name']
    interaction_times = get_interaction_times(frame)
    total_interactions = len(energies)

    total_times = get_total_times(frame)

    return frame, energies, file_name, interaction_times, total_interactions, total_times

def print_info(frame, energies, file_name, interaction_times, total_interactions, total_times):
    if verbose:
        print("Median energy loss per interaction: ", np.median(energies), "eV")
        print("Mean energy loss per interaction: ", np.mean(energies), "eV")
        print("Minimum energy loss: ", np.min(energies), "eV")
        print("Maximum energy loss: ", np.max(energies), "eV")
        print("Total interactions: ", total_interactions)
        print("Average number of interactions: ", total_interactions/frame["File_name"].nunique())


        print("Timing information")
        print("Average event time: ", np.mean(total_times), "seconds")
        print("Median event time: ", np.median(total_times), "seconds")
        print("Average interaction time: ", np.mean(interaction_times), "seconds")
        print("Median interaction time: ", np.median(interaction_times), "seconds")


if __name__ == "__main__":
    
    
    
    
    if file_names == None:
        plt.figure(figsize=(10, 6))
        frame, energies, file_name, interaction_times, total_interactions, total_times = get_info(path)
        if verbose:
            print_info(frame, energies, file_name, 
                       interaction_times, total_interactions, total_times)  
        
        if plot:
            
            
            E_min = 0
            E_max = 100

            upper = np.where(energies > E_min)
            lower = np.where(energies < E_max)
            indices = np.intersect1d(upper,lower)
                
            
            plt.hist(energies[indices], bins=100, color='blue', alpha=0.7, edgecolor='black', histtype='stepfilled')
            plt.xlabel('$\Delta$ E [eV]')
            plt.axvline(24.6, label='Ionisation energy of helium', color='red', linestyle='--')
            plt.axvline(13.6, label='Ionisation energy of hydrogen', color='green', linestyle='--')
            plt.legend()
            plt.ylabel('Frequency')
            plt.show()
            
    else:
        for i, f in enumerate(file_names):
            path = path_to_dir + f
            frame, energies, file_name, interaction_times, total_interactions, total_times = get_info(path)
            if verbose:
                print("\n")
                print("File name: ", f)
                print("--------------------------------")
                print_info(frame, energies, file_name, 
                           interaction_times, total_interactions, total_times)  
                print("--------------------------------")
                print("\n")
                
            if plot:
                
                E_min = 1
                E_max = 100

                upper = np.where(energies > E_min)
                lower = np.where(energies < E_max)
                indices = np.intersect1d(upper,lower)
                
                
                plt.hist(energies[indices], bins=50, alpha=1, color=colours[i], 
                         histtype='step', label=f, density=False)
                plt.xlabel('$\Delta$ E [eV]')
                plt.ylabel('Frequency')
                plt.xlim(0, 100)
                plt.legend()
        
        plt.show()