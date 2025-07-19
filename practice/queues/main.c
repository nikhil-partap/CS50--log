#include <stdio.h>
#include "queue.h"


int main() {
    Queue *q = queue_create();

    enqueue(q, 10);
    enqueue(q, 20);
    enqueue(q, 30);

    int value;
    while (dequeue(q, &value)) {
        printf("Dequeued: %d\n", value);
    }

    queue_destroy(q);
    return 0;
}