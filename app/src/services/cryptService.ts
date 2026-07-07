import { hkdf } from "noble-hashes/lib/hkdf";
import { sha256 } from "noble-hashes/lib/sha256";
import { toUint8Array } from "js-base64";

import "react-native-get-random-values";
import nacl from "tweetnacl";

class CryptService{
    private encoder;

    constructor(){
        this.encoder = new TextEncoder();
    }

    cryptMessage(text:string, nonce:Uint8Array, messageKey:Uint8Array){
        const encodedMessage = this.encoder.encode(text);
        return nacl.secretbox(encodedMessage, nonce, messageKey);
    }

    cryptMediaMessage(data:Uint8Array, nonce:Uint8Array, messageKey:Uint8Array){
        return nacl.secretbox(data, nonce, messageKey);
    }

    decryptMessage(message:Uint8Array, nonce:Uint8Array, messageKey:Uint8Array){
        const decryptedMessage = nacl.secretbox.open(message, nonce, messageKey);
        return decryptedMessage;
    }

    sharedKey(publicKey:Uint8Array, privateKey:Uint8Array): Uint8Array{
        return nacl.box.before(publicKey, privateKey);
    }

    KDF(key:Uint8Array, info:any) {
        return hkdf(sha256, key, "", info, 32);
    }
}

export const cryptService = new CryptService();