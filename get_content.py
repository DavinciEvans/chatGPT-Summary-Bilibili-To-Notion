import time
import openai
import requests


def bili_info(bvid):
    params = (
        ('bvid', bvid),
    )
    response = requests.get('https://api.bilibili.com/x/web-interface/view', params=params)
    return response.json()['data']

def bili_tags(bvid):
    params = (
        ('bvid', bvid),
    )

    response = requests.get('https://api.bilibili.com/x/web-interface/view/detail/tag', params=params)
    data = response.json()['data']
    if data:
        tags = [x['tag_name'] for x in data]
        if len(tags) > 5:
            tags = tags[:5]
    else:
        tags = []
    return tags


sect = {13: {'name': '番剧', 'parent_tid': 13, 'parent_name': '番剧'},
 33: {'name': '连载动画', 'parent_tid': 13, 'parent_name': '番剧'},
 32: {'name': '完结动画', 'parent_tid': 13, 'parent_name': '番剧'},
 51: {'name': '资讯', 'parent_tid': 13, 'parent_name': '番剧'},
 152: {'name': '官方延伸', 'parent_tid': 13, 'parent_name': '番剧'},
 23: {'name': '电影', 'parent_tid': 23, 'parent_name': '电影'},
 167: {'name': '国创', 'parent_tid': 167, 'parent_name': '国创'},
 153: {'name': '国产动画', 'parent_tid': 167, 'parent_name': '国创'},
 168: {'name': '国产原创相关', 'parent_tid': 167, 'parent_name': '国创'},
 169: {'name': '布袋戏', 'parent_tid': 167, 'parent_name': '国创'},
 195: {'name': '动态漫·广播剧', 'parent_tid': 167, 'parent_name': '国创'},
 170: {'name': '资讯', 'parent_tid': 167, 'parent_name': '国创'},
 11: {'name': '电视剧', 'parent_tid': 11, 'parent_name': '电视剧'},
 177: {'name': '纪录片', 'parent_tid': 177, 'parent_name': '纪录片'},
 1: {'name': '动画', 'parent_tid': 1, 'parent_name': '动画'},
 24: {'name': 'MAD·AMV', 'parent_tid': 1, 'parent_name': '动画'},
 25: {'name': 'MMD·3D', 'parent_tid': 1, 'parent_name': '动画'},
 47: {'name': '短片·手书·配音', 'parent_tid': 1, 'parent_name': '动画'},
 210: {'name': '手办·模玩', 'parent_tid': 1, 'parent_name': '动画'},
 86: {'name': '特摄', 'parent_tid': 1, 'parent_name': '动画'},
 27: {'name': '综合', 'parent_tid': 1, 'parent_name': '动画'},
 4: {'name': '游戏', 'parent_tid': 4, 'parent_name': '游戏'},
 17: {'name': '单机游戏', 'parent_tid': 17, 'parent_name': '单机游戏'},
 171: {'name': '电子竞技', 'parent_tid': 4, 'parent_name': '游戏'},
 172: {'name': '手机游戏', 'parent_tid': 4, 'parent_name': '游戏'},
 65: {'name': '网络游戏', 'parent_tid': 4, 'parent_name': '游戏'},
 173: {'name': '桌游棋牌', 'parent_tid': 4, 'parent_name': '游戏'},
 121: {'name': 'GMV', 'parent_tid': 4, 'parent_name': '游戏'},
 136: {'name': '音游', 'parent_tid': 4, 'parent_name': '游戏'},
 19: {'name': 'Mugen', 'parent_tid': 4, 'parent_name': '游戏'},
 119: {'name': '鬼畜', 'parent_tid': 119, 'parent_name': '鬼畜'},
 22: {'name': '鬼畜调教', 'parent_tid': 119, 'parent_name': '鬼畜'},
 26: {'name': '音MAD', 'parent_tid': 119, 'parent_name': '鬼畜'},
 126: {'name': '人力VOCALOID', 'parent_tid': 119, 'parent_name': '鬼畜'},
 216: {'name': '鬼畜剧场', 'parent_tid': 119, 'parent_name': '鬼畜'},
 127: {'name': '教程演示', 'parent_tid': 119, 'parent_name': '鬼畜'},
 3: {'name': '音乐', 'parent_tid': 3, 'parent_name': '音乐'},
 28: {'name': '原创音乐', 'parent_tid': 3, 'parent_name': '音乐'},
 31: {'name': '翻唱', 'parent_tid': 3, 'parent_name': '音乐'},
 30: {'name': 'VOCALOID·UTAU', 'parent_tid': 3, 'parent_name': '音乐'},
 194: {'name': '电音', 'parent_tid': 3, 'parent_name': '音乐'},
 59: {'name': '演奏', 'parent_tid': 3, 'parent_name': '音乐'},
 193: {'name': 'MV', 'parent_tid': 3, 'parent_name': '音乐'},
 29: {'name': '音乐现场', 'parent_tid': 3, 'parent_name': '音乐'},
 130: {'name': '音乐综合', 'parent_tid': 3, 'parent_name': '音乐'},
 129: {'name': '舞蹈', 'parent_tid': 129, 'parent_name': '舞蹈'},
 20: {'name': '宅舞', 'parent_tid': 129, 'parent_name': '舞蹈'},
 198: {'name': '街舞', 'parent_tid': 129, 'parent_name': '舞蹈'},
 199: {'name': '明星舞蹈', 'parent_tid': 129, 'parent_name': '舞蹈'},
 200: {'name': '中国舞', 'parent_tid': 129, 'parent_name': '舞蹈'},
 154: {'name': '舞蹈综合', 'parent_tid': 129, 'parent_name': '舞蹈'},
 156: {'name': '舞蹈教程', 'parent_tid': 129, 'parent_name': '舞蹈'},
 181: {'name': '影视', 'parent_tid': 181, 'parent_name': '影视'},
 182: {'name': '影视杂谈', 'parent_tid': 181, 'parent_name': '影视'},
 183: {'name': '影视剪辑', 'parent_tid': 181, 'parent_name': '影视'},
 85: {'name': '短片', 'parent_tid': 181, 'parent_name': '影视'},
 184: {'name': '预告·资讯', 'parent_tid': 181, 'parent_name': '影视'},
 5: {'name': '娱乐', 'parent_tid': 5, 'parent_name': '娱乐'},
 71: {'name': '综艺', 'parent_tid': 5, 'parent_name': '娱乐'},
 241: {'name': '娱乐杂谈', 'parent_tid': 5, 'parent_name': '娱乐'},
 242: {'name': '粉丝创作', 'parent_tid': 5, 'parent_name': '娱乐'},
 137: {'name': '明星综合', 'parent_tid': 5, 'parent_name': '娱乐'},
 36: {'name': '知识', 'parent_tid': 36, 'parent_name': '知识'},
 201: {'name': '科学科普', 'parent_tid': 36, 'parent_name': '知识'},
 124: {'name': '社科·法律·心理', 'parent_tid': 36, 'parent_name': '知识'},
 228: {'name': '人文历史', 'parent_tid': 36, 'parent_name': '知识'},
 207: {'name': '财经商业', 'parent_tid': 36, 'parent_name': '知识'},
 208: {'name': '校园学习', 'parent_tid': 36, 'parent_name': '知识'},
 209: {'name': '职业职场', 'parent_tid': 36, 'parent_name': '知识'},
 229: {'name': '设计·创意', 'parent_tid': 36, 'parent_name': '知识'},
 122: {'name': '野生技能协会', 'parent_tid': 36, 'parent_name': '知识'},
 188: {'name': '科技', 'parent_tid': 188, 'parent_name': '科技'},
 95: {'name': '数码', 'parent_tid': 188, 'parent_name': '科技'},
 230: {'name': '软件应用', 'parent_tid': 188, 'parent_name': '科技'},
 231: {'name': '计算机技术', 'parent_tid': 188, 'parent_name': '科技'},
 232: {'name': '工业·工程·机械', 'parent_tid': 188, 'parent_name': '科技'},
 202: {'name': '资讯', 'parent_tid': 202, 'parent_name': '资讯'},
 203: {'name': '热点', 'parent_tid': 202, 'parent_name': '资讯'},
 204: {'name': '环球', 'parent_tid': 202, 'parent_name': '资讯'},
 205: {'name': '社会', 'parent_tid': 202, 'parent_name': '资讯'},
 206: {'name': '综合', 'parent_tid': 202, 'parent_name': '资讯'},
 211: {'name': '美食', 'parent_tid': 211, 'parent_name': '美食'},
 76: {'name': '美食制作', 'parent_tid': 211, 'parent_name': '美食'},
 212: {'name': '美食侦探', 'parent_tid': 211, 'parent_name': '美食'},
 213: {'name': '美食测评', 'parent_tid': 211, 'parent_name': '美食'},
 214: {'name': '田园美食', 'parent_tid': 211, 'parent_name': '美食'},
 215: {'name': '美食记录', 'parent_tid': 211, 'parent_name': '美食'},
 160: {'name': '生活', 'parent_tid': 160, 'parent_name': '生活'},
 138: {'name': '搞笑', 'parent_tid': 138, 'parent_name': '搞笑'},
 163: {'name': '家居房产', 'parent_tid': 160, 'parent_name': '生活'},
 161: {'name': '手工', 'parent_tid': 160, 'parent_name': '生活'},
 162: {'name': '绘画', 'parent_tid': 160, 'parent_name': '生活'},
 21: {'name': '日常', 'parent_tid': 160, 'parent_name': '生活'},
 223: {'name': '汽车', 'parent_tid': 223, 'parent_name': '汽车'},
 176: {'name': '汽车生活', 'parent_tid': 223, 'parent_name': '汽车'},
 224: {'name': '汽车文化', 'parent_tid': 223, 'parent_name': '汽车'},
 225: {'name': '汽车极客', 'parent_tid': 223, 'parent_name': '汽车'},
 240: {'name': '摩托车', 'parent_tid': 223, 'parent_name': '汽车'},
 226: {'name': '智能出行', 'parent_tid': 223, 'parent_name': '汽车'},
 227: {'name': '购车攻略', 'parent_tid': 223, 'parent_name': '汽车'},
 155: {'name': '时尚', 'parent_tid': 155, 'parent_name': '时尚'},
 157: {'name': '美妆护肤', 'parent_tid': 155, 'parent_name': '时尚'},
 158: {'name': '穿搭', 'parent_tid': 155, 'parent_name': '时尚'},
 159: {'name': '时尚潮流', 'parent_tid': 155, 'parent_name': '时尚'},
 234: {'name': '运动', 'parent_tid': 234, 'parent_name': '运动'},
 235: {'name': '篮球·足球', 'parent_tid': 234, 'parent_name': '运动'},
 164: {'name': '健身', 'parent_tid': 234, 'parent_name': '运动'},
 236: {'name': '竞技体育', 'parent_tid': 234, 'parent_name': '运动'},
 237: {'name': '运动文化', 'parent_tid': 234, 'parent_name': '运动'},
 238: {'name': '运动综合', 'parent_tid': 234, 'parent_name': '运动'},
 217: {'name': '动物圈', 'parent_tid': 217, 'parent_name': '动物圈'},
 218: {'name': '喵星人', 'parent_tid': 217, 'parent_name': '动物圈'},
 219: {'name': '汪星人', 'parent_tid': 217, 'parent_name': '动物圈'},
 220: {'name': '大熊猫', 'parent_tid': 217, 'parent_name': '动物圈'},
 221: {'name': '野生动物', 'parent_tid': 217, 'parent_name': '动物圈'},
 222: {'name': '爬宠', 'parent_tid': 217, 'parent_name': '动物圈'},
 75: {'name': '动物综合', 'parent_tid': 217, 'parent_name': '动物圈'}}

