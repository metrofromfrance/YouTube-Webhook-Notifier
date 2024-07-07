import requests
import os
from googleapiclient.discovery import build

# YouTube Data API setup
api_key = 'YOUR_YOUTUBE_API_KEY'
channel_id = 'YOUR_CHANNEL_ID'
webhook_url = 'YOUR_WEBHOOK_URL'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_name(channel_id):
    # Get the channel name
    response = youtube.channels().list(part='snippet', id=channel_id).execute()
    channel_name = response['items'][0]['snippet']['title']
    return channel_name

def get_latest_video(channel_id):
    # Get the uploads playlist ID
    response = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the latest video from the uploads playlist
    response = youtube.playlistItems().list(part='snippet', playlistId=uploads_playlist_id, maxResults=1).execute()
    latest_video = response['items'][0]['snippet']

    return latest_video

def post_to_webhook(channel_name, video):
    data = {
        "content": f"{channel_name} UPLOADED A NEW SUPERIOR CONTENT\nhttps://www.youtube.com/watch?v={video['resourceId']['videoId']}"
    }
    response = requests.post(webhook_url, json=data)
    return response.status_code

if __name__ == "__main__":
    channel_name = get_channel_name(channel_id)
    latest_video = get_latest_video(channel_id)
    response_code = post_to_webhook(channel_name, latest_video)
    if response_code == 200:
        print('Successfully posted to webhook.')
    else:
        print('Failed to post to webhook.')
