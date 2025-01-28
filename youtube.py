import pytchat
from multiprocessing import Process
import pandas as pd


def load_youtube_chat(video_id):
    yt = pytchat.create(video_id=video_id)
    while yt.is_alive():
        for c in yt.get().sync_items():
            print(f"{c.json()}")

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