from urlextract import URLExtract
import pandas as pd
from collections import Counter

extractor = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['messages']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

    # # total messages
    # num_messages = df.shape[0] # fetch number of messeges
    #
    # # total words
    # words = []
    # for message in df['messages'].dropna().astype(str):
    #     words.extend(message.split())
    #
    #
    # # media messages
    # num_media_messages = df[df['messages'] == '<Media omitted>'].shape[0]
    #
    # # links
    # links = []
    # for message in df['messages'].dropna().astype(str):  # Drop NaN before loop
    #     links.extend(extractor.find_urls(message))
    #
    # return num_messages, len(words), num_media_messages, len(links)



def most_busy_users(df):
    x=df['users'].value_counts().head()

    df = round((df['users'].value_counts() / df.shape[0])* 100, 2).reset_index().rename(columns={'users':'name', 'count':'percent'})
    return x,df


def monthly_timeline(selected_user,df):
    if selected_user !='Overall':
        df =df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap

