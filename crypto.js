export function bufToBase64(buf) {
  return btoa(String.fromCharCode(...new Uint8Array(buf)));
}
export function base64ToBuf(b64) {
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return arr.buffer;
}
export function strToBuf(s) {
  return new TextEncoder().encode(s);
}
export function bufToStr(buf) {
  return new TextDecoder().decode(buf);
}

// --- KDF ---
export async function deriveKeyPBKDF2(password, saltBuf, iterations = 200000, keyLen = 256) {
  const baseKey = await crypto.subtle.importKey(
    "raw", strToBuf(password), "PBKDF2", false, ["deriveKey"]
  );
  return await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt: saltBuf, iterations, hash: "SHA-256" },
    baseKey,
    { name: "AES-GCM", length: keyLen },
    true,
    ["encrypt", "decrypt"]
  );
}

// --- Encrypt ---
export async function encryptText(plainText, password) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const key = await deriveKeyPBKDF2(password, salt, 200000, 256);
  const cipherBuf = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    strToBuf(plainText)
  );
  return {
    v: 1,
    kdf: "PBKDF2",
    hash: "SHA-256",
    iterations: 200000,
    algo: "AES-GCM",
    salt: bufToBase64(salt.buffer),
    iv: bufToBase64(iv.buffer),
    cipher: bufToBase64(cipherBuf)
  };
}

// --- Decrypt ---
export async function decryptBlob(blobObj, password) {
  const saltBuf = base64ToBuf(blobObj.salt);
  const ivBuf = base64ToBuf(blobObj.iv);
  const cipherBuf = base64ToBuf(blobObj.cipher);
  const key = await deriveKeyPBKDF2(password, saltBuf, blobObj.iterations || 200000, 256);
  const plainBuf = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: new Uint8Array(ivBuf) },
    key,
    cipherBuf
  );
  return bufToStr(plainBuf);
}

// --- Упаковка ---
export function packBlob(obj) {
  return btoa(unescape(encodeURIComponent(JSON.stringify(obj))));
}
export function unpackBlob(packedStr) {
  return JSON.parse(decodeURIComponent(escape(atob(packedStr))));
}
