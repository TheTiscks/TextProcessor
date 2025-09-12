#include "crypto.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _WIN32
  #include <windows.h>
  #include <wincrypt.h>
#else
  #include <fcntl.h>
  #include <unistd.h>
#endif

static const char charset[] =
  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

char* generate_key(int length) {
    if (length <= 0) return NULL;
    char *out = (char*)malloc(length + 1);
    if (!out) return NULL;

    unsigned char *buf = (unsigned char*)malloc(length);
    if (!buf) { free(out); return NULL; }

#ifdef _WIN32
    HCRYPTPROV hProv = 0;
    if(!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT)) {
        srand((unsigned)time(NULL));
        for (int i = 0; i < length; ++i) out[i] = charset[rand() % (sizeof(charset)-1)];
    } else {
        if(!CryptGenRandom(hProv, (DWORD)length, buf)) {
            srand((unsigned)time(NULL));
            for (int i = 0; i < length; ++i) buf[i] = rand() % 256;
        }
        CryptReleaseContext(hProv, 0);
        for (int i = 0; i < length; ++i) out[i] = charset[buf[i] % (sizeof(charset)-1)];
    }
#else
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd >= 0) {
        ssize_t r = read(fd, buf, length);
        close(fd);
        if (r != length) {
            srand((unsigned)time(NULL));
            for (int i = 0; i < length; ++i) buf[i] = rand() % 256;
        }
    } else {
        srand((unsigned)time(NULL));
        for (int i = 0; i < length; ++i) buf[i] = rand() % 256;
    }
    for (int i = 0; i < length; ++i) out[i] = charset[buf[i] % (sizeof(charset)-1)];
#endif

    out[length] = '\0';
    free(buf);
    return out;
}

void free_key(char* ptr) {
    if (ptr) free(ptr);
}
