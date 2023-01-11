def filter_results(arr, pid: int, start: int=0):
    """
    Function that filters the data from one process from an array of power measurements
    
    @arr: array containing power measurements 
    @pid: pid of the process that needs to be filtered out
    """
    return [
        (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
            for measurement in arr 
                for consumer in measurement['consumers'] 
                    if consumer['pid'] == pid]
                    
def filter_results_string(arr, exe: str, start: int=0):
    """
    Function that filters the data from one process from an array of power measurements
    
    @arr: array containing power measurements 
    @pid: pid of the process that needs to be filtered out
    """
    return [
        (round(consumer['timestamp']-start, 3), consumer['consumption']/1000000) 
            for measurement in arr 
                for consumer in measurement['consumers'] 
                    if consumer['exe'] == str]

def wh_to_w(arr):
    """
    Converts an array containg watt hours measurements to watts
    
    @arr array containing measurements
    """
    return [(measurement[0], measurement[1]/measurement[0]) if i == 0 else (measurement[0], measurement[1]/(measurement[0]-arr[i-1][0])) for i, measurement in enumerate(arr) ]

def aggregate_results(arr, step):
    """
    Aggregates the results
    
    arr : 2d array containing timestamps and given wattages: [[t0, t1, ..., tn][w0, w1, ..., wn]]
    step: step of returning array
    
    returns array in the form of [[0, 1*step, ..., m*step][w0^, w1^, ...,, wm^]] 
        where m*step < tn
    """
    import numpy as np
    last_time, last_pwr, i = arr[0][0], arr[0][1], 0 
    pwr1 = (  (step*last_pwr) / last_time  )
    
    x_y_aggr = [(0,0)]
    
    for t in np.arange(0, arr[0][-1], step):
        if t > arr[i][0]:
            new_time, new_pwr = arr[i+1][0] - arr[i][0], arr[i+1][1]
            pwr2 = (  (step*new_pwr) / (new_time)  )
    
            frac = ( t - arr[i][0] ) / step
            x_y_aggr.append(  (t, frac * new_pwr + (1-frac) * last_pwr)   )
    
            i+=1
            last_time, last_pwr, pwr1 = new_time, new_pwr, pwr2
        else:
            x_y_aggr.append(  (t, pwr1)  )
    
    return np.array(list(zip(*x_y_aggr)))