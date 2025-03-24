#include <stdio.h>
#include <wchar.h>
#include <locale.h>
#include <string.h>
#include <stdlib.h>

// Функция подсчета слов для широких символов
int count_words(const wchar_t *text) {
    int words = 0;
    int in_word = 0;
    
    for (size_t i = 0; text[i] != L'\0'; i++) {
        if (iswspace(text[i])) {
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

// Реверс строки широких символов
void reverse_wide_string(wchar_t *str) {
    size_t length = wcslen(str);
    for (size_t i = 0; i < length / 2; i++) {
        wchar_t temp = str[i];
        str[i] = str[length - i - 1];
        str[length - i - 1] = temp;
    }
}

// Меню
void show_menu() {
    wprintf(L"\n1. Анализ текста\n");
    wprintf(L"2. Выход\n");
    wprintf(L"Выберите действие: ");
}

int main() {
    // Установка локали для поддержки Unicode
    setlocale(LC_ALL, "");
    
    // Для Windows: дополнительная настройка консоли
    #ifdef _WIN32
    system("chcp 65001 > nul"); // UTF-8
    #endif

    wchar_t text[1000];
    int choice;
    
    do {
        show_menu();
        wscanf(L"%d", &choice);
        while(getwchar() != L'\n'); // Очистка буфера
        
        switch(choice) {
            case 1: {
                wprintf(L"\nВведите текст (до 999 символов):\n");
                fgetws(text, sizeof(text)/sizeof(wchar_t), stdin);
                text[wcslen(text)-1] = L'\0'; // Удаление \n
                
                // Подсчет слов
                int words = count_words(text);
                
                // Шифрование (реверс)
                wchar_t encrypted[1000];
                wcscpy(encrypted, text);
                reverse_wide_string(encrypted);
                
                // Вывод результатов
                wprintf(L"\nРезультаты:\n");
                wprintf(L"Слов: %d\n", words);
                wprintf(L"Зашифровано: %ls\n", encrypted);
                break;
            }
            case 2:
                wprintf(L"Выход...\n");
                break;
            default:
                wprintf(L"Неверный выбор!\n");
        }
    } while(choice != 2);
    
    return 0;
}