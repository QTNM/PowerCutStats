from __init__ import *

dir_path = "../data/" # Path to save data

frame_strings = [           'File_name',
                               'signal',
                                 'trap',   
                        'B_bkg [Tesla]',
          'Cyclotron frequency [Hertz]',
'Downmixed cyclotron frequency [Hertz]',
                          'Energy [eV]',
                 'LO frequency [Hertz]',
                'Pitch angle [degrees]',
           'Starting position [metres]',
    'Starting velocity [metres/second]',
                  'Time step [seconds]',
           'Waveguide impedance [Ohms]',
                        'i_coil [Amps]',
                      'r_coil [metres]',
                        'r_wg [metres]'
]


def set_data_path(file):
    
    return dir_path + file


def get_signal(file, signal_string, full_path=False, override_path=False):
    
    if full_path:
        data_path = file
        
    else:
        data_path = set_data_path(file)

    if override_path:
        data_path = override_path + file
    
    if not data_path.endswith('.h5'):
        raise ValueError("File must be an h5 file")
    if not os.path.exists(data_path):
        raise FileNotFoundError("File does not exist")
    
    
    with h5py.File(data_path, 'r') as f:
        signal = f['Data'][signal_string][:]
        
    return signal




def get_attributes(file, verbose=False, full_path=False):
    """ Print the attributes of the signal in the h5 file

    Args:
        file (str): Path to the h5 file

    Returns:
        list: List of signal strings
        list: List of attributes
        list: List of attribute values
    """
    
    data_path = set_data_path(file)
    
    
    # Error handling
    if not data_path.endswith('.h5'):
        raise ValueError("File must be an h5 file")

    if not os.path.exists(data_path):
        raise FileNotFoundError("File does not exist")
    ##################################################
    
    
    with h5py.File(data_path, 'r') as f:
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

def get_truth_data(f_list, verbose=False, full_path=True, savefile=False):
    """ Get the truth data from the h5 file and save it to a csv file

    Args:
        f_list (.h5): Paths to h5 files
        verbose (bool, optional):  Defaults to False.
        full_path (bool, optional): Path to file. Defaults to True.
        savefile (bool, optional): Option to Save .csv . Defaults to False.
    """
    
    # Error handling
    if not isinstance(f_list, list):
        raise ValueError("f_list must be a list of file paths")
    if not all([f.endswith('.h5') for f in f_list]):
        raise ValueError("All files must be h5 files")
    if not all([os.path.exists(f) for f in f_list]):
        raise FileNotFoundError("All files must exist")
    if not isinstance(verbose, bool):
        raise ValueError("Verbose must be a boolean")
    if not isinstance(full_path, bool):
        raise ValueError("full_path must be a boolean")
    ##################################################
    
    df = pd.DataFrame()
    
    for i, f in enumerate(f_list):
    
        
        signal_strings, b, data = get_attributes(f, full_path=True)
        filename = f.split('/')[-1]
        trap_type = f.split('/')[-3]
        vars = {
            'File_name': filename,
            'signal': signal_strings[0], # signal1 only as default [0], signal2 is not used ([1])
            'trap': trap_type,
            'B_bkg': data[0][0], # Changing to data[1][0] will give the background field for signal2, repeat this for below if required
            'f_cyc': data[0][1],
            'f_cyc_d': data[0][2],
            'energy': data[0][3],
            'f_lo': data[0][4],
            'pitch_angle': data[0][5],
            'r_0': [data[0][6]],
            'v_0': [data[0][7]],
            'dt': data[0][8],
            'Z_wg': data[0][9],
            'i_coil': data[0][10],
            'r_coil': data[0][11],
            'r_wg': data[0][12]
        }
        
        new_frame = pd.DataFrame(vars)
        
        if i == 0:
            df = pd.DataFrame(vars)
        
        else:
            df = pd.concat([df, new_frame], axis=0)

    
        if verbose and i % 100 == 0:
            print(str(i) + ' files processed')

    df.columns = frame_strings

    if savefile!=False:
        
        df.to_csv(savefile, index=False)
        
    return df

    