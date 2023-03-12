from typing import Optional
import openai
import time


class ChatGPTSummaryWriter:
    def __init__(self, api_key: str, text: str, summary_count: Optional[int] = None) -> None:
        self.api_key = api_key
        self.text = text
        self.seg_length = 3400
        self.summary_count = 10 if summary_count is None else summary_count

    
    def _seg_content(self):
        text_length = len(self.text)
        n = text_length // self.seg_length + 1
        segment_text = [self.text[(self.seg_length*i) : (self.seg_length*(i+1)) if text_length > (self.seg_length*(i+1)-1) else text_length] for i in range(n)]
        return segment_text
    
    def write_summary(self):
        openai.api_key = self.api_key
        prompt = f'请你帮我将以下视频字幕文本的精华内容进行总结，然后以无序列表的方式返回，不要超过{self.summary_count}条！确保所有的句子都足够精简，清晰完整，并无视任何作者的推广、点赞、订阅等内容。以下是视频字幕内容：'

        for times in range(5):
            try:
                completions = openai.ChatCompletion.create(
                    model = 'gpt-3.5-turbo',
                    messages = [
                        {"role": "system", "content": "一个视频内容概括助手"},
                        {"role": "user", "content": prompt + self.text},
                    ],
                )
                break
            except openai.APIError as e:
                print(e)
                print(f"请求失败，准备进行第 {times+2} 次请求尝试")
                time.sleep((times+1)*5)

        if times == 4:
            raise ChatGPTConnectError("ChatGPT连接错误")
        
        ans = completions.choices[0].message.content
        return ans


class ChatGPTConnectError:
    pass