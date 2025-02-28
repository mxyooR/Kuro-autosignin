let window = globalThis;
const JsEncrypt = function() {
    function s() {
        this["i"] = 0,
        this["j"] = 0,
        this["S"] = [];
    }
    s["prototype"]["init"] = function C(e) {
        var t, s, n;
        for (t = 0; t < 256; ++t)
            this["S"][t] = t;
        for (t = s = 0; t < 256; ++t)
            s = s + this["S"][t] + e[t % e["length"]] & 255,
            n = this["S"][t],
            this["S"][t] = this["S"][s],
            this["S"][s] = n;
        this["i"] = 0,
        this["j"] = 0;
    }
    ,
    s["prototype"]["next"] = function E() {
        var e;
        return this["i"] = this["i"] + 1 & 255,
        this["j"] = this["j"] + this["S"][this["i"]] & 255,
        e = this["S"][this["i"]],
        this["S"][this["i"]] = this["S"][this["j"]],
        this["S"][this["j"]] = e,
        this["S"][e + this["S"][this["i"]] & 255];
    }
    ;
    var n, i, r, t, o = 256;
    if (null == i) {
        var a;
        if (i = [],
        r = 0,
        window["crypto"] && window["crypto"]["getRandomValues"]) {
            var _ = new Uint32Array(256);
            for (window["crypto"]["getRandomValues"](_),
            a = 0; a < _["length"]; ++a)
                i[r++] = 255 & _[a];
        }
        var u = 0
          , c = function c(t) {
            if (256 <= (u = u || 0) || o <= r)
                window["removeEventListener"] ? (u = 0,
                window["removeEventListener"]("mousemove", c, !1)) : window["detachEvent"] && (u = 0,
                window["detachEvent"]("onmousemove", c));
            else
                try {
                    var s = t["x"] + t["y"];
                    i[r++] = 255 & s,
                    u += 1;
                } catch (e) {}
        };
        window["addEventListener"] ? window["addEventListener"]("mousemove", c, !1) : window["attachEvent"] && window["attachEvent"]("onmousemove", c);
    }
    function h() {
        if (null == n) {
            n = function t() {
                return new s();
            }();
            while (r < o) {
                var e = Math["floor"](65536 * Math["random"]());
                i[r++] = 255 & e;
            }
            for (n["init"](i),
            r = 0; r < i["length"]; ++r)
                i[r] = 0;
            r = 0;
        }
        return n["next"]();
    }
    function p() {}
    p["prototype"]["nextBytes"] = function A(e) {
        var t;
        for (t = 0; t < e["length"]; ++t)
            e[t] = h();
    }
    ;
    function b(e, t, s) {
        null != e && ("number" == typeof e ? this["fromNumber"](e, t, s) : null == t && "string" != typeof e ? this["fromString"](e, 256) : this["fromString"](e, t));
    }
    function w() {
        return new b(null);
    }
    t = false ? (b["prototype"]["am"] = function B(e, t, s, n, i, r) {
        var o = 32767 & t
          , a = t >> 15;
        while (0 <= --r) {
            var _ = 32767 & this[e]
              , u = this[e++] >> 15
              , c = a * _ + u * o;
            i = ((_ = o * _ + ((32767 & c) << 15) + s[n] + (1073741823 & i)) >>> 30) + (c >>> 15) + a * u + (i >>> 30),
            s[n++] = 1073741823 & _;
        }
        return i;
    }
    ,
    30) : false ? (b["prototype"]["am"] = function S(e, t, s, n, i, r) {
        while (0 <= --r) {
            var o = t * this[e++] + s[n] + i;
            i = Math["floor"](o / 67108864),
            s[n++] = 67108863 & o;
        }
        return i;
    }
    ,
    26) : (b["prototype"]["am"] = function D(e, t, s, n, i, r) {
        var o = 16383 & t
          , a = t >> 14;
        while (0 <= --r) {
            var _ = 16383 & this[e]
              , u = this[e++] >> 14
              , c = a * _ + u * o;
            i = ((_ = o * _ + ((16383 & c) << 14) + s[n] + i) >> 28) + (c >> 14) + a * u,
            s[n++] = 268435455 & _;
        }
        return i;
    }
    ,
    28),
    b["prototype"]["DB"] = t,
    b["prototype"]["DM"] = (1 << t) - 1,
    b["prototype"]["DV"] = 1 << t;
    b["prototype"]["FV"] = Math["pow"](2, 52),
    b["prototype"]["F1"] = 52 - t,
    b["prototype"]["F2"] = 2 * t - 52;
    var l, f, d = "0123456789abcdefghijklmnopqrstuvwxyz", g = [];
    for (l = "0"["charCodeAt"](0),
    f = 0; f <= 9; ++f)
        g[l++] = f;
    for (l = "a"["charCodeAt"](0),
    f = 10; f < 36; ++f)
        g[l++] = f;
    for (l = "A"["charCodeAt"](0),
    f = 10; f < 36; ++f)
        g[l++] = f;
    function m(e) {
        return d["charAt"](e);
    }
    function v(e) {
        var t = w();
        return t["fromInt"](e),
        t;
    }
    function y(e) {
        var t, s = 1;
        return 0 != (t = e >>> 16) && (e = t,
        s += 16),
        0 != (t = e >> 8) && (e = t,
        s += 8),
        0 != (t = e >> 4) && (e = t,
        s += 4),
        0 != (t = e >> 2) && (e = t,
        s += 2),
        0 != (t = e >> 1) && (e = t,
        s += 1),
        s;
    }
    function x(e) {
        this["m"] = e;
    }
    function k(e) {
        this["m"] = e,
        this["mp"] = e["invDigit"](),
        this["mpl"] = 32767 & this["mp"],
        this["mph"] = this["mp"] >> 15,
        this["um"] = (1 << e["DB"] - 15) - 1,
        this["mt2"] = 2 * e["t"];
    }
    function T() {
        this["n"] = null,
        this["e"] = 0,
        this["d"] = null,
        this["p"] = null,
        this["q"] = null,
        this["dmp1"] = null,
        this["dmq1"] = null,
        this["coeff"] = null;
        this["setPublic"]("00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81", "10001");
    }
    return x["prototype"]["convert"] = function z(e) {
        return e["s"] < 0 || 0 <= e["compareTo"](this["m"]) ? e["mod"](this["m"]) : e;
    }
    ,
    x["prototype"]["revert"] = function F(e) {
        return e;
    }
    ,
    x["prototype"]["reduce"] = function O(e) {
        e["divRemTo"](this["m"], null, e);
    }
    ,
    x["prototype"]["mulTo"] = function M(e, t, s) {
        e["multiplyTo"](t, s),
        this["reduce"](s);
    }
    ,
    x["prototype"]["sqrTo"] = function R(e, t) {
        e["squareTo"](t),
        this["reduce"](t);
    }
    ,
    k["prototype"]["convert"] = function I(e) {
        var t = w();
        return e["abs"]()["dlShiftTo"](this["m"]["t"], t),
        t["divRemTo"](this["m"], null, t),
        e["s"] < 0 && 0 < t["compareTo"](b["ZERO"]) && this["m"]["subTo"](t, t),
        t;
    }
    ,
    k["prototype"]["revert"] = function j(e) {
        var t = w();
        return e["copyTo"](t),
        this["reduce"](t),
        t;
    }
    ,
    k["prototype"]["reduce"] = function P(e) {
        while (e["t"] <= this["mt2"])
            e[e["t"]++] = 0;
        for (var t = 0; t < this["m"]["t"]; ++t) {
            var s = 32767 & e[t]
              , n = s * this["mpl"] + ((s * this["mph"] + (e[t] >> 15) * this["mpl"] & this["um"]) << 15) & e["DM"];
            e[s = t + this["m"]["t"]] += this["m"]["am"](0, n, e, t, 0, this["m"]["t"]);
            while (e[s] >= e["DV"])
                e[s] -= e["DV"],
                e[++s]++;
        }
        e["clamp"](),
        e["drShiftTo"](this["m"]["t"], e),
        0 <= e["compareTo"](this["m"]) && e["subTo"](this["m"], e);
    }
    ,
    k["prototype"]["mulTo"] = function N(e, t, s) {
        e["multiplyTo"](t, s),
        this["reduce"](s);
    }
    ,
    k["prototype"]["sqrTo"] = function q(e, t) {
        e["squareTo"](t),
        this["reduce"](t);
    }
    ,
    b["prototype"]["copyTo"] = function L(e) {
        for (var t = this["t"] - 1; 0 <= t; --t)
            e[t] = this[t];
        e["t"] = this["t"],
        e["s"] = this["s"];
    }
    ,
    b["prototype"]["fromInt"] = function H(e) {
        this["t"] = 1,
        this["s"] = e < 0 ? -1 : 0,
        0 < e ? this[0] = e : e < -1 ? this[0] = e + this["DV"] : this["t"] = 0;
    }
    ,
    b["prototype"]["fromString"] = function $(e, t) {
        var s;
        if (16 == t)
            s = 4;
        else if (8 == t)
            s = 3;
        else if (256 == t)
            s = 8;
        else if (2 == t)
            s = 1;
        else if (32 == t)
            s = 5;
        else {
            if (4 != t)
                return void this["fromRadix"](e, t);
            s = 2;
        }
        this["t"] = 0,
        this["s"] = 0;
        var n, i, r = e["length"], o = !1, a = 0;
        while (0 <= --r) {
            var _ = 8 == s ? 255 & e[r] : (n = r,
            null == (i = g[e["charCodeAt"](n)]) ? -1 : i);
            _ < 0 ? "-" == e["charAt"](r) && (o = !0) : (o = !1,
            0 == a ? this[this["t"]++] = _ : a + s > this["DB"] ? (this[this["t"] - 1] |= (_ & (1 << this["DB"] - a) - 1) << a,
            this[this["t"]++] = _ >> this["DB"] - a) : this[this["t"] - 1] |= _ << a,
            (a += s) >= this["DB"] && (a -= this["DB"]));
        }
        8 == s && 0 != (128 & e[0]) && (this["s"] = -1,
        0 < a && (this[this["t"] - 1] |= (1 << this["DB"] - a) - 1 << a)),
        this["clamp"](),
        o && b["ZERO"]["subTo"](this, this);
    }
    ,
    b["prototype"]["clamp"] = function V() {
        var e = this["s"] & this["DM"];
        while (0 < this["t"] && this[this["t"] - 1] == e)
            --this["t"];
    }
    ,
    b["prototype"]["dlShiftTo"] = function U(e, t) {
        var s;
        for (s = this["t"] - 1; 0 <= s; --s)
            t[s + e] = this[s];
        for (s = e - 1; 0 <= s; --s)
            t[s] = 0;
        t["t"] = this["t"] + e,
        t["s"] = this["s"];
    }
    ,
    b["prototype"]["drShiftTo"] = function X(e, t) {
        for (var s = e; s < this["t"]; ++s)
            t[s - e] = this[s];
        t["t"] = Math["max"](this["t"] - e, 0),
        t["s"] = this["s"];
    }
    ,
    b["prototype"]["lShiftTo"] = function G(e, t) {
        var s, n = e % this["DB"], i = this["DB"] - n, r = (1 << i) - 1, o = Math["floor"](e / this["DB"]), a = this["s"] << n & this["DM"];
        for (s = this["t"] - 1; 0 <= s; --s)
            t[s + o + 1] = this[s] >> i | a,
            a = (this[s] & r) << n;
        for (s = o - 1; 0 <= s; --s)
            t[s] = 0;
        t[o] = a,
        t["t"] = this["t"] + o + 1,
        t["s"] = this["s"],
        t["clamp"]();
    }
    ,
    b["prototype"]["rShiftTo"] = function W(e, t) {
        t["s"] = this["s"];
        var s = Math["floor"](e / this["DB"]);
        if (s >= this["t"])
            t["t"] = 0;
        else {
            var n = e % this["DB"]
              , i = this["DB"] - n
              , r = (1 << n) - 1;
            t[0] = this[s] >> n;
            for (var o = s + 1; o < this["t"]; ++o)
                t[o - s - 1] |= (this[o] & r) << i,
                t[o - s] = this[o] >> n;
            0 < n && (t[this["t"] - s - 1] |= (this["s"] & r) << i),
            t["t"] = this["t"] - s,
            t["clamp"]();
        }
    }
    ,
    b["prototype"]["subTo"] = function Z(e, t) {
        var s = 0
          , n = 0
          , i = Math["min"](e["t"], this["t"]);
        while (s < i)
            n += this[s] - e[s],
            t[s++] = n & this["DM"],
            n >>= this["DB"];
        if (e["t"] < this["t"]) {
            n -= e["s"];
            while (s < this["t"])
                n += this[s],
                t[s++] = n & this["DM"],
                n >>= this["DB"];
            n += this["s"];
        } else {
            n += this["s"];
            while (s < e["t"])
                n -= e[s],
                t[s++] = n & this["DM"],
                n >>= this["DB"];
            n -= e["s"];
        }
        t["s"] = n < 0 ? -1 : 0,
        n < -1 ? t[s++] = this["DV"] + n : 0 < n && (t[s++] = n),
        t["t"] = s,
        t["clamp"]();
    }
    ,
    b["prototype"]["multiplyTo"] = function Y(e, t) {
        var s = this["abs"]()
          , n = e["abs"]()
          , i = s["t"];
        t["t"] = i + n["t"];
        while (0 <= --i)
            t[i] = 0;
        for (i = 0; i < n["t"]; ++i)
            t[i + s["t"]] = s["am"](0, n[i], t, i, 0, s["t"]);
        t["s"] = 0,
        t["clamp"](),
        this["s"] != e["s"] && b["ZERO"]["subTo"](t, t);
    }
    ,
    b["prototype"]["squareTo"] = function K(e) {
        var t = this["abs"]()
          , s = e["t"] = 2 * t["t"];
        while (0 <= --s)
            e[s] = 0;
        for (s = 0; s < t["t"] - 1; ++s) {
            var n = t["am"](s, t[s], e, 2 * s, 0, 1);
            (e[s + t["t"]] += t["am"](s + 1, 2 * t[s], e, 2 * s + 1, n, t["t"] - s - 1)) >= t["DV"] && (e[s + t["t"]] -= t["DV"],
            e[s + t["t"] + 1] = 1);
        }
        0 < e["t"] && (e[e["t"] - 1] += t["am"](s, t[s], e, 2 * s, 0, 1)),
        e["s"] = 0,
        e["clamp"]();
    }
    ,
    b["prototype"]["divRemTo"] = function Q(e, t, s) {
        var n = e["abs"]();
        if (!(n["t"] <= 0)) {
            var i = this["abs"]();
            if (i["t"] < n["t"])
                return null != t && t["fromInt"](0),
                void (null != s && this["copyTo"](s));
            null == s && (s = w());
            var r = w()
              , o = this["s"]
              , a = e["s"]
              , _ = this["DB"] - y(n[n["t"] - 1]);
            0 < _ ? (n["lShiftTo"](_, r),
            i["lShiftTo"](_, s)) : (n["copyTo"](r),
            i["copyTo"](s));
            var u = r["t"]
              , c = r[u - 1];
            if (0 != c) {
                var h = c * (1 << this["F1"]) + (1 < u ? r[u - 2] >> this["F2"] : 0)
                  , p = this["FV"] / h
                  , l = (1 << this["F1"]) / h
                  , f = 1 << this["F2"]
                  , d = s["t"]
                  , g = d - u
                  , m = null == t ? w() : t;
                r["dlShiftTo"](g, m),
                0 <= s["compareTo"](m) && (s[s["t"]++] = 1,
                s["subTo"](m, s)),
                b["ONE"]["dlShiftTo"](u, m),
                m["subTo"](r, r);
                while (r["t"] < u)
                    r[r["t"]++] = 0;
                while (0 <= --g) {
                    var v = s[--d] == c ? this["DM"] : Math["floor"](s[d] * p + (s[d - 1] + f) * l);
                    if ((s[d] += r["am"](0, v, s, g, 0, u)) < v) {
                        r["dlShiftTo"](g, m),
                        s["subTo"](m, s);
                        while (s[d] < --v)
                            s["subTo"](m, s);
                    }
                }
                null != t && (s["drShiftTo"](u, t),
                o != a && b["ZERO"]["subTo"](t, t)),
                s["t"] = u,
                s["clamp"](),
                0 < _ && s["rShiftTo"](_, s),
                o < 0 && b["ZERO"]["subTo"](s, s);
            }
        }
    }
    ,
    b["prototype"]["invDigit"] = function J() {
        if (this["t"] < 1)
            return 0;
        var e = this[0];
        if (0 == (1 & e))
            return 0;
        var t = 3 & e;
        return 0 < (t = (t = (t = (t = t * (2 - (15 & e) * t) & 15) * (2 - (255 & e) * t) & 255) * (2 - ((65535 & e) * t & 65535)) & 65535) * (2 - e * t % this["DV"]) % this["DV"]) ? this["DV"] - t : -t;
    }
    ,
    b["prototype"]["isEven"] = function ee() {
        return 0 == (0 < this["t"] ? 1 & this[0] : this["s"]);
    }
    ,
    b["prototype"]["exp"] = function te(e, t) {
        if (4294967295 < e || e < 1)
            return b["ONE"];
        var s = w()
          , n = w()
          , i = t["convert"](this)
          , r = y(e) - 1;
        i["copyTo"](s);
        while (0 <= --r)
            if (t["sqrTo"](s, n),
            0 < (e & 1 << r))
                t["mulTo"](n, i, s);
            else {
                var o = s;
                s = n,
                n = o;
            }
        return t["revert"](s);
    }
    ,
    b["prototype"]["toString"] = function se(e) {
        if (this["s"] < 0)
            return "-" + this["negate"]()["toString"](e);
        var t;
        if (16 == e)
            t = 4;
        else if (8 == e)
            t = 3;
        else if (2 == e)
            t = 1;
        else if (32 == e)
            t = 5;
        else {
            if (4 != e)
                return this["toRadix"](e);
            t = 2;
        }
        var s, n = (1 << t) - 1, i = !1, r = "", o = this["t"], a = this["DB"] - o * this["DB"] % t;
        if (0 < o--) {
            a < this["DB"] && 0 < (s = this[o] >> a) && (i = !0,
            r = m(s));
            while (0 <= o)
                a < t ? (s = (this[o] & (1 << a) - 1) << t - a,
                s |= this[--o] >> (a += this["DB"] - t)) : (s = this[o] >> (a -= t) & n,
                a <= 0 && (a += this["DB"],
                --o)),
                0 < s && (i = !0),
                i && (r += m(s));
        }
        return i ? r : "0";
    }
    ,
    b["prototype"]["negate"] = function ne() {
        var e = w();
        return b["ZERO"]["subTo"](this, e),
        e;
    }
    ,
    b["prototype"]["abs"] = function ie() {
        return this["s"] < 0 ? this["negate"]() : this;
    }
    ,
    b["prototype"]["compareTo"] = function re(e) {
        var t = this["s"] - e["s"];
        if (0 != t)
            return t;
        var s = this["t"];
        if (0 != (t = s - e["t"]))
            return this["s"] < 0 ? -t : t;
        while (0 <= --s)
            if (0 != (t = this[s] - e[s]))
                return t;
        return 0;
    }
    ,
    b["prototype"]["bitLength"] = function oe() {
        return this["t"] <= 0 ? 0 : this["DB"] * (this["t"] - 1) + y(this[this["t"] - 1] ^ this["s"] & this["DM"]);
    }
    ,
    b["prototype"]["mod"] = function ae(e) {
        var t = w();
        return this["abs"]()["divRemTo"](e, null, t),
        this["s"] < 0 && 0 < t["compareTo"](b["ZERO"]) && e["subTo"](t, t),
        t;
    }
    ,
    b["prototype"]["modPowInt"] = function $_CEf(e, t) {
        var s;
        return s = e < 256 || t["isEven"]() ? new x(t) : new k(t),
        this["exp"](e, s);
    }
    ,
    b["ZERO"] = v(0),
    b["ONE"] = v(1),
    T["prototype"]["doPublic"] = function ue(e) {
        return e["modPowInt"](this["e"], this["n"]);
    }
    ,
    T["prototype"]["setPublic"] = function ce(e, t) {
        null != e && null != t && 0 < e["length"] && 0 < t["length"] ? (this["n"] = function s(e, t) {
            return new b(e,t);
        }(e, 16),
        this["e"] = parseInt(t, 16)) : console && console["error"] && console["error"]("Invalid RSA public key");
    }
    ,
    T["prototype"]["encrypt"] = function he(e) {
        var t = function a(e, t) {
            if (t < e["length"] + 11)
                return console && console["error"] && console["error"]("Message too long for RSA"),
                null;
            var s = []
              , n = e["length"] - 1;
            while (0 <= n && 0 < t) {
                var i = e["charCodeAt"](n--);
                i < 128 ? s[--t] = i : 127 < i && i < 2048 ? (s[--t] = 63 & i | 128,
                s[--t] = i >> 6 | 192) : (s[--t] = 63 & i | 128,
                s[--t] = i >> 6 & 63 | 128,
                s[--t] = i >> 12 | 224);
            }
            s[--t] = 0;
            var r = new p()
              , o = [];
            while (2 < t) {
                o[0] = 0;
                while (0 == o[0])
                    r["nextBytes"](o);
                s[--t] = o[0];
            }
            return s[--t] = 2,
            s[--t] = 0,
            new b(s);
        }(e, this["n"]["bitLength"]() + 7 >> 3);
        if (null == t)
            return null;
        var s = this["doPublic"](t);
        if (null == s)
            return null;
        var n = s["toString"](16);
        return 0 == (1 & n["length"]) ? n : "0" + n;
    }
    ,
    T;
}();

module.exports = {
    JsEncrypt
}
