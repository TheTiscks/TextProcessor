#include <stdio.h>
#include <string.h>

int main() {
    char text[10000];
    fgets(text, sizeof(text), stdin);
    int words = 0;
    for (int i = 0; text[i]; i++) {
        if (text[i] == ' ' || text[i] == '\n') words++;
    }
    printf("%d", words);
    return 0;
}