import copy
import time
import httpx


def get_lates_fuck_post_datas(guid: str, episode: str):
    url = "https://h5.cyol.com/special/weixin/sign.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.7(0x13070010) Safari/605.1.15 NetType/WIFI",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    res = httpx.get(url, headers=headers)
    datas = res.json()
    latest_fuck_info = datas[list(datas.keys())[-1]]
    latest_fuck_video_link = latest_fuck_info["url"].strip()
    finish_pic_link = latest_fuck_video_link.replace("m.html", "images/end.jpg")
    download_finish_pic(finish_pic_link)
    tc = int(round(time.time() * 1000))
    tn = tc + 10 * 60 * 1000
    temp_data = '{{"guid":"{guid}","tc":"{tc}","tn":"{tn}","n":"{n}","u":"{u}","d":"cyol.com","r":"{r}","w":448,"m":"[{{\\"c\\":\\"2023\\",\\"s\\":\\"{s}\\"{other}}}]"}}'
    steps = ["打开页面", "开始学习", "播放完成", "课后答题"]
    data = {
        "guid": guid,
        "tc": tc,
        "tn": tn,
        "n": "打开页面",
        "u": latest_fuck_video_link + "?t=1&z=201",
        "r": latest_fuck_video_link.replace("m.html", "index.html"),
        "s": episode,
        "other": r',\"prov\":\"18\",\"city\":\"1\"',
    }
    for i in steps:
        if i == "打开页面":
            temp = copy.deepcopy(data)
            temp["other"] = ""
            result = temp_data.format(**temp)
        else:
            data["n"] = i
            result = temp_data.format(**data)
        send_to_log_api(result)


def download_finish_pic(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.7(0x13070010) Safari/605.1.15 NetType/WIFI",
    }
    res = httpx.get(url, headers=headers)
    with open("finish.jpg", "wb") as fo:
        fo.write(res.content)


def send_to_log_api(data: str) -> bool:
    url = "https://gqti.zzdtec.com/api/event"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.7(0x13070010) Safari/605.1.15 NetType/WIFI",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "*/*",
        "Origin": "https://h5.cyol.com",
        "Content-type": "text/plain",
        "Referer": "https://h5.cyol.com/",
        "Connection": "keep-alive"
    }
    res = httpx.post(url, headers=headers, data=data)
    print(data)
    print(res.text)
    if res.text == "ok" and res.status_code == 200:
        return True
    else:
        return False


def main():
    episode = input("input your episode:")
    guid = input("input your guid:")
    get_lates_fuck_post_datas(guid, episode)


if __name__ == '__main__':
    main()
