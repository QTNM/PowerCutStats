# FFT PDF/ROC Curve Generator Documentation

## Overview
The **FFT ROC Curve Generator** is a Python script that processes FFT data, generates Probability Density Functions (PDFs), and optionally produces Receiver Operating Characteristic (ROC) curves for signal analysis. The script allows for configurable inputs such as system temperature, impedance, and FFT peak detection thresholds.

## Requirements
To run the script, ensure you have the following dependencies installed:
```bash
pip install numpy scipy matplotlib argparse
```

## Usage
The script can be run from the command line with the following arguments:
```bash
python FROG.py -i <input_fft_file> -T <temperature> [-o <output_path>] [-R <impedance>] [-c <cut_value>] [--roc] [--plotFFT] [--plotPDF] [--plotROC]
```

### Arguments

- `-i <input_fft_file>`: Path to the input FFT data file. (Examples in data/FFT/).
- `-T <temperature>`: System temperature in Kelvin.
- `-o <output_path>`: Path to the output directory. Default is the current directory.
- `-R <impedance>`: System impedance in Ohms. Default is 50 Ohms.
- `-c <cut_value>`: FFT peak detection threshold. Default is 0.5.
- `--roc`: Generate ROC curves.
- `--fpr`: False Positive Rate for ROC curve. Default is 0.01.
- `--plotFFT`: Plot the FFT data.
- `--plotPDF`: Plot the PDFs.
- `--plotROC`: Plot the ROC curves.
- `--save`: Save the plots and data to the output directory.

## Example Usage

Running FFT Analysis & Generating a PDF:
```bash
python FROG.py -i example_fft.txt -T 300 --plotPDF
```

Running Analaysis with ROC Curve Generation:
```bash
python FROG.py -i example_fft.csv -T 300 --roc --plotROC
```

## Processing Steps

1. Load FFT data from the input file.
2. Calculate the PDFs for the signal and noise (from system temperature).
3. Generate ROC curves (if requested).
4. Plot the FFT data, PDFs, and ROC curves (if requested).
5. Save the output data and plots to the output directory (if requested).

## Output
The script generates the following output files:
- `PDF.pdf`: PDF plot for the signal and noise
- `ROC.pdf`: ROC curve plot (if requested)
- `FFT.pdf`: FFT data plot (if requested)
- `noise_pdf.txt`: Noise PDF data
- `signal_pdf.txt`: Signal PDF data
- `roc_data.txt`: ROC curve data (if requested)

## Notes
- The script assumes the input FFT data is in a specific format (csv, txt, etc.). [I can add more functionality later]
- The script uses a simple peak detection algorithm to identify signal peaks in the FFT data, specified by the cut value. 
- The ROC curve generation is based on the False Positive Rate (FPR) and True Positive Rate (TPR) calculations.