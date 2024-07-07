import requests
from googleapiclient.discovery import build

# YouTube Data API setup
api_key = 'YOUR_YOUTUBE_API_KEY'
webhook_url = 'YOUR_WEBHOOK_URL'
channels_file = 'channels.txt'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_name(channel_id):
    response = youtube.channels().list(part='snippet', id=channel_id).execute()
    channel_name = response['items'][0]['snippet']['title']
    return channel_name

def get_latest_video(channel_id):
    response = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    response = youtube.playlistItems().list(part='snippet', playlistId=uploads_playlist_id, maxResults=1).execute()
    latest_video = response['items'][0]['snippet']

    return latest_video

def post_to_webhook(channel_name, video):
    data = {
        "content": f"{channel_name} UPLOADED A NEW SUPERIOR CONTENT\nhttps://www.youtube.com/watch?v={video['resourceId']['videoId']}"
    }
    response = requests.post(webhook_url, json=data)
    return response.status_code

def read_channel_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

if __name__ == "__main__":
    channel_ids = read_channel_ids(channels_file)
    
    for channel_id in channel_ids:
        try:
            channel_name = get_channel_name(channel_id)
            latest_video = get_latest_video(channel_id)
            response_code = post_to_webhook(channel_name, latest_video)
            if response_code == 200:
                print(f'Successfully posted to webhook for channel: {channel_name}.')
            else:
                print(f'Failed to post to webhook for channel: {channel_name}.')
        except Exception as e:
            print(f'Error processing channel ID {channel_id}: {e}')
