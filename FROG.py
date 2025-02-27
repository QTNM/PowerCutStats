## FFT ROC CURVE GENERATOR

import sys
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

R = 500 # Value inputted by user 




def parse_inputs():
    parser = argparse.ArgumentParser(description="Analyze FFTs and generate PDFs/ROC curves.")

    # Required argument: input FFT file with 40960 samples (40.96 us)
    parser.add_argument("-i", "--input", required=True, help="Path to the input FFT file")
    
    
    # Required argument: System Temperature
    parser.add_argument("-T", "--temperature", required=True, help="Value of System Temperature in Kelvin")

    # Optional argument: output PDF file
    parser.add_argument("-o", "--output", default="figures/generated/output.pdf", help="Path to save the output PDF")
    
    # Optional argument: R value, default is 500
    parser.add_argument("-R", "--impedance", type=float, default=500, help="Value of Impedance R")

    # Optional argument: cut value for FFT peaks
    parser.add_argument("-c", "--cut", type=float, default=1e-8, help="Cut value for FFT peaks")

    # Optional flag: Generate ROC curve
    parser.add_argument("--roc", action="store_true", help="Include this flag to generate an ROC curve")

    # Optional flag: Plot FFT
    parser.add_argument("--plotFFT", action="store_true", help="Include this flag to plot the FFT")
    
    # Optional flag: Plot PDF
    parser.add_argument("--plotPDF", action="store_true", help="Include this flag to plot the PDF")

    # Parse arguments
    args = parser.parse_args()
    
    args.temperature = float(args.temperature)
    args.cut = float(args.cut)
    args.R_value = float(args.impedance)
    
    # Example usage of arguments
    print(f"Processing FFT file: {args.input}")
    print(f"Saving output to: {args.output}")
    
    if args.roc:
        print("Generating ROC curve...")

    # Add actual processing logic here
    # (e.g., loading FFT, analyzing data, generating plots)
    return args

if __name__ == "__main__":
    args = parse_inputs()
    
    cut = args.cut
  
    # Below should be replaced by user input
    # file_name = 'data/harmonic/86p5deg/out_0aa72c89-416e-4f11-8eda-ae7542078817.h5'
    # signal_strings, attributes, attrs_container = get_attributes(file_name)
    # signal = get_signal(file_name, 'signal1', full_path=True) # One polarisation
    # signal_FFT = np.fft.fft(signal, norm='forward')

    data_dir = 'data/FFT/'
    data_path = data_dir + args.input
    
    signal_FFT = np.loadtxt(data_path, dtype=complex)
    
    abs_signal_FFT = np.abs(signal_FFT)
    peaks, _ = abs_signal_FFT[abs_signal_FFT > cut], np.where(abs_signal_FFT > cut)
    
    # np.savetxt(data_path, abs_signal_FFT)
    
    if args.plotFFT:
        plt.plot(abs_signal_FFT)
        plt.show()
    
    n_pwr = kb * T * bw # noise power
    tau_1t = n_pwr * R # noise variance single channel, time-domain (tau_1t)
    tau_1f = tau_1t / Nsamp # noise variance single channel, freq-domain (tau_1f)
    
    threshold = np.linspace(1e-9, 9e-6, 20001)
    x = threshold
    
    noise_pdf = get_dists([],threshold, tau_1f, Nsamp)[1]
    
    rice_cdf = np.ones(20001)
    for peak in peaks:
        rice_cdf *= scipy.stats.rice.cdf(x, b=abs(peak)/np.sqrt(tau_1f/2), loc=0, scale=np.sqrt(tau_1f/2))
    
    signal_cdf = rice_cdf * (1-np.exp(-(x**2)/tau_1f)) ** (Nsamp-peaks.size)

    signal_pdf = np.gradient(signal_cdf, x[1]-x[0])
    
    if args.plotPDF:
        
        fig, ax1 = plt.subplots(1, 1, figsize=(16, 8))
        
        ax1.plot(threshold, noise_pdf, 'r--', label='Noise PDF')
        ax1.fill_between(threshold, noise_pdf, alpha=0.3, color='red')
        
        ax1.plot(threshold, signal_pdf, '--', label=f"{args.input} Signal PDF")
        ax1.fill_between(threshold, signal_pdf, alpha=0.3)

        ax1.set_xlabel('Threshold')
        ax1.set_ylabel('Probability Density')
        ax1.legend()
        ax1.set_xlim(0, 0.2e-6)
        ax1.grid(True)
        
        plt.tight_layout()
        plt.show()
    
    print(args)