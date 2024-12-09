from __init__ import *



def get_signal_peaks(signal, cut):
    """_summary_

    Args:
        signal (times ): Time series of voltage data, the signal
        cut (_type_): Value upon which to cut FFT spectrum peaks

    Returns:
        _type_: _description_
    """
    
    signal_FFT = np.fft.fft(signal, norm='forward')
    
    abs_signal_FFT = np.abs(signal_FFT)
    
    peaks, _ = abs_signal_FFT[abs_signal_FFT > cut], np.where(abs_signal_FFT > cut)
    
    return peaks #, np.where(abs_signal_FFT > cut)


def get_dists(peaks, y, tau_1f, Nsamp):
    """_summary_

    Args:
        peaks (_type_): _description_

    Returns:
        _type_: _description_
    """

    if peaks == []:
        
        cdf = (1-np.exp(-(y**2)/tau_1f)) ** (Nsamp)
        pdf = np.gradient(cdf, y[1]-y[0])
        
        return cdf, pdf

    rice_cdf = np.ones(20001)
    for peak in peaks:
        rice_cdf *= scipy.stats.rice.cdf(y, b=abs(peak)/np.sqrt(tau_1f/2), loc=0, scale=np.sqrt(tau_1f/2))
        
    signal_cdf = rice_cdf * (1-np.exp(-(y**2)/tau_1f)) ** (Nsamp-peaks.size)

    signal_pdf = np.gradient(signal_cdf, y[1]-y[0])
    
    return signal_cdf, signal_pdf