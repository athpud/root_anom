import pandas as pd
import numpy as np
import datetime
    
def round_anom_times(anom_df):
    anom_df['start_anomaly'] =  pd.to_datetime(anom_df['start_anomaly'])
    anom_df['end_anomaly'] =  pd.to_datetime(anom_df['end_anomaly'])
    anom_df['start_anomaly_rounded'] = anom_df['start_anomaly'].dt.floor('h') 
    anom_df['end_anomaly_rounded'] = anom_df['end_anomaly'].dt.ceil('h') 
    

def round_raw_times(raw_df):
    raw_df.timestamp =  pd.to_datetime(raw_df['timestamp'])
    raw_df['timestamp_rounded'] = raw_df['timestamp'].dt.floor('h') 
    raw_event_df = raw_df[raw_df['userId'].notna()]
    return raw_event_df


def anom_over(anom_df):
    # calculate overlap in anomaly period:
    anom_df = anom_df.reset_index(drop=True)
    anom_over_list = [0]
    for a in range(len(anom_df)):
        if a > 0:
            curr_start = anom_df['start_anomaly_rounded'][a]
            curr_end = anom_df['end_anomaly_rounded'][a]
            prev_start = anom_df['start_anomaly_rounded'][a-1]
            prev_end = anom_df['end_anomaly_rounded'][a-1]
            
            late_start = max(curr_start, prev_start)
            earl_end = min(curr_end, prev_end)
            change = ((earl_end - late_start).total_seconds()/60)/60
            time_over = max(0, change)
            anom_over_list.append(time_over)    
            
    anom_df.insert(len(anom_df.columns), "time_overlap", anom_over_list)

    anom_num_list = []
    anom_num = 0
    for o in range(len(anom_df)):
        if o < len(anom_df)-1:
            this_overlap = anom_df.time_overlap[o]
            next_overlap = anom_df.time_overlap[o+1]
        
            if this_overlap == 0 and next_overlap == 0:
                anom_num = anom_num + 1
            elif this_overlap == 0 and next_overlap > 0:
                anom_num = anom_num + 1
            elif this_overlap > 0 and next_overlap > 0:
                anom_num = anom_num
        anom_num_list.append(anom_num)
    anom_df.insert(len(anom_df.columns), "anom_num", anom_num_list)
    
    return anom_df
