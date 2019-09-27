import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

'''    
解法一：hook点击事件,在onClick()方法中判断结果的方法showMessageTask()执行前有1秒延迟。
我们可以在判断结果前修改我们和电脑的出拳,直接让此时的我们赢了999次。
每次点击都是第1000次胜利,就得到了Flag。
'''

jscode = """
Java.perform(function () {
  var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity');
  MainActivity.onClick.implementation = function (v) {
    send("Hook Start...");
    this.onClick(v);
    this.cnt.value = 999;
    this.m.value = 0;
    this.n.value = 1;
    send("Success!");
  };
});
"""

'''
解法二：在源码中看到第1000胜利时只有calc()的值是未知的。
直接在onCreate()中调用calc()方法,解出Flag。
在Hook方法内还需要再调用onCreate()方法。
'''

jscode = """
Java.perform(function () {
    var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity');
    MainActivity.onCreate.implementation = function (a) {
        send("Hook Start...");
        send("Flag:" + "SECCON{" + ((1000 + this.calc()) * 107) + "}");
        this.onCreate(a);
        send("Success!");
    }
});
"""

process = frida.get_usb_device().attach('com.example.seccon2015.rock_paper_scissors')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()