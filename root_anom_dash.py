#importing library functions:
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import datetime
import streamlit as st
import glob
import re

#importing custom functions:
from root_data_clean import *
from root_data_match import *
from root_data_analysis import *
    
#open Streamlit dash by navigating to this file and then
#streamlit run root_anom_dash.py

st.title('Comparing anomalies in a company')

#########################
##### ANOMALY DATA ######
#########################

# getting the data from the directory (if the data (.csv) files stored in /anon_data) 
code_dir = os.getcwd()
data_dir = code_dir + '/anon_data/'

#parse the data file names:
org_dir_tog = []
org_num_tog = []
for name in glob.glob(os.path.join(data_dir, 'anonymized-anomalies-org*.csv')):
    org_dir_tog.append(name)
    org_num = re.findall("anonymized-anomalies-org(\d+).csv", name)
    org_num = int(org_num[0])
    org_num_tog.append(org_num)
    
#####>#>CHOOSE ORGANIZATION/COMPANY ID<#<#####
st.subheader("First, choose a company of interest.")
org_num = st.radio("Company ID:", (org_num_tog))

full_anomalies_df = pd.read_csv(data_dir+'anonymized-anomalies-org'+str(org_num)+'.csv') 
  
round_anom_times(full_anomalies_df)

# calculate overlap in anomaly period:
full_anomalies_overlap_df = anom_over(full_anomalies_df)


#####>#>CHOOSE SOURCE NUMBER<#<#####
full_anomalies_df_data_sources = list(full_anomalies_overlap_df.source_name.unique())

st.subheader("Next, choose a source of that company. These correspond to web, iOS, or Android.")
source_num = st.radio("Source ID:", (full_anomalies_df_data_sources))
anomalies_df = full_anomalies_overlap_df[full_anomalies_overlap_df.source_name==source_num].reset_index()

'Here are all the logged anomalies for that company and source:', anomalies_df


anom_counts = anomalies_df['anom_num'].value_counts().rename_axis('anom_num').reset_index(name='counts')

#getting isolated anomalies:
isol_anom_list = anom_counts[anom_counts.counts==1]

#getting chained anomalies:
chain_anom_list = anom_counts[anom_counts.counts>1]

#####>#>CHOOSE ANOMALY TYPE<#<#####
st.subheader("Now, choose an anomaly of interest: either a single, isolated one or an overlapping, chained one.")
anom_type = st.radio("Anomaly type:", ('isolated', 'chained'))

if anom_type=='isolated':
    anom_df = anomalies_df[anomalies_df.anom_num.isin(isol_anom_list.anom_num)].reset_index(drop=True)
elif anom_type=='chained':
    anom_df = anomalies_df[anomalies_df.anom_num.isin(chain_anom_list.anom_num)].reset_index(drop=True)

'Here are all of the', str(anom_type), 'anomaly data:', anom_df


#####>#>CHOOSE ANOMALY NUMBER<#<#####
st.subheader("Next, choose an anomaly based on its ID, i.e. anom_num.")
anom_id = st.radio("Anomaly ID:", (anom_df.anom_num.unique()))


#########################
######## RAW DATA #######
#########################

raw_df = pd.read_csv('./anon_data/anonymized-events-org'+str(org_num)+'.csv')  
raw_event_df = round_raw_times(raw_df)

# total number of users:
raw_unique_user_id = raw_event_df.userId.unique()
raw_unique_user_total = len(raw_unique_user_id)

# total number of events:
raw_uniqe_event_id = raw_event_df.event.unique()
raw_uniqe_event_total = len(raw_uniqe_event_id)

##################################################
########## MATCHING ANOMALY AND RAW DATA #########
##################################################
# relating that web anomaly (by index of anomaly from anom_web_df) to the raw events recorded from web
matched_anom_raw_events = match_anom_to_raw(anom_id, anom_df, raw_event_df)

'For Anomaly ID', str(anom_id), ', here are the raw user events that occured during that time period:', matched_anom_raw_events


# choosing an non-anomaly to relate to raw data
# relating that web anomaly (by index of anomaly from anom_web_df) to the raw events recorded from web
matched_nonanom_raw_events = match_nonanom_to_raw(anom_id, anom_df, raw_event_df)

'Here are the time-matched raw user events that occured a week prior to Anomaly ID', str(anom_id), matched_nonanom_raw_events

if matched_nonanom_raw_events.empty:
    st.text('There is not enough prior data to time-match this particular event.')
    sys.exit("Error! Try another anomaly.")
    

##################################################
################# PLOTTING EVENTS ################
##################################################
st.subheader("Next, examine which events users clicked on first, second, or third when browsing during the anomaly period.")
event_num = st.radio("Choose event click of interest:", list(range(1,4)))

event_num_count_prop = event_rank_count(raw_unique_user_id, raw_uniqe_event_id, matched_anom_raw_events, event_num)

st.header('Distribution of events participants clicked')
plot_event_rank(event_num_count_prop, event_num, raw_unique_user_id)
st.pyplot()

