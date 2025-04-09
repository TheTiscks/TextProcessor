#include <stdio.h>
#include <string.h>
#include <ctype.h>  // для корректной обработки пробелов

int main() {
    char text[10000];
    fgets(text, sizeof(text), stdin);
    
    int words = 0;
    int in_word = 0;
    
    for(int i = 0; text[i]; i++) {
        if(isspace(text[i])) {
            if(in_word) {
                words++;
                in_word = 0;
            }
        } else {
            in_word = 1;
        }
    }
    
    // Последнее слово, если текст не заканчивается пробелом
    if(in_word) words++;
    
    printf("%d", words);
    return 0;
}