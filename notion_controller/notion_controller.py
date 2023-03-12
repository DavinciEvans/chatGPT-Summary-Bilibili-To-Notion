import time
from typing import Dict
import requests


class NotionController:
    def __init__(self, token: str, database_id: str) -> None:
        self.database_id = database_id
        self.headers = {
            'Notion-Version': '2022-06-28',
            'Authorization': 'Bearer '+token,
        }
        self.notion_api = "https://api.notion.com/v1/pages"

    def insert_to_notion(self, video_info: Dict, summarized_text: str):
        info = video_info["info"]
        tags = video_info["tags"]
        multi_select = [{'name': tag} for tag in tags]

        body = {
            "parent": {"type": "database_id","database_id": self.database_id},
            "properties": {
                "标题": { "title": [{"type": "text","text": {"content": info['title']}}]},
                "URL": { "url": 'https://www.bilibili.com/video/'+video_info["bvid"]},
                "UP主": { "rich_text": [{"type": "text","text": {"content": info['owner']['name']}}]},
                "分区": { "select": {"name": video_info["section"]['parent_name']}},
                'tags': {'type': 'multi_select', 'multi_select': multi_select},
                "发布时间": {"date": {"start": time.strftime("%Y-%m-%d", time.localtime(info['pubdate'])), "end": None }},
            },
            "children": self._generate_children(info, summarized_text)
        }

        for times in range(3):
            try:
                notion_request = requests.post(self.notion_api, json=body, headers=self.headers)
                if(str(notion_request.status_code) == "200"):
                    return(notion_request.json()['url'])
            except:
                print(f"Notion 导入失败，准备第{times+2}次重试")
            
            print(notion_request.text)
            raise NotionConnectError("Notion 导入错误")

    def _generate_children(self, info: Dict, summarized_text: str):        
        children = [
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": info['pic']
                    }
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                            "content": "内容摘要："
                            }
                        }
                    ]
                }
            },
        ]
        item_list = summarized_text.split("- ")
        for item in item_list:
            if not item:
                continue
            bullet_item = {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": item.replace("\n", ""),
                                "link": None
                            }
                        }
                    ]
                }
            }
            children.append(bullet_item)

        return children
    

class NotionConnectError:
    pass