import requests

def bili_player_list(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid='+bvid
    response = requests.get(url)
    cid_list = [x['cid'] for x in response.json()['data']]
    return cid_list

def bili_subtitle_list(bvid, cid):
    url = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
    headers = {
        'authority': 'api.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Cookie': "buvid3=294F904A-526C-E549-6FDD-EED6EB4BF34914465infoc; b_nut=1675604514; _uuid=714551C9-F10B7-FEFE-10E1010-710F3C428D29247183infoc; DedeUserID=12129519; DedeUserID__ckMd5=0ccb57aa1f2addab; rpdid=|(u~||um|R|l0J'uY~lY|RlR~; b_ut=5; hit-new-style-dyn=0; hit-dyn-v2=1; buvid4=22E938FF-995E-0346-7972-E9613D36515A15296-023020521-wJ/XJ57ZLhxbUQoLPBkZ7Q==; buvid_fp_plain=undefined; nostalgia_conf=-1; CURRENT_QUALITY=80; LIVE_BUVID=AUTO5716759459604901; i-wanna-go-feeds=-1; i-wanna-go-back=-1; header_theme_version=CLOSE; CURRENT_FNVAL=4048; fingerprint=792a5b93f7d3387f172b2847f145272b; buvid_fp=792a5b93f7d3387f172b2847f145272b; SESSDATA=8152db08,1694145818,0a673*31; bili_jct=a82f1f11596476b52a8d1cea7b3cac0b; sid=5o9a2f8c; PVID=3; bp_video_offset_12129519=772107692630081500; innersign=1; b_lsid=17104D398_186D59BDD8C"
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    subtitles = response.json()['data']['subtitle']['subtitles']
    if subtitles:
        return ['https:' + x['subtitle_url'] for x in subtitles]
    else:
        return []

def bili_subtitle(bvid, cid):
    # add cookies if necessary
    subtitles = bili_subtitle_list(bvid, cid)
    if subtitles:
        response = requests.get(subtitles[0])
        if response.status_code == 200:
            body = response.json()['body']
            return body
    return []

bvid = "BV1fR4y1y7vT"
subtitle_text = bili_subtitle(bvid, bili_player_list(bvid)[0])
print(subtitle_text)