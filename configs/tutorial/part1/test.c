#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ARRAY_SIZE 16 * 1024 * 1024  

int array[ARRAY_SIZE];

int main() {
    srand(time(NULL));  

    for (int i = 0; i < ARRAY_SIZE; i++) {
        array[i] = rand();  
    }

    for (int i = 0; i < ARRAY_SIZE; i++) {
        int index = rand() % ARRAY_SIZE;  
        int value = array[index];
    }

    return 0;
}