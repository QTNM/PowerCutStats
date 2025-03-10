## FFT ROC CURVE GENERATOR

import sys
from pathlib import Path
import os
sys.path.append("../")

from __init__ import *
from data_tools import *
from testing import *
from analysis import *

import argparse

import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'

R, Nch, kb, bw, Nsamp, T= 496.1709043911709, 1, 1.38e-23, 1000e6, 40960, 5 
cut = 1e-8
R = 500 # Value inputted by user 

# Point towards the grid of batch created Events
dir_path = "../../../../Desktop/BatchCreatedFiles/Bathtub/"

def parse_inputs():
    parser = argparse.ArgumentParser(description="Analyze FFTs and generate PDFs/ROC curves.")
    
    # # Required argument: System Temperature
    # parser.add_argument("-T", "--temperature", required=True, help="Value of System Temperature in Kelvin")

    # Optional argument: output location
    parser.add_argument("-o", "--output", default="figures/generated/output.pdf", help="Path to save the output PDF")

    # Optional argument: cut value for FFT peaks
    parser.add_argument("-c", "--cut", type=float, default=1e-8, help="Cut value for FFT peaks")

    # Optional flag: False Positive Rate
    parser.add_argument("-fpr", "--fpr", type=float, default=0.01, help="False Positive Rate for ROC curve")
    
    # Optional flag: Save Data and Plots
    parser.add_argument("--save", action="store_true", help="Include this flag to save data and plots")

    # Parse arguments
    args = parser.parse_args()
    
    # args.temperature = float(args.temperature)
    args.cut = float(args.cut)
    
    # Example usage of arguments
    print(f"Processing files")
    print(f"Saving output to: {args.output}")

    # Add actual processing logic here
    # (e.g., loading FFT, analyzing data, generating plots)
    return args
# =============================================================================

path_to_data = "../../../../Desktop/BatchCreatedFiles/Bathtub/"



# =============================================================================


def calculate_noise_dists(vals, tau, Nsamp):
    ray_cdf = (1-np.exp(-(vals**2)/tau)) ** Nsamp
    ray_pdf = np.gradient(ray_cdf, vals[1]-vals[0])
    
    return ray_cdf, ray_pdf