def bili_player_list(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid='+bvid
    response = requests.get(url)
    cid_list = [x['cid'] for x in response.json()['data']]
    return cid_list

def bili_subtitle_list(bvid, cid):
    url = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
    response = requests.get(url)
    subtitles = response.json()['data']['subtitle']['subtitles']
    if subtitles:
        return ['https:' + x['subtitle_url'] for x in subtitles]
    else:
        return []

def bili_subtitle(bvid, cid):
    headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    }
    subtitles = bili_subtitle_list(bvid, cid)
    if subtitles:
        response = requests.get(subtitles[0], headers=headers)
        if response.status_code == 200:
            body = response.json()['body']
            return body
    return []


def segTranscipt(transcript):
    transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in enumerate(transcript)]
    text = " ".join([x["text"] for x in sorted(transcript, key=lambda x: x["index"])])
    length = len(text)
    seg_length = 3400
    n = length // seg_length + 1
    print(f"视频文本共{length}字, 分为{n}部分进行摘要")
    division = len(transcript) // n
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    segedTranscipt = [" ".join([x["text"] for x in sorted(j, key=lambda x: x["index"])]) for j in new_l]
    return segedTranscipt

def chat(api_key, prompt, text):
    openai.api_key = api_key
    completions = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {"role": "system", "content": "一个视频内容概括助手"},
            {"role": "user", "content": prompt + text},
        ],
    )
    ans = completions.choices[0].message.content
    return ans


