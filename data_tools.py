from __init__ import *

path = "../data/" # Path to save data

def get_signal(file, signal_string):
    
    if not file.endswith('.h5'):
        raise ValueError("File must be an h5 file")
    if not os.path.exists(file):
        raise FileNotFoundError("File does not exist")
    
    
    with h5py.File(file, 'r') as f:
        signal = f['Data'][signal_string][:]
        
    return signal




def get_attributes(file, verbose=False):
    """ Print the attributes of the signal in the h5 file

    Args:
        file (str): Path to the h5 file

    Returns:
        list: List of signal strings
        list: List of attributes
        list: List of attribute values
    """
    
    if not file.endswith('.h5'):
        raise ValueError("File must be an h5 file")
    
    if not os.path.exists(file):
        raise FileNotFoundError("File does not exist")
    
    with h5py.File(file, 'r') as f:
        signal_strings = list(f['Data'].keys()) # ['signal1', 'signal2']

        attrs_container = []

        for signal_string in signal_strings:
            
            attributes = list((f['Data'][signal_string].attrs.keys()))
            attribute_vals = list((f['Data'][signal_string].attrs.values()))

            attrs_container.append(attribute_vals)
            
            if verbose:
                print('Signal String: ', signal_string)
                for attribute in attributes:
                    print(attribute, ': ', f['Data'][signal_string].attrs[attribute])  
    
    return signal_strings, attributes, attrs_container

