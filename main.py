from bili_subtitle_downloader import BiliSubtitleDownloader
from bili_video_info_downloader import VideoInfoDownloader
from chatgpt_summary_writer import ChatGPTSummaryWriter
from notion_controller import NotionController
import argparse
import json
import os


class NoArgsError:
    pass


def read_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bv", help="获取bv号")
    parser.add_argument("-p", help="分p，默认为0")
    parser.add_argument("--summary_count", help="需要的精简概括的数量（默认为10条）")
    args = parser.parse_args()
    return (args.bv, args.p, args.summary_count)
    
if __name__ == "__main__":
    with open("settings.json", "r") as f:
        settings = json.load(f)
    notion_token = settings.get("notion_token")
    database_id = settings.get("database_id")
    api_key = settings.get("api_key")

    cookie = None
    if os.path.isfile("./cookie"):
        with open("./cookie", "r") as f:
            cookie = f.read()

    bv_id, p, summary_count = read_command_line_args()
    bv_id = bv_id if bv_id is not None else input("请输入BV号：")
    p_num = p if p is not None else 0

    print(f"开始处理：{bv_id}")
    video_info = VideoInfoDownloader(bv_id).download_video_info()
    title = video_info["info"]["title"]
    print(f"获取到视频信息：{title}")
    subtitle = BiliSubtitleDownloader(bv_id, p_num, cookie).download_subtitle()
    print("字幕获取成功，chatGPT开始编写摘要")
    summary = ChatGPTSummaryWriter(api_key, subtitle, summary_count).write_summary()
    print("chatGPT编写摘要成功")
    NotionController(notion_token, database_id).insert_to_notion(video_info, summary)
    print("导入Notion成功")