import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)


    #fetch unique users
    new_user = df['user'].unique().tolist()
    new_user.remove('Group Notification')
    new_user.sort()
    new_user.insert(0, 'Overall')


    selected_user=st.sidebar.selectbox("Show Analysis wrt",new_user)

    if st.sidebar.button('Show Analysis'):

        num_msg,words,media_shared,links=helper.fetch_user(selected_user,df)
        st.title("Top Statistics")

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header('Total Message')
            st.title(num_msg)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(media_shared)

        with col4:
            st.header('Links Shared')
            st.title(links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        


        if selected_user=="Overall":
            st.title('Most Busy User')
            x,new_data=helper.most_busy_user(df)
            fig,ax=plt.subplots()


            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='Pink')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_data)


        # word count
        df_wc=helper.word_cloud(selected_user,df)
        st.title('Word Cloud')
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common word

        most_common=helper.most_common_words(selected_user,df)
        st.title('Most Common Words')

        fig, ax = plt.subplots()
        ax.barh(most_common[0],most_common[1], color='Orange')
        st.pyplot(fig)

        #emoji analysis

        emoji_df = helper.emoji_show(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
