import requests

url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'

headers = {'Host': 'qun.qq.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/74.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept-Encoding': 'gzip, deflate, br',
           'Referer': 'https://qun.qq.com/member.html',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest',
           'Content-Length': '47',
           'Origin': 'https://qun.qq.com',
           'Cookie': '请填入自己的cookie',
           'Connection': 'keep-alive',
           'TE': 'Trailers'
           }

qq_group_num = input("请输人QQ群号：")

data = {'gc': str(qq_group_num),
        'st': '0',
        'end': '20',
        'sort': '0',
        'bkn': '1137758137'  # 改为自己的bkn
        }

"""
st:0    st:21   st:42   st:63    st:84      st:105
end:20  end:41  end:62  end:83   end:104    end:109
"""

# 获取群成员数量
html = requests.post(url, headers=headers, data=data)
member_count = html.json()["count"]

st = [i for i in range(0, member_count, 21)]
end = [j for j in range(20, member_count, 21)]
if member_count not in end:
    end.append(member_count)

ls = dict(zip(st, end))


def get_qq_group(url, headers, data):
    """
    进行数据的获取
    :param url: 请求网址
    :param headers: 请求头
    :param data: 传入的表单数据
    :return: 写入TXT文件
    """
    html = requests.post(url, headers=headers, data=data)
    # 群成员数量
    member_count = html.json()["count"]
    print(member_count)
    for i in range(len(html.json()['mems'])):
        qq = html.json()['mems'][i]['uin']
        name = html.json()['mems'][i]['nick']
        print(qq, name)
        with open('qq.txt', 'a', encoding='utf-8')as f:
            f.write(str(qq) + "," + str(name) + '\n')


if __name__ == '__main__':
    for i in ls:
        data = {'gc': str(qq_group_num),
                'st': str(i),
                'end': str(ls[i]),
                'sort': '0',
                'bkn': '1137758137'  # 改为自己的bkn
                }
        get_qq_group(url, headers, data)
