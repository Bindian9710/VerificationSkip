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

