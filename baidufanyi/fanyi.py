jsCode = """
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
    var i = null;
    function e(r) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
    
            var u = void 0,l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
            u = null !== i ? i : (i = "320305.131321201" || "") || "";
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
"""
import execjs
query = input("请输入你想翻译的中文：")
#query="中国"
sign = execjs.compile(jsCode).call("e", str(query))
#print(sign)
import requests
import json

data={
    "from":"zh",
    "to":"en",
    "query":query,
    "transtype":"translang",
    "simple_means_flag":"3",
    "sign":sign,
    "token":"2b39a2cc2d9993e593a7bcdddbb19d07",
}

headers={
    "cookie":"BAIDUID=C739F25B99EEF3857CEE806F334450E0:FG=1; BIDUPSID=C739F25B99EEF3857CEE806F334450E0; PSTM=1559132826; BDUSS=16fko2fnliWn5mc2VMMnB1VC1NWm1LdktnN2xVNUMtU2J0NmtBdS1PZVBNeGhkSVFBQUFBJCQAAAAAAAAAAAEAAACnxPY9c2ZmZMC2yasAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI-m8FyPpvBccC; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; H_PS_PSSID=1450_21119_18560_29237_28519_29099_28832_29220_29072_22159; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ZD_ENTRY=baidu; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1562054101,1562054197,1562590995,1562592097; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1562592097; yjs_js_security_passport=28d88c7c5c25f664cd0c1100dbe61c0f9193bb05_1562592100_js; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D",
    "origin":"https://fanyi.baidu.com",
    "pragma":"no-cache",
    "referer":"https://fanyi.baidu.com/?aldtype=16047",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "x-requested-with":"XMLHttpRequest",
}

url='https://fanyi.baidu.com/v2transapi'
resp=requests.post(url=url,headers=headers,data=data)

print("翻译结果：")
print(resp.json()["trans_result"]["data"][0]["dst"])