if __name__ == "__main__":
    
    args = parse_inputs()
    cut = args.cut
    defined_FPR = args.fpr
    
    # # ==== Generating The Data Files we need to use ====
    # # Truth information location
    # truth_path = "../data/simulations_truth/BatchCreatedFilesFor2DPlot_Bathtub.pkl"
    
    # data_frame = pd.read_pickle(truth_path)

    # file_list = data_frame['File_name'].values
    # print(file_list)
    # print(len(file_list))
    
    # true_paths_to_data = []
    # starting_pos = []
    # pitch_angles = []
    
    # print("Initialised Containers")
    
    # for i, file_name in enumerate(file_list):
        
    #     matches = list(Path(path_to_data).rglob(file_name))  # Search recursively
    #     true_paths_to_data.append(matches[0])  # Append the first match
    #     starting_pos.append(np.linalg.norm(data_frame['Starting position [metres]'].values[i]))
    #     pitch_angles.append(data_frame['Pitch angle [degrees]'].values[i])
        
    #     # print(f"Processed {i+1} files")
        
    # print("Generating Initial Data Frame")
    
    # df = pd.DataFrame({'File_name': file_list, 'Path_to_data': true_paths_to_data, 
    #                 'Starting position [metres]': starting_pos,
    #                    'Pitch angle [degrees]': pitch_angles})
    
    # df.to_csv("../data/simulations_truth/2Ddata_Bathtubv1.csv")
    # df.to_pickle("../data/simulations_truth/2Ddata_Bathtubv1.pkl")
    
    # df["Path_to_data"] = df["Path_to_data"].astype(str)
    
    # df.to_parquet("../data/simulations_truth/2Ddata_Bathtubv1.pq")
    
    # print("Initial Data Frame Generated")
    # ## ================ Finished =================================
    
    # ================== Loading in Data Files ====================
    # Loading in data files
    
    # Change Harmonic to Bathtub and vice versa
    # df = pd.read_pickle("../data/simulations_truth/2Ddata_Bathtubv1.pkl")
    
    # true_paths_to_data = df['Path_to_data'].values
    # file_list = df['File_name'].values
    # starting_pos = df['Starting position [metres]'].values
    # pitch_angles = df['Pitch angle [degrees]'].values
    
    # signal_pdfs = []
    # noise_pdfs = []
    
    # signal_cdfs = []
    # noise_cdfs = []
    
    # tpr_vals = []
    # fpr_vals = []
    
    # print("Beginning Processing of Data Files")
    
    # for i, file_name in enumerate(true_paths_to_data):
        
    #     file_name = str(file_name)
        
    #     if i % 10 == 0:
    #         print(f"Processing file no.{i}")
        
    #     signal_strings, attributes, attrs_container = get_attributes(file_name, full_path=True)
    #     signal = get_signal(file_name, signal_strings[0], full_path=True) # One polarisation
        
    #     peaks = get_signal_peaks(signal, cut)
    
    #     R = attrs_container[0][10] # Make sure this is correct [9] for harmonic [10] for bathtub
        
    #     # print(f"Impedance: {R}")
        
    #     n_pwr = kb * args.temperature * bw # noise power    
    #     tau_1t = n_pwr * R # noise variance single channel, time-domain (tau_1t)
    #     tau_1f = tau_1t / Nsamp # noise variance single channel, freq-domain (tau_1f)

    #     threshold = np.linspace(1e-9, 1e-6, 20001) #! This line changes the range of our potential threshold values
    #     x = threshold
        
    #     noise_cdf, noise_pdf = calculate_noise_dists(x, tau_1f, Nsamp)
        
    #     # noise_pdf = get_dists([],threshold, tau_1f, Nsamp)[1]
            
    #     rice_cdf = np.ones(20001)
    #     for peak in peaks:
    #         rice_cdf *= scipy.stats.rice.cdf(x, b=abs(peak)/np.sqrt(tau_1f/2), loc=0, scale=np.sqrt(tau_1f/2))
        
    #     signal_cdf = rice_cdf * (1-np.exp(-(x**2)/tau_1f)) ** (Nsamp-peaks.size)

    #     signal_pdf = np.gradient(signal_cdf, x[1]-x[0])
        
        # fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        # ax.plot(x, signal_pdf, label="Signal PDF")
        # ax.fill_between(x, signal_pdf, alpha=0.3)
        # ax.plot(x, noise_pdf, label="Noise PDF")
        # ax.fill_between(x, noise_pdf, alpha=0.3)
        # ax.set_xlabel('Threshold')
        # ax.set_ylabel('Probability Density')
        # ax.legend()
        # plt.show()
        
        
        # tpr = 1 - signal_cdf  # true positive rate
        # fpr = 1 - noise_cdf  # false positive rate
        
    #     # # plot roc curve for each event file
        
    #     # fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        
    #     # ax.plot(fpr, tpr, label=f"Pitch Angle: {pitch_angles[i]} degrees, Starting Position: {starting_pos[i]} metres")
    #     # ax.set_xlabel('False Positive Rate')
    #     # ax.set_ylabel('True Positive Rate')
    #     # ax.legend()
    #     # ax.grid(True)
    #     # plt.show()
        
        # signal_pdfs.append(np.array(signal_pdf))
        # noise_pdfs.append(np.array(noise_pdf))
        
        # signal_cdfs.append(np.array(signal_cdf))
        # noise_cdfs.append(np.array(noise_pdf))
        
        # tpr_vals.append(np.array(tpr))
        # fpr_vals.append(np.array(fpr))
        

 

    # plot = True
    # if plot == True:
    #     # fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    #     detected_TPR_vals = []

    #     for i in range(len(file_list)):
            
    #         # fig, ax = plt.subplots(1, 1, figsize=(16, 8))
            
    #         tpr = tpr_vals[i]
    #         fpr = fpr_vals[i]
            
    #         # # plot roc curve for each event file
            
    #         # ax.plot(fpr, tpr, label=f"Pitch Angle: {pitch_angles[i]} degrees, Starting Position: {starting_pos[i]} metres")
    #         # ax.set_xlabel('False Positive Rate')
    #         # ax.set_ylabel('True Positive Rate')
    #         # ax.legend()
    #         # ax.grid(True)
    #         # plt.show()
            
    #         pitch_angle = pitch_angles[i]
    #         starting_position = starting_pos[i]
    #         f_name = file_list[i]
            
    #         defined_FPR = 0.01

    #         closest_value = np.argmin(np.abs(fpr - defined_FPR))

    #         detected_TPR_vals.append(tpr[closest_value])
            
    #         print(f"Pitch Angle: {pitch_angle}, Starting Position: {starting_position}, Detected TPR: {tpr[closest_value]}")

            
    # =============================================================================
    # Plotting
    # =============================================================================
    
    df = pd.read_parquet("../data/simulations_truth/FINAL_2Ddata_Bathtub_5.0K.pq")
    
    true_paths_to_data = df['Path_to_data'].values
    file_list = df['File_name'].values
    starting_pos = df['Starting position [metres]'].values
    pitch_angles = df['Pitch angle [degrees]'].values
    tpr_vals = df['TPR'].values
    fpr_vals = df['FPR'].values
    signal_pdfs = df['Signal PDF'].values
    noise_pdfs = df['Noise PDF'].values
    signal_cdfs = df['Signal CDF'].values
    noise_cdfs = df['Noise CDF'].values
    detected_TPR_vals = df['Detected TPR'].values
    defined_FPR = df['Defined FPR'].values
    
    # detected_TPR_vals = []
    
    # for i in range(len(file_list)):
        
    #     if i % 10 == 0:
        
    #         print(f"Processing file no.{i+1}")
        
    #     # defined_FPR = 0.01
    #     closest_value = np.argmin(np.abs(FPR_vals[i] - defined_FPR))
        
    #     detected_TPR_vals.append(TPR_vals[i][closest_value])
    
    defined_FPR_val = defined_FPR[0]
    
    # plt.tricontourf(pitch_angles[:len(detected_TPR_vals)], starting_pos[:len(detected_TPR_vals)], detected_TPR_vals, levels=100, cmap="viridis")
    # plt.figure(figsize=(16, 8))
    plt.scatter(pitch_angles[:len(detected_TPR_vals)], starting_pos[:len(detected_TPR_vals)], c=detected_TPR_vals, cmap="viridis")  
    plt.colorbar(label="TPR at defined FPR")
    plt.xlabel("Pitch Angle [degrees]")
    plt.ylabel("Starting Position [metres]")
    plt.title(f"TPR at FPR = {defined_FPR_val}")
    plt.show()
                    
    # full_data_frame = pd.DataFrame({'File_name': file_list, 'Path_to_data': true_paths_to_data, 
    #                                 'Starting position [metres]': starting_pos,
    #                                 'Pitch angle [degrees]': pitch_angles, 'Signal PDF': signal_pdfs, 'Noise PDF': noise_pdfs,
    #                                 'Signal CDF': signal_cdfs, 'Noise CDF': noise_cdfs, 'TPR': tpr_vals, 'FPR': fpr_vals})
    
    # full_data_frame["Path_to_data"] = full_data_frame["Path_to_data"].astype(str)
    
    # print data frame data types
    
    # print(full_data_frame.dtypes)
    
    if args.save:
        print("Saving Plot")
        
        plt.savefig('../figures/generated/2D_FPRvsPitchvsStartPos.pdf')
        # plt.savefig(args.output)
        
        # full_data_frame.to_pickle(f"../data/simulations_truth/2Ddata_Bathtub_{args.temperature}K_v1.pkl")
        # full_data_frame.to_csv(f"../data/simulations_truth/2Ddata_Bathtub_{args.temperature}K_v1.csv")
        # full_data_frame.to_parquet(f"../data/simulations_truth/2Ddata_Bathtub_{args.temperature}K_v1.pq")
        print("Saved Data Frame")
        
    

