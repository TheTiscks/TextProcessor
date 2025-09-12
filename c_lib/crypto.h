#ifndef CRYPTO_H
#define CRYPTO_H

#ifdef __cplusplus
extern "C" {
#endif

// Возвращает malloc C-строку длиной length (без терминатора).
// Нужно вызвать free_key(ptr) после использования.
char* generate_key(int length);

// Освобождает память
void free_key(char* ptr);

#ifdef __cplusplus
}
#endif

#endif
