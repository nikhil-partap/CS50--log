// main.c

#include <stdio.h>
#include "stack.h"

int main(void) {
    push(10);
    push(20);
    push(30);

    int value;
    if (peek(&value))
        printf("Top of stack: %d\n", value);  // Should print 30

    while (pop(&value))
        printf("Popped: %d\n", value);

    if (is_empty())
        printf("Stack is now empty.\n");

    free_stack(); // Always free memory

    return 0;
}
