import numpy as np 
import matplotlib.pyplot as plt 
import scipy 
import h5py # Import h5py for saving data

from scipy.special import i0
from scipy.integrate import quad, trapezoid
from scipy import integrate
from scipy.stats import rice, rayleigh
from scipy.stats import ks_2samp


import glob

path = "../data/" # Path to save data

k = 1.38e-23 # Boltzmann constant
B = 500e6 # Bandwidth
T = 5 # Temperature

############################# Rayleigh Functions #################################################

def rayleigh_CDF(z, tau, N_bin=1):
    """ Generate the CDF of the Rayleigh distribution for the given parameters and number of bins

    Args:
        z (array): Array of magnitude values
        tau (float): 2 X Sigma squared (kBTR / NFFT)
        N_bin (int): Number of bins

    Returns:
        Array: Array of the CDF values
    """
    # return (1 - np.exp(-z**2 / tau))**N_bin
    return rayleigh.cdf(z, scale=np.sqrt(tau/2))**N_bin


# Numerical derivative of the Rayleigh CDF
def numerical_derivative_rayleigh_CDF(z, tau, N_bin, delta=1e-5):
    """ Numerical derivative of the Rayleigh CDF

    Args:
        z (array): Array of magnitude values
        tau (float): 2 X Sigma squared (kBTR / NFFT)
        N_bin (int): Number of bins
        delta (float): Step size for numerical differentiation

    Returns:
        Array: Array of the numerical derivative values
    """
    return (rayleigh_CDF(z + delta, tau, N_bin) - rayleigh_CDF(z - delta, tau, N_bin)) / (2 * delta)


# Define the derived PDF function
def H0_PDF(z, tau, N_bin, scipy=True):
    """ Generate the derived PDF function

    Args:
        z (array): Array of magnitude values
        tau (float): 2 X Sigma squared (kBTR / NFFT)
        N_bin (int): Number of bins
        scipy (bool, optional): Use scipy or numpy functions. Defaults to True.

    Returns:
        _type_: _description_
    """
    
    if scipy == True:
        return (2 * N_bin * z / tau) * rayleigh.cdf(z, scale=np.sqrt(tau/2))**(N_bin - 1) * np.exp(-z**2 / tau)

    if scipy == False:
        return (2 * N_bin * z / tau) * (1 - np.exp(-z**2 / tau))**(N_bin - 1) * np.exp(-z**2 / tau)
    
    else: 
        print("Error: Please specify whether to use the scipy or numpy function")
        return None


############################# Rice Functions #################################################