import os
import json
from TikTokApi import TikTokApi
from yt_dlp import YoutubeDL
import asyncio
from datetime import datetime, timedelta

# Hard-code the ms_token value
ms_token = "YOUR_MS_TOKEN_HERE"

# Set the time threshold (2 years ago)
time_threshold = datetime.now() - timedelta(days=2 * 365)

# Define the search keywords and hashtags
keywords = [
    "soccer dribbling drills",
    "soccer passing drills",
    "soccer shooting drills",
    "soccer ball control drills",
    "soccer heading drills",
    "soccer tackling drills"
]

hashtags = [
    "soccerdribblingdrills",
    "soccerpassingdrills",
    "soccershootingdrills",
    "soccerballcontroldrills",
    "soccerheadingdrills",
    "soccertacklingdrills"
]

# Maximum number of videos to download per keyword
max_videos = 200

async def search_and_download_videos(keyword, is_hashtag=False):
    output_dir = f"output/{keyword.replace(' ', '')}"
    video_output_dir = os.path.join(output_dir, "videos")
    os.makedirs(video_output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{keyword.replace(' ', '')}.json")
    formatted_output_file = os.path.join(output_dir, f"formatted_{keyword.replace(' ', '')}.json")

    print(f"Starting search and download for {keyword}")
    try:
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)

            video_list = []
            cursor = 0
            has_more = True

            while has_more and len(video_list) < max_videos:
                if is_hashtag:
                    async for video in api.hashtag(name=keyword).videos(count=100, cursor=cursor):
                        video_data = video.as_dict
                        video_list.append(video_data)
                        if len(video_list) >= max_videos:
                            break
                else:
                    search_url = f"https://www.tiktok.com/api/search/item/full/"
                    params = {
                        "keyword": keyword,
                        "count": 100,
                        "cursor": cursor,
                        "source": "search_video"
                    }
                    response = await api.make_request(url=search_url, params=params)

                    if "item_list" in response:
                        for video_data in response["item_list"]:
                            video_list.append(video_data)
                            if len(video_list) >= max_videos:
                                break

                    has_more = response.get("has_more", False)
                    cursor = response.get("cursor", 0)

                print(f"Cursor: {cursor}, Number of items retrieved: {len(video_list)}")
            
            video_list = video_list[:max_videos]

            for video in video_list:
                username = video['author']['uniqueId']
                upload_time = datetime.fromtimestamp(video['createTime']).strftime('%Y%m%d')
                filename = f"{username}_{video['id']}_{upload_time}.mp4"
                video_url = f"https://www.tiktok.com/@{username}/video/{video['id']}"

                ydl_opts = {
                    'outtmpl': os.path.join(video_output_dir, filename),
                }

                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                        print(f"Downloaded video: {video_url}")
                except Exception as e:
                    print(f"Failed to download video: {video_url}, error: {e}")

            with open(output_file, "w") as f:
                json.dump(video_list, f, indent=4)

            reformat_json(output_file, formatted_output_file)

    except Exception as e:
        print(f"An error occurred: {e}")

def reformat_json(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        video_list = json.load(f)

    formatted_list = []

    for video in video_list:
        post_text = video["desc"]
        profile_name = video["author"]["uniqueId"]
        video_id = video["id"]
        created_date = datetime.fromtimestamp(video["createTime"]).strftime('%Y-%m-%d')
        video_filename = f"tiktok_{profile_name}_{video_id}_{created_date}.mp4"

        formatted_video = {
            "text": post_text,
            "tags": video.get('keyword', ''),
            "pillars": "technical skills",
            "user_type": "player, coach",
            "mediaFileUrl": video_filename,
            "externalCreatedAt": datetime.fromtimestamp(video["createTime"]).strftime('%Y-%m-%d %H:%M:%S'),
            "externalAuthor": profile_name,
            "externalPostUrl/ID": f"https://www.tiktok.com/@{profile_name}/video/{video_id}",
            "externalSiteName": "tiktok"
        }
        formatted_list.append(formatted_video)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    for keyword in keywords:
        asyncio.run(search_and_download_videos(keyword))
    for hashtag in hashtags:
        asyncio.run(search_and_download_videos(hashtag, is_hashtag=True))
    print("Script completed")
