import pandas as pd
import datetime
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr

def event_rank_count(user_list, event_list, time_matched_events, event_rank_num):
    #create dataframe titled with unique event IDs:
    anom_event_count_list = pd.DataFrame(0, columns=event_list, index=[0])

    for n in range(len(user_list)-1):
        this_user = user_list[n]
        user_raw = time_matched_events[time_matched_events.userId == this_user].reset_index(drop=True)
        if len(user_raw) > event_rank_num:
            count_event = user_raw.event[event_rank_num]
            anom_event_count_list[count_event][0] = anom_event_count_list[count_event][0] + 1
        else:
            continue
    return anom_event_count_list


def plot_event_rank(count_list, click_num, user_list):
    #now sorting the column by values in ascending order:
    event_count_list_ordered = count_list.sort_values(by=0, ascending=False, axis=1)
    event_count_list_ordered_prop = event_count_list_ordered/len(user_list)
    event_count_list_ordered_prop_top_ranked = event_count_list_ordered_prop[event_count_list_ordered_prop.columns[0:5]]
    
    ax = sns.barplot(data=event_count_list_ordered_prop_top_ranked)
    ax.set(xlabel='Event', ylabel='Prop. users', title="Click #"+str(click_num))
    return plt.show


def stream_to_prob(stream_data_df): 
    stream_data_df_reindexed = stream_data_df.reset_index(drop=True)
    unique_users = stream_data_df_reindexed.userId.unique()
    unique_events = stream_data_df_reindexed.event.unique()
    user_mat = np.zeros((len(unique_events), len(unique_events)))
    
    for n in range(len(stream_data_df_reindexed)-1):
        if n != len(stream_data_df_reindexed)-1:
            this_user = stream_data_df_reindexed.userId[n]
            this_event = stream_data_df_reindexed.event[n]
            this_event_index = np.where(unique_events == this_event)[0][0]
        
            next_user = stream_data_df_reindexed.userId[n+1]
            next_event = stream_data_df_reindexed.event[n+1]
            next_event_index = np.where(unique_events == next_event)[0][0]
        
            if n > 0:
                before_user = stream_data_df_reindexed.userId[n-1]
                before_event = stream_data_df_reindexed.event[n-1]
                before_event_index = np.where(unique_events == before_event)[0][0]
            else:
                before_user = stream_data_df_reindexed.userId[n]
                before_event = stream_data_df_reindexed.event[n]
                before_event_index = np.where(unique_events == before_event)[0][0]                
            
            if this_user == next_user:
                user_mat[this_event_index, next_event_index] = user_mat[this_event_index, next_event_index] + 1
            elif this_user != next_user and this_user != before_user:
                user_mat[this_event_index, this_event_index] = user_mat[this_event_index, this_event_index] + 1
            
    #sum rows
    row_sum = user_mat.sum(axis=0).tolist()

    #sum columns
    col_sum = user_mat.sum(axis=1).tolist()

    user_mat_div = user_mat / row_sum
    
    return user_mat_div


def plot_stream_prob(stream_prob_mat, raw_events, *img_name):
    
    event_list = list(raw_events)
    fig = plt.figure()
    fig = plt.tight_layout()
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    color = clr.LinearSegmentedColormap.from_list('custom blue', ['whitesmoke','royalblue'], N=256)
    ax.matshow(stream_prob_mat, cmap=color)
    fig.colorbar(ax.matshow(stream_prob_mat, cmap=color))
    ax.set_yticks(range(len(event_list)+1))
    ax.set_yticklabels(event_list+[''], fontsize=15)
    ax.set_xticks(range(len(event_list)+1))
    plt.xticks(rotation=90, ha='right')
    ax.set_xticklabels(['']+event_list, fontsize=15) 
    if type(img_name)== str:
        fig.savefig(str(img_name) + '.pdf', bbox_inches = "tight")
        
    return plt.show()

def plot_stream_diff_prob(stream_prob_mat, event_list, *img_name):
    
    mid_norm = clr.TwoSlopeNorm(vcenter=0.)
    
    fig = plt.figure()
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    color = 'bwr_r'
    ax.matshow(stream_prob_mat, cmap=color)
    fig.colorbar(ax.matshow(stream_prob_mat, cmap=color, norm=mid_norm))
    ax.set_yticks(range(len(event_list)+1))
    ax.set_yticklabels(event_list+[''], fontsize=15)
    ax.set_xticks(range(len(event_list)+1))
    plt.xticks(rotation=90, ha='right')
    ax.set_xticklabels(['']+event_list, fontsize=15) 
    if type(img_name)== str:
        fig.savefig(img_name + '.pdf', bbox_inches = "tight")