def insert2notion(token, database_id, bvid, summarized_text):    
    headers = {
        'Notion-Version': '2022-06-28',
        'Authorization': 'Bearer '+token,
    }
    info = bili_info(bvid)
    print(f'正在导入视频信息：{info["title"]}')
    tags = bili_tags(bvid)
    multi_select = []
    pubdate = time.strftime("%Y-%m-%d", time.localtime(info['pubdate']))
    for each in tags:
        multi_select.append({'name': each})
    body= {
        "parent": {"type": "database_id","database_id": database_id},
        "properties": {
            "标题": { "title": [{"type": "text","text": {"content": info['title']}}]},
            "URL": { "url": 'https://www.bilibili.com/video/'+bvid},
            "UP主": { "rich_text": [{"type": "text","text": {"content": info['owner']['name']}}]},
            "分区": { "select": {"name": sect[info['tid']]['parent_name']}},
            'tags': {'type': 'multi_select', 'multi_select': multi_select},
            "发布时间": { "date": {"start": pubdate, "end": None }},
            # "观看时间": { "date": {"start": time.strftime("%Y-%m-%d", time.localtime()), "end": None }},
            # "封面": {'files': [{"type": "external", "name": "封面",'external': {'url': info['pic']}}]},
        },
        "children": [
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
                    }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": summarized_text,
                            "link": None,
                        }
                    }]
                }
            }]
    }
    notion_request = requests.post("https://api.notion.com/v1/pages", json = body, headers=headers)
    if(str(notion_request.status_code) == "200"):
        print("导入信息成功")
        return(notion_request.json()['url'])
    else:
        print("导入失败，请检查Body字段")
        print(notion_request.text)
        return('')



