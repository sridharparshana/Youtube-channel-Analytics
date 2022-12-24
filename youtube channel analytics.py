

#Importing Libraries
import pandas as pd
import requests
import json

api_key='AIzaSyCDg3BbA_qzDz-nu2KucUkrNT_KlisgbX'  # Replace this key with your API key

channel_id='UCSjPe5kinQtwcyHcFJyyMfw'  # Replace it with your required channel ID

# For channel's basic statistics

url1 = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&key={api_key}&id={channel_id}"
channel_info = requests.get(url1)
json_data1 = json.loads(channel_info.text)



channel_subscribers = int(json_data1['items'][0]['statistics']['subscriberCount']);
channel_videos = int(json_data1['items'][0]['statistics']['videoCount']);



limit = 15 # how many pages of information you want
video_Ids = []
nextPageToken ="" # used here to get page with unrepeated content, for 0th iteration let it be null
for i in range(limit):
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&channelId={channel_id}&maxResults=50&pageToken={nextPageToken}";
    data = json.loads(requests.get(url).text)
    data.get('items')
    for item in data['items']:
        video_Id = item['id']
        video_Ids.append(video_Id)  # Storing video Ids for extracting videos information
    nextPageToken = data.get('nextPageToken') # to collect videos from the next page

data_df = pd.DataFrame(columns=['video_id','channel_id','published_date',
                             'video_title','video_description',
                             'likes','dislikes','views','comment_count'])


#Let's put gathered data videos in their respective categories columns


for i,video_Id in enumerate(video_Ids):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&key={api_key}&id={video_Id}"
    data = json.loads(requests.get(url).text)
    channel_id = data['items'][0]['snippet']['channelId']      
    published_date = data['items'][0]['snippet']['publishedAt']    
    video_title =  data['items'][0]['snippet']['title']     
    video_description = data['items'][0]['snippet']['description']
    likes =  data["items"][0]["statistics"]["likeCount"]
    dislikes = data["items"][0]["statistics"]["dislikeCount"]
    views = data["items"][0]["statistics"]["viewCount"]
    comment_count = data["items"][0]["statistics"]['commentCount']
    row = [video_Id,channel_id,published_date,
           video_title,video_description,
           likes,dislikes,views,comment_count]
    data_df.loc[i]=row;
    
# Let's store the information as a csv file

    data_df.to_csv('channel.csv',index=False)