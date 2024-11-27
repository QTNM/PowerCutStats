import numpy as np 
import matplotlib.pyplot as plt 
import scipy 
import h5py # Import h5py for saving data
import awkward as ak

from scipy.special import i0
from scipy.integrate import quad, trapezoid
from scipy import integrate
from scipy.stats import rice, rayleigh
from scipy.stats import ks_2samp

import glob
import os
import sys

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


def rice_CDF(z, tau, x_k):
    """
    Compute the Rice CDF for given parameters |z|, tau, and |x_k|.

    Parameters:
    z    : float, the value at which to evaluate the CDF
    tau  : float, scale parameter of the distribution
    x_k  : float, amplitude of the k-th component of the signal frequency spectrum

    Returns:
    cdf  : float, the value of the Rice CDF at |z|
    """
    
    return scipy.stats.rice.cdf(z, b=x_k, loc=0, scale=np.sqrt(tau/2))


def manual_rice_CDF(z, tau, x_k):
    """
    Compute the Rice CDF for given parameters |z|, tau, and |x_k|.

    Parameters:
    z    : float, the value at which to evaluate the CDF
    tau  : float, scale parameter of the distribution
    x_k  : float, amplitude of the k-th component of the signal frequency spectrum

    Returns:
    cdf  : float, the value of the Rice CDF at |z|
    """
    def integrand(tilde_z):
        """
        Define the integrand function for the Rice CDF.
        """
        return (2 * tilde_z / tau) * np.exp(-(tilde_z**2 + x_k**2) / tau) * i0(2 * tilde_z * x_k / tau)
    
    # Perform the integration from |z| to infinity
    vals = integrand(z)
    
    # Compute the integral
    integral = scipy.integrate.quad(integrand, z, 1e-3)
    
    # Compute the Rice CDF
    cdf = 1 - integral
    return cdf

def rice_cdf_log_space(z, tau, x_k):
    """Compute the Rician CDF at z with parameters tau and x_k using log-space calculations."""
    
    def integrand_log_space(tilde_z, tau, x_k):
        # Handle the case where x_k is very small
        if x_k < 1e-8:
            # If x_k is too small, the Bessel function approaches 1, and we can approximate it
            log_bessel_term = 0
        else:
            # Otherwise calculate the Bessel function normally
            bessel_argument = (2 * tilde_z * x_k) / tau
            bessel_val = i0(bessel_argument)
            log_bessel_term = np.log(bessel_val) if bessel_val > 0 else -np.inf
        
        # Logarithmic terms to avoid underflow
        prefactor = 2 * tilde_z / tau
        log_term1 = np.log(prefactor) if prefactor > 0 else -np.inf
        
        exp_term = -(tilde_z**2 + x_k**2) / tau
        
        # Return the sum of terms in log space and exponentiate at the end
        return np.exp(log_term1 + exp_term + log_bessel_term)
    
    # Set a finite upper limit to prevent nan issues
    upper_limit = z + 10 * tau  # Adjust this based on tau, though tau is very small here
    
    # Perform the integration using adaptive quadrature
    integral_result, _ = quad(integrand_log_space, z, upper_limit, args=(tau, x_k), limit=100)
    
    # Return the CDF value
    return 1 - integral_result

def numerical_derivative_cdf(cdf_func, z_values, delta_z, *args):
    return np.array([(cdf_func(z + delta_z, *args) - cdf_func(z - delta_z, *args)) / (2 * delta_z) for z in z_values])


############################# Signal Functions #################################################

B = 500e6
k = 1.38e-23

def generate_noise(T=T, samples=1000, resistance=1, B=B, k=k):
    """Generates noise with a given temperature and resistance

    Args:
        T (float, optional): Temperature in Kelvin (K). Defaults to T.
        samples (int, optional): Number of samples to generate. Defaults to 1000.
        resistance (_type_, optional): Resistance in Ohms. Defaults to resistance.
        B (_type_, optional): Bandwidth. Defaults to B.
        k (_type_, optional): Boltzmann Constant. Defaults to k.

    Returns:
        noise_dist (arr): Noise distribution
    """
    
    P_noise = k * T * B   # Noise Power (W) 

    noise_dist = np.sqrt(resistance *0.5) * np.random.normal(0, np.sqrt(P_noise), samples) # Noise distribution

    # plt.hist(noise_dist, bins=100)
    # plt.show()

    return noise_dist # Returns the noise distribution

