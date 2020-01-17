let CryptoJS = require("crypto-js");

function AES(key,encrypt_key) {
    let encutf8 = CryptoJS.enc.Utf8.parse(encrypt_key);
    let iv_utf8 = CryptoJS.enc.Utf8.parse('2801003954373300');
    return CryptoJS.AES.encrypt(key, encutf8, {
        iv:iv_utf8,
        mode:CryptoJS.mode.CBC,
        padding:CryptoJS.pad.ZeroPadding
    }).toString()
}

console.log(AES("221,32:1579253970660||219,24:1579254506338",'c28725d494c78ad782a6199c341630ee'))