from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor=URLExtract()

def fetch_user(selected_user,df):
    if selected_user == 'Overall':
        # fetch number of message
        num_message=df.shape[0]
        # fetch media messages
        media_message=df[df['message']=="<Media omitted>\n"].shape[0]
        # fetch links
        links = []
        for link in df['message']:
            links.extend(extractor.find_urls(link))
        # fetch number of words
        words = []
        for f in df['message']:
            words.extend(f.split())
        return num_message,len(words),media_message,len(links)
    else:
        new_df = df[df['user'] == selected_user]
        media_message=new_df[new_df['message'] == "<Media omitted>\n"].shape[0]

        num_message=new_df.shape[0]

        # fetch links
        links = []
        for link in new_df['message']:
            links.extend(extractor.find_urls(link))

        words = []
        for f in new_df['message']:
            words.extend(f.split())
        return num_message, len(words),media_message,len(links)


def most_busy_user(df):
    x = df['user'].value_counts().head()
    new_data=((df['user'].value_counts() / df.shape[0]) * 100).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x,new_data


def word_cloud(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    temp_df = df[df['user'] != 'Group Notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp_df['message'] = temp_df['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp_df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    temp_df = df[df['user'] != 'Group Notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']

    words = []

    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common=pd.DataFrame(Counter(words).most_common(20))

    return most_common

def emoji_show(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    e = []
    for message in df['message']:
        e.extend([c for c in message if c in emoji.EMOJI_DATA])

    most_emoji=pd.DataFrame(Counter(e).most_common(20))
    return most_emoji


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
