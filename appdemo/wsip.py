import frida,sys
 
def on_message(message,data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)
 
jscode = """
Java.perform(function(){

    //由于js中实现字符串转bytes相对复杂，这里可以调用java中的方法
    function stringToBytes(str){
        var javaString = Java.use('java.lang.String');
        var bytes = [];
        bytes = javaString.$new(str).getBytes();
        return bytes;
    } 
    function bytesToString(bytes){
        var javaString = Java.use('java.lang.String');
        return javaString.$new(bytes);
    }   

    //Hook方法选择下面一个就行
    //方法一:Hook getKey()，直接计算activedKey的值
    var launcherActivity = Java.use('de.fraunhofer.sit.premiumapp.LauncherActivity');
    var MainActivity = Java.use('de.fraunhofer.sit.premiumapp.MainActivity');       
    launcherActivity.getKey.implementation = function(){
        send("Hook start...");
        var mac = this.getMac();
        send("mac:" + mac);
        //实例化MainActivity
        var instance = MainActivity.$new()
        //调用实例化对象的xor方法
        var xorResult = instance.xor(stringToBytes(mac), stringToBytes("LICENSEKEYOK"));
        var activedKey = bytesToString(xorResult)
        send("activedKey:" + activedKey);
        return activedKey;
    }

    //方法二：Hook showPremium，也就是第二个控件，计算前getKey返回空，计算后返回activedKey的值
    var launcherActivity = Java.use('de.fraunhofer.sit.premiumapp.LauncherActivity');
    var activedKey = "";
    launcherActivity.getKey.implementation = function(v){
        return activedKey;             
    }
    launcherActivity.showPremium.implementation = function(v){
        send("Hook start...");
        var key = this.getKey();
        var mac = this.getMac();
        send("key:"+key);
        send("mac:"+mac);
        var MainActivity = Java.use('de.fraunhofer.sit.premiumapp.MainActivity');
        var xorResult = MainActivity.xor(stringToBytes(mac),stringToBytes("LICENSEKEYOK"));
        activedKey = bytesToString(xorResult);   
        send("activedKey:" + activedKey);
        this.showPremium(v);
    }

    //使点击第一个控件也能得到Flag
    launcherActivity.verifyClick.implementation = function(view){
        this.showPremium(view);
    }
}
);
"""
 
dev = frida.get_usb_device()
session = dev.attach('de.fraunhofer.sit.premiumapp')
script = session.create_script(jscode)
script.on('message',on_message)
script.load()
sys.stdin.read()