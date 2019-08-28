var _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
, _p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O";

function e1(e) {
  if (null == e)
      return null;
  for (var t, n, r, o, i, a, s, u = "", c = 0; c < e.length; )
      o = (t = e.charCodeAt(c++)) >> 2,
      i = (3 & t) << 4 | (n = e.charCodeAt(c++)) >> 4,
      a = (15 & n) << 2 | (r = e.charCodeAt(c++)) >> 6,
      s = 63 & r,
      isNaN(n) ? a = s = 64 : isNaN(r) && (s = 64),
      u = u + _keyStr.charAt(o) + _keyStr.charAt(i) + _keyStr.charAt(a) + _keyStr.charAt(s);
  return u
}
function e2(e) {
  if (null == (e = _u_e(e)))
      return null;
  for (var t = "", n = 0; n < e.length; n++) {
      var r = _p.charCodeAt(n % _p.length);
      t += String.fromCharCode(e.charCodeAt(n) ^ r)
  }
  return t
}
function sig(e) {
  return md5(e + _p).toUpperCase()
}
function d1(e) {
    var t, n, r, o, i, a, s = "", u = 0;
    for (e = e.replace(/[^A-Za-z0-9\+\/\=]/g, ""); u < e.length; )
        t = _keyStr.indexOf(e.charAt(u++)) << 2 | (o = _keyStr.indexOf(e.charAt(u++))) >> 4,
            n = (15 & o) << 4 | (i = _keyStr.indexOf(e.charAt(u++))) >> 2,
            r = (3 & i) << 6 | (a = _keyStr.indexOf(e.charAt(u++))),
            s += String.fromCharCode(t),
        64 != i && (s += String.fromCharCode(n)),
        64 != a && (s += String.fromCharCode(r));
    return s
}
function _u_e(e) {
  if (null == e)
      return null;
  e = e.replace(/\r\n/g, "\n");
  for (var t = "", n = 0; n < e.length; n++) {
      var r = e.charCodeAt(n);
      r < 128 ? t += String.fromCharCode(r) : r > 127 && r < 2048 ? (t += String.fromCharCode(r >> 6 | 192),
      t += String.fromCharCode(63 & r | 128)) : (t += String.fromCharCode(r >> 12 | 224),
      t += String.fromCharCode(r >> 6 & 63 | 128),
      t += String.fromCharCode(63 & r | 128))
  }
  return t
}
function _u_d(e) {
  for (var t = "", n = 0, r = 0, o = 0, i = 0; n < e.length; )
      (r = e.charCodeAt(n)) < 128 ? (t += String.fromCharCode(r),
      n++) : r > 191 && r < 224 ? (o = e.charCodeAt(n + 1),
      t += String.fromCharCode((31 & r) << 6 | 63 & o),
      n += 2) : (o = e.charCodeAt(n + 1),
      i = e.charCodeAt(n + 2),
      t += String.fromCharCode((15 & r) << 12 | (63 & o) << 6 | 63 & i),
      n += 3);
  return t
}
function d2(e) {
  for (var t = "", n = 0; n < e.length; n++) {
      var r = _p.charCodeAt(n % _p.length);
      t += String.fromCharCode(e.charCodeAt(n) ^ r)
  }
  return t = _u_d(t)
}

function encrypt(c) {
    var l = JSON.parse(c);
    var f = e1(e2(JSON.stringify(l.payload)));
    //  , p = sig(f), md5(f + _p).toUpperCase() 请求参数里sig，在python中实现
    return f;
}
function decrypt(s) {
    var d = d1(s), 
    m = d2(d), 
    v = JSON.parse(m);
    return m;
}
