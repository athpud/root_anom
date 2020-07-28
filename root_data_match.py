import pandas as pd
import numpy as np
import datetime

# choosing an anomaly to relate to raw data
def match_anom_to_raw(num_anom, df_anom, df_raw):
    relevant_anom = df_anom[df_anom.anom_num == num_anom]
    relevant_anom = relevant_anom.reset_index(drop=True)
    
    anom_start_adj = relevant_anom['start_anomaly_rounded'][0] - datetime.timedelta(hours=1)
    anom_end_adj = relevant_anom['end_anomaly_rounded'][len(relevant_anom)-1] + datetime.timedelta(hours=1)
    
    anom_match_raw_df = df_raw[(df_raw['timestamp_rounded'] > anom_start_adj) & (df_raw['timestamp_rounded'] < anom_end_adj)]
    return anom_match_raw_df


# choosing an non-anomaly to relate to raw data
def match_nonanom_to_raw(num_anom, df_anom, df_raw):
    relevant_anom = df_anom[df_anom.anom_num == num_anom]
    relevant_anom = relevant_anom.reset_index(drop=True)
    nonanom_start_adj = relevant_anom['start_anomaly_rounded'][0] - datetime.timedelta(days=7) - datetime.timedelta(hours=1)
    nonanom_end_adj = relevant_anom['end_anomaly_rounded'][len(relevant_anom)-1] - datetime.timedelta(days=7) + datetime.timedelta(hours=1)
    
    anom_match_raw_df = df_raw[(df_raw['timestamp_rounded'] > nonanom_start_adj) & (df_raw['timestamp_rounded'] < nonanom_end_adj)]
    return anom_match_raw_df