##################################################
############## GETTING PROBABILITY ###############
##################################################
anom_mat_div = stream_to_prob(matched_anom_raw_events)
anom_data_names = matched_anom_raw_events.event.unique()
#np.sum(anom_mat_div[:, 16]) #checking if columns = 1

nonanom_mat_div = stream_to_prob(matched_nonanom_raw_events)
nonanom_data_names = matched_nonanom_raw_events.event.unique()
#np.sum(anom_mat_div[:, 16]) #checking if columns = 1

##################################################
############## PLOTTING PROBABILITY ##############
##################################################

### Matching plots of anomaly and non-anomaly probabilities
# convert the matrix to a dataframe with names on the x and y axis 
anom_mat_div_df = pd.DataFrame(anom_mat_div)
anom_mat_div_df.columns = anom_data_names
anom_mat_div_df.index = anom_data_names

# convert the matrix to a dataframe with names on the x and y axis 
nonanom_mat_div_df = pd.DataFrame(nonanom_mat_div)
nonanom_mat_div_df.columns = nonanom_data_names
nonanom_mat_div_df.index = nonanom_data_names

# anom diff.
anom_diff_name = set(anom_data_names).difference(set(nonanom_data_names))

anom_mat_div_df_drop = anom_mat_div_df.drop(anom_diff_name, axis = 0)
anom_mat_div_df_drop = anom_mat_div_df_drop.drop(anom_diff_name, axis = 1)

anom_mat_div_df_drop_col = anom_mat_div_df_drop.columns

#reorder the columns to match:
anom_mat_div_df_drop_reorder = anom_mat_div_df_drop.reindex(columns=anom_mat_div_df_drop_col)
anom_mat_div_df_drop_reorder = anom_mat_div_df_drop_reorder.reindex(anom_mat_div_df_drop_col)

# nonanom diff.
nonanom_diff_name = set(nonanom_data_names).difference(set(anom_data_names))

nonanom_mat_div_df_drop = nonanom_mat_div_df.drop(nonanom_diff_name, axis = 0)
nonanom_mat_div_df_drop = nonanom_mat_div_df_drop.drop(nonanom_diff_name, axis = 1)

nonanom_mat_div_df_drop_col = nonanom_mat_div_df_drop.columns

#reorder the columns to match:
nonanom_mat_div_df_drop_reorder = nonanom_mat_div_df_drop.reindex(columns=anom_mat_div_df_drop_col)
nonanom_mat_div_df_drop_reorder = nonanom_mat_div_df_drop_reorder.reindex(anom_mat_div_df_drop_col)

st.header('Probability of participants'' click traversals during the anomalous event.')
plot_stream_prob(anom_mat_div_df_drop_reorder.to_numpy(), anom_mat_div_df_drop_reorder.columns.values, 'anom_mat', 1)
st.pyplot()

st.header('Probability of participants'' click traversals during the non-anomalous event.')
plot_stream_prob(nonanom_mat_div_df_drop_reorder.to_numpy(), nonanom_mat_div_df_drop_reorder.columns.values, 'nonanom_mat', 2)
st.pyplot()


##################################################
########### PLOTTING DIFF. PROBABILITY ###########
##################################################

diff_df =  anom_mat_div_df_drop_reorder - nonanom_mat_div_df_drop_reorder

st.header('Difference in probability of participants'' click traversals (anomalous - non-anomalous).')
plot_stream_diff_prob(diff_df.to_numpy(), list(diff_df.columns.values), 'diff_mat', 1)
st.pyplot()

##################################################
########## PLOTTING BIGGEST EVENT DIFF. ##########
##################################################
#find the biggest/smallest values in all the columns
diff_df_max = diff_df.max(axis=1)
diff_df_min = diff_df.min(axis=1)

#then get the 3 biggest/smallest 3 columns
diff_df_max_sort_df = pd.DataFrame(diff_df_max.nlargest(5))
diff_df_max_sort_df = diff_df_max_sort_df.reset_index()
diff_df_max_sort_df.columns = ['event', 'prob']

#then get the 3 biggest/smallest 3 columns
diff_df_min_sort_df = pd.DataFrame(diff_df_min.nsmallest(5))
diff_df_min_sort_df = diff_df_min_sort_df.reset_index()
diff_df_min_sort_df.columns = ['event', 'prob']
diff_df_min_sort_df = diff_df_min_sort_df.sort_values('prob')

st.header('Difference in events.')
f, axes = plt.subplots(1, 2)
max_pal = sns.color_palette(sns.light_palette("blue", reverse=False),len(diff_df_max_sort_df))
min_pal = sns.color_palette(sns.light_palette("red", reverse=True),len(diff_df_min_sort_df))
ax = sns.barplot(x="event", y="prob", data = diff_df_max_sort_df, palette=np.array(max_pal[::1]), order=diff_df_max_sort_df.sort_values('prob').event, ax=axes[0]).set_title("Max Vals")
ax = sns.barplot(x="event", y="prob", data = diff_df_min_sort_df, palette=np.array(min_pal[::1]), order=diff_df_min_sort_df.sort_values('prob').event, ax=axes[1]).set_title("Min Vals")
f = plt.tight_layout()
st.pyplot()
