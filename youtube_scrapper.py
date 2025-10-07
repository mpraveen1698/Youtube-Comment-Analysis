import os

import googleapiclient.discovery
import pandas as pd


def get_statistics_views(youtube, video_id, token=""):
    response = youtube.videos().list(
        part='statistics, snippet',
        id=video_id).execute()

    view_count = response['items'][0]['statistics']['viewCount']
    like_count = response['items'][0]['statistics']['likeCount']
    #dislike_count = response['items'][0]['statistics']['dislikeCount']
    dislike_count=0
    return view_count, like_count, dislike_count


def get_comment_threads(youtube, video_id, comments=[], token="", max_results=100):
    request = youtube.commentThreads().list(
        part="snippet,replies",
        maxResults=max_results,
        videoId=video_id
        )
    response = request.execute()
    return response


def get_comments(service, **kwargs):
    comments = []
    like_count = []
    reply_count = []
    author_name = []
    author_url_profile = []
    results = service.commentThreads().list(**kwargs).execute()

    while results:        
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment)
            like =item['snippet']['topLevelComment']['snippet']['likeCount']
            like_count.append(like)
            reply = item['snippet']['totalReplyCount']
            reply_count.append(reply)
            a_name =  item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            author_name.append(a_name)
            a_ch_url = item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            author_url_profile.append(a_ch_url)
 
        if ('nextPageToken' in results) and (len(comments)<400):
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    df = pd.DataFrame()
    df['comments'] = comments
    print(len(comments))
    df['like_count'] = like_count
    df['reply_count'] = reply_count
    df['author_name'] = author_name
    df['author_url_profile'] = author_url_profile
    return df


def main(video_id):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAaEMuw_JogB-rarI2WvODzKYqwcRZC9vs"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    views, likes, dislikes = get_statistics_views(youtube, video_id)
    
    comments_df = get_comments(
        youtube, part="snippet, replies", maxResults=500, videoId=video_id)  # , order="relevance"
    return views, likes, dislikes, comments_df


if __name__ == "__main__":
    main("CYnFhpNSbdk")
