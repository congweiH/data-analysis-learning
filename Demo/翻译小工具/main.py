import js2py
import requests
import re
import json

class Fanyi:
    def __init__(self,word,to_lan=None):
        '''
        :param word: 翻译的内容
        :param to_lan: 翻译后的语言
         "zh":中文，"en":英文，"jp":日语，"kor":韩语,"de":德语，"fra":法语，"ru":俄语
        '''
        self.word = word
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "Cookie":"BAIDUID=6737C296C853173DAB856FED5FBF25F5:FG=1; BIDUPSID=6737C296C853173DAB856FED5FBF25F5; PSTM=1545117994; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDUSS=5Vfjc2R3FCZVpUYlNIblFmSVV0NDNwOW9ySmEtVVFBWXdIamZafjB6WUZPelZkSVFBQUFBJCQAAAAAAAAAAAEAAABFdh3EaU11cnBoeXIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWuDV0Frg1dUU; H_PS_PSSID=1427_21102_29522_29520_29721_29567_29221; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=5; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1567392751,1567392962,1567392984,1567420420; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1567420420; APPGUIDE_8_0_0=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1567422653,1567422686,1567424993,1567425108; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1567427040; __yjsv5_shitong=1.0_7_dc8b8f3b6a56183f0bb6155366f89c2a816b_300_1567427040913_122.195.67.210_e7b1c846; yjs_js_security_passport=5d7fe0960b4d7e88d50f05c5a707327bf14b611d_1567427043_js; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D"
        }
        self.post_url = "https://fanyi.baidu.com/v2transapi"
        self.sign = None
        self.to_lan = to_lan

    def get_sign(self,word): # 计算sign值
        session = requests.Session()
        session.headers=self.headers
        response = session.get("http://fanyi.baidu.com/")
        gtk = re.findall(";window.gtk = ('.*?');", response.content.decode())[0]
        context = js2py.EvalJs()
        js = r'''
        function a(r) {
                if (Array.isArray(r)) {
                    for (var o = 0, t = Array(r.length); o < r.length; o++)
                        t[o] = r[o];
                    return t
                }
                return Array.from(r)
            }
            function n(r, o) {
                for (var t = 0; t < o.length - 2; t += 3) {
                    var a = o.charAt(t + 2);
                    a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
                        a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
                        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
                }
                return r
            }
            function e(r) {
                var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
                if (null === o) {
                    var t = r.length;
                    t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
                } else {
                    for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                        "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                        C !== h - 1 && f.push(o[C]);
                    var g = f.length;
                    g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
                }
                var u = void 0
                    , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
                u = 'null !== i ? i : (i = window[l] || "") || ""';
                for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
                    var A = r.charCodeAt(v);
                    128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
                        S[c++] = A >> 18 | 240,
                        S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
                        S[c++] = A >> 6 & 63 | 128),
                        S[c++] = 63 & A | 128)
                }
                for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
                    p += S[b],
                        p = n(p, F);
                return p = n(p, D),
                    p ^= s,
                0 > p && (p = (2147483647 & p) + 2147483648),
                    p %= 1e6,
                p.toString() + "." + (p ^ m)
            }
        '''
        # js中添加一行gtk
        js = js.replace('\'null !== i ? i : (i = window[l] || "") || ""\'', gtk)
        # 执行js
        context.execute(js)
        sign = context.e(word)
        return sign

    def parse_url(self,url):    # 发送post请求
        data = {
            "from": None,
            "to": self.to_lan,
            "query": self.word,
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": self.sign,
            "token": "8e3e547a6eeb51b0e15dadf70e7e01f0"
        }
        r = requests.post(url, data=data, headers=self.headers)
        # 把json格式转成字典格式
        return json.loads(r.content.decode())

    def get_result(self,text): # 分析返回的jaon数据
        ret = text["trans_result"]["data"][0]["dst"]
        print(ret)

    def run(self): # 实现主要逻辑
        # 1.通过翻译的内容计算sign值
        self.sign = self.get_sign(self.word)
        # 2.发送post请求,获取相应后的内容
        text = self.parse_url(self.post_url)
        # 3.获取翻译后的内容
        self.get_result(text)

if __name__ == '__main__':
    ret = Fanyi("안녕하세요.")
    ret.run()
