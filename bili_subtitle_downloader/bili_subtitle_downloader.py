import requests
import os 


class BiliSubtitleDownloader:
    def __init__(self, bv_id: str, p_num: int, cookie: str):
        self.bv_id = bv_id
        self.p_num = p_num
        self.pagelist_api = 'https://api.bilibili.com/x/player/pagelist'
        self.subtitle_api = f'https://api.bilibili.com/x/player/v2'
        self.headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Cookie': cookie
        }


    def _get_player_list(self):
        response = requests.get(self.pagelist_api, params={'bvid': self.bv_id})
        cid_list = [x['cid'] for x in response.json()['data']]
        return cid_list
    

    def _get_subtitle_list(self, cid: int):
        params = (
            ('bvid', self.bv_id),
            ('cid', cid)
        )
        response = requests.get(self.subtitle_api, headers=self.headers, params=params)
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            return ['https:' + x['subtitle_url'] for x in subtitles]
        return []
        
    
    def _get_subtitle(self, cid: str):
        subtitles = self._get_subtitle_list(cid)
        if subtitles:
            return self._request_subtitle(subtitles[0])
        else:
            cookie = input("请输入cookie：")
            with open("./cookie", "w") as f:
                f.write(cookie)
            self.headers["Cookie"] = cookie
            subtitles = self._get_subtitle_list(cid)
            if subtitles:
                return self._request_subtitle(subtitles[0])

        raise SubtitleDownloadError("字幕下载失败，请确保原视频有cc字幕并更换新的cookie")
    

    def _request_subtitle(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            body = response.json()['body']
            return body
    

    def download_subtitle(self):
        subtitle_list = self._get_subtitle(self._get_player_list()[self.p_num])
        subtitle = ", ".join([x['content'] for x in subtitle_list])
        return subtitle


class SubtitleDownloadError(Exception):
    pass
