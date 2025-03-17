# PowerCutStats

## Overview
PowerCutStats is a repository for statistical analysis of event FFT power and noise characterization. The codebase includes tools for data validation, matched filtering, and ROC curve generation.

## Features
- FFT analysis for event power spectra
- Noise characterization and statistical analysis
- ROC curve generation
- Data validation utilities

## Installation
To use this repository, clone it and install the required dependencies:
```bash
git clone https://github.com/nathanhigginbotham/PowerCutStats.git
cd PowerCutStats
pip install -r requirements.txt
```

## Structure
```bash
PowerCutStats/
│-- data/          # Data sets and truth information (CSV and PKL format)
│-- docs/          # Documentation
│-- examples/      # Example scripts and templates for analysis
│-- figures/       # Stored figures and results
│-- scripts/       # Various scripts for data processing, validation and analysis
│-- FROG.py        # FFT PDF/ROC Curve Generator
│-- analysis.py    # Functions for FFT noise analysis
│-- data_tools.py  # Data processing functions
│-- testing.py     # Validation and testing scripts
│-- README.md      # Project documentation
│-- LICENSE        # MIT License
```
## Contributing
If you'd like to contribute, feel free to submit a pull request. Ensure that any new scripts or modifications include proper documentation and testing.

## Acknowledgments
Part of the QTNM collaboration for statistical analysis of FFT/spectrogram data.
