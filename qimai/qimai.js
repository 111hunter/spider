function X(t, e, n, i) {
    for (var r = 0; r < i && !(r + n >= e.length || r >= t.length); ++r)
        e[r + n] = t[r];
    return r
}

function G(t) {
    for (var e = [], n = 0; n < t.length; ++n)
        e.push(255 & t.charCodeAt(n));
    return e
}

function t_write(t,e,b,i){
    return X(G(e), t, 0, i);
}

function e_from(t_str,b){
    var i = t_str.length;
    t = new Uint8Array(i);
    var r = t_write(t,t_str,b,i)
    return t = t.slice(0,r),t
}

function n_fun(t) {
    var n;
    return n = e_from(t.toString(), "binary"),
    q_fromB(n)
}

function v(n) {
    return n_fun(encodeURIComponent(n)["replace"](/%([0-9A-F]{2})/g, function(a, n) {
        return m("0x" + n)
    }))
}

function m(n){
    var t="fromCharCode"
    return String[t](n)
}

function k(a, n) {
    a = a["split"]("");
    for (var t = a["length"], e = n["length"], r = "charCodeAt", i = 0; i < t; i++)
        a[i] = m(a[i][r](0) ^ n[(i + 10) % e][r](0));
    return a["join"]("")
}

u = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9,+,/"
u = u.split(",")

function a(t) {
    return u[t >> 18 & 63] + u[t >> 12 & 63] + u[t >> 6 & 63] + u[63 & t]
}

function s(t, e, n) {
    for (var i, r = [], o = e; o < n; o += 3)
        i = (t[o] << 16 & 16711680) + (t[o + 1] << 8 & 65280) + (255 & t[o + 2]),
        r.push(a(i));
    return r.join("")
}

function q_fromB(t) {
    for (var e, n = t.length, i = n % 3, r = "", o = [], a = 16383, l = 0, c = n - i; l < c; l += a)
        o.push(s(t, l, l + a > c ? c : l + a));
    return 1 === i ? (e = t[n - 1],
    r += u[e >> 2],
    r += u[e << 4 & 63],
    r += "==") : 2 === i && (e = (t[n - 2] << 8) + t[n - 1],
    r += u[e >> 10],
    r += u[e >> 4 & 63],
    r += u[e << 2 & 63],
    r += "="),
    o.push(r),
    o.join("")
}

function get_analysis(synct, params) {

    // 生成时间戳
    console.log(synct);
    var g = new Date() - 1000 * synct; //参数g的生成,应该是cookies中的syncd,这里不会检测e
    var e = new Date() - g - 1515125653845;
    console.log(e);
    var analy = [];
    var palist = [];

    for (var key in params) {
        palist.push(params[key])
    }

    var mm = palist["sort"]()["join"]("");
    var mmm = v(mm);

    var m_str0 = mmm + "@#/rank/indexPlus/brand_id/0@#" + e + "@#0";
    var m_str1 = mmm + "@#/rank/indexPlus/brand_id/1@#" + e + "@#1";
    var m_str2 = mmm + "@#/rank/indexPlus/brand_id/2@#" + e + "@#2";
    var b_str = "00000008d78d46a";
    var r0 = v(k(m_str0, b_str));
    var r1 = v(k(m_str1, b_str));
    var r2 = v(k(m_str2, b_str));
    analy.push(r0, r1, r2);
    return analy
}


