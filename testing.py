
from __init__ import *



def KS_test(distributions):
    """ Perform the Two Sample Kolmogorov-Smirnov test on a list of distributions

    Args:
        distributions (_type_): _description_
    """
    if not isinstance(distributions, list):
        raise TypeError('Input must be a list of distributions')
    if len(distributions) < 2:
        raise ValueError('Input must contain at least two distributions')
    if not all(isinstance(distribution, np.ndarray) for distribution in distributions):
        raise TypeError('Distributions must be numpy arrays')


    results = {}

    print('KS Test Results:')

    for i in range(len(distributions)):
        for j in range(i + 1, len(distributions)):
            stat, p_value = ks_2samp(distributions[i], distributions[j])
            results[f'Comparison {i+1} vs {j+1}'] = {'KS Statistic': stat, 'p-value': p_value}

    # Display results
    for comparison, result in results.items():
        print(f"{comparison}: KS Statistic = {result['KS Statistic']:.8f}, p-value = {result['p-value']:.8f}");
        
        
        
def get_integral(distributions, z_values):
    
    if not isinstance(distributions, list):
        raise TypeError('Input must be a list of distributions')
    if len(distributions) < 2:
        raise ValueError('Input must contain at least two distributions')
    if not all(isinstance(distribution, np.ndarray) for distribution in distributions):
        raise TypeError('Distributions must be numpy arrays')
    if not isinstance(z_values, np.ndarray):
        raise TypeError('z_values must be a numpy array')
    
    for dist in distributions:
        integral = trapezoid(dist, z_values)
        print(f'Integral: {integral}')