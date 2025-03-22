#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <windows.h> // Для SetConsoleCP

int count_words(const char *text) {
    int words = 0;
    int in_word = 0;
    
    for (size_t i = 0; text[i] != '\0'; i++) {
        // Явно проверяем только пробел и табуляцию
        if (text[i] == ' ' || text[i] == '\t') {
            if (in_word) {
                words++;
                in_word = 0;
            }
        } else {
            in_word = 1;
        }
    }
    
    if (in_word) words++;
    return words;
}

void reverse_string(char *str) {
    size_t length = strlen(str);
    for (size_t i = 0; i < length / 2; i++) {
        char temp = str[i];
        str[i] = str[length - i - 1];
        str[length - i - 1] = temp;
    }
}

void show_menu() {
    printf("\n1. Анализ текста\n");
    printf("2. Выход\n");
    printf("Выберите действие: ");
}

int main() {
    char text[1000];
    int choice;
    
    // Настройка кодировки для Windows
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    
    do {
        show_menu();
        if(scanf("%d", &choice) != 1) {
            while(getchar() != '\n'); // Очистка буфера
            continue;
        }
        getchar(); // Очистка '\n'
        
        switch(choice) {
            case 1: {
                printf("\nВведите текст (до 999 символов):\n");
                fgets(text, sizeof(text), stdin);
                text[strcspn(text, "\n")] = '\0';
                
                // Подсчет слов
                int words = count_words(text);
                
                // Шифрование
                char encrypted[1000];
                strcpy(encrypted, text);
                reverse_string(encrypted);
                
                printf("\nРезультаты:\n");
                printf("Слов: %d\n", words);
                printf("Зашифровано: %s\n", encrypted);
                break;
            }
            case 2:
                printf("Выход...\n");
                break;
            default:
                printf("Неверный выбор!\n");
        }
    } while(choice != 2);
    
    return 0;
}

// для работы с кириллицей комплировать как: gcc -fexec-charset=CP1251 altC.c -o altC.exe  