def main():
    notion_token = 'secret_EIgw5snYm4sjVo9biUr5veuNT8tCxHHpHikOhrnMyzj'
    database_id = '3fb34eba370345bfa6affe6b6968eb8c'
    api_key = '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'
    bvid = input('请输入B站的BV号：')
    # bvid = blink.split('/')[4]
    print(f'开始处理视频信息：{bvid}')
    prompt = '请你帮我将以下视频字幕文本的精华内容进行总结，然后以无序列表的方式返回，不要超过5条！确保所有的句子都足够精简，清晰完整。并无视开头和结尾作者关于订阅或点赞的内容。以下是视频字幕内容：'
    transcript_text = bili_subtitle(bvid, bili_player_list(bvid)[0])
    if transcript_text:
        print('字幕获取成功')
        seged_text = segTranscipt(transcript_text)
        summarized_text = ''
        i = 1
        for entry in seged_text:
            try:
                response = chat(api_key, prompt, entry)
                print(f'完成第{str(i)}部分摘要')
                i += 1
            except:
                print('GPT接口摘要失败, 请检查网络连接')
                response = '摘要失败'
            summarized_text += '\n'+response
        insert2notion(notion_token, database_id, bvid, summarized_text)
    else:
        print('字幕获取失败')

if __name__ == '__main__':
    main()