import pytchat
from multiprocessing import Process
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import json

load_dotenv()
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
host = os.getenv("HOST")


def load_youtube_chat(video_id):
    db = MongoClient( host=host, username=mongo_user, password=mongo_password, port=27017)["youtube_chat"]
    collection = db["chat"]
    yt = pytchat.create(video_id=video_id)
    while yt.is_alive():
        for c in yt.get().sync_items():
            print(f"{c.json()}")
            document = json.loads( c.json() )
            document["youtube_id"] = video_id
            collection.update_one(
                {"id": document["id"]},  # Match condition (use a unique field, e.g., "id")
                {"$set": document},  # Fields to set/update
                upsert=True  # Enable upsert
            )

def main():
    df = pd.read_csv("yt_list.csv")
    yt_list = df["id"]
    processes = []


    # Create and start a process for each video ID
    for video_id in yt_list:
        process = Process(target=load_youtube_chat, args=(video_id,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()