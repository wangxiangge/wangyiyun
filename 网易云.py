import requests
import execjs
import os


headers = {
        'cookie': '_iuqxldmzr_=32; _ntes_nnid=babaf8c1e7a6d0a10a3df8ca24d0537e,1629115954710; _ntes_nuid=babaf8c1e7a6d0a10a3df8ca24d0537e; NMTID=00O6rbHNWfCJ0uRFk9ik5Dq7R9AbRsAAAF7TuC2jA; WEVNSM=1.0.0; WNMCID=opgyne.1629115955204.01.0; WM_TID=JTwG3VdoBzdAVQFUUQM7j2StqQTLjgOA; ntes_kaola_ad=1; JSESSIONID-WYYY=wwaZCd23Sa5FM4OeGe89d9nD0j%5C1QpteqeQst9Dgg7359hAa3Vj1OxiE9Oxq6J0hsyTJdww3niUn3Hu8vkvTtbRYpekCpWK13ShPOpSpUNzG8g696Ga2N69Dd8N12fHIf7YAcJfajkHXNV99Zvw36ytqJWQi0Z%2B%5C3mecVgc4EJ%5C%2BiOCz%3A1647963200763; WM_NI=v4ZB4CtKQNf1lg3kw2Mb%2BSZz368nSR%2BXC7WrXcgQAeY8agk3D8HD7qQ%2BF6Sqn4Tk0axtq4L9U373Y6mQ%2B1Pn5WX2K1pewF2%2FeYw1DuXohqjXGWjtqqEVtW74rYknoIp5V0Q%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeadd05ced958ad7e1428cb48aa2d85b929e9aafaa3db4adaca4c733f893888cd32af0fea7c3b92ab6ec96a3b749b8959fafe53bb0b9fd8cf63a8fbee5b4d972f1eaf88fd25ae9888dd8d67a9cbda9b2c46f9be8af88ea3988e888a5b67b93f58ad7d27baeec9c8cb36bbcacbfd5cf3397edf9d4dc3eaf8fe5d2d366f78998d3ca3bb4bbb9a7b125a787b9d2c77f9cb1a892e9548589a695f47b878abcb8b640b287a58fee43b4eb9ad1d437e2a3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}

judge = os.path.exists(".\music")
if judge == True:
    pass
else:
    os.mkdir(".\music")


"""
通过js代码解析获得想要的歌曲的id
"""
def get_id(name):
    num_1 = 1
    music_list = []
    musician_list = []
    music_id_list = []
    url_1 = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=a4c5aabbdb05c59e612162108ab8c0ce'
    js = open("网易云.js", 'r', encoding='utf-8').read()
    ctx = execjs.compile(js)
    result = ctx.call('start_id', name)
    data_1 = {
        'params': result['encText'],
        'encSecKey': result['encSecKey']
    }
    data_list = requests.post(url=url_1, data=data_1, headers=headers).json()["result"]["songs"]
    for data in data_list:
        music_1 = data['name']
        musician_1 = data['ar'][0]['name']
        music_id_1 = data['id']
        print(num_1, music_1, musician_1, music_id_1)
        num_1 = num_1 + 1
        music_list.append(music_1)
        musician_list.append(musician_1)
        music_id_list.append(music_id_1)
    num_2 = int(input("您想听第几首歌曲：")) - 1
    id = music_id_list[num_2]
    music = music_list[num_2]
    musician = musician_list[num_2]
    return music,musician,id


"""
通过获得的id再次进行js代码解析并进一步得到想要的歌曲的链接
"""
def get_url(id):
    url_2 = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=a4c5aabbdb05c59e612162108ab8c0ce'
    js = open("网易云.js", 'r', encoding='utf-8').read()
    ctx = execjs.compile(js)
    result = ctx.call('start', id)
    data = {
        'params': result['encText'],
        'encSecKey': result['encSecKey']
    }
    res = requests.post(url=url_2, data=data, headers=headers).json()['data'][0]['url']
    return res


"""
通过获得的歌曲的链接进行指定路径的下载
"""
def download_url(url,music,musician):
    response = requests.get(url=url)
    with open(f".\music\{music}（{musician}）.mp3","wb") as code:
        code.write(response.content)
    print(f"{music}（{musician}）.mp3")
    print("1：播放，2：不播放")
    idea = int(input("你是否想播放刚才下载好的音乐："))
    if idea == 1:
        os.system(f".\music\{music}（{musician}）.mp3")
    elif idea == 2:
        pass
    else:
        print("你的输入不正确。。。。。。。。。系统自动跳过，不进行播放")
        pass



if __name__ == '__main__':
    name = input("你想要听的歌的歌名或者歌手：")
    music,musician,id = get_id(name)
    url = get_url(id)
    download_url(url,music,musician)