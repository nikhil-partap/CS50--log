#ifndef QUEUE_H
#define QUEUE_H

#include <stdbool.h>

// Node definition (hidden from user)
typedef struct Queue Queue;

Queue *queue_create();
void    enqueue(Queue *q, int data);
bool    dequeue(Queue *q, int *out_data);
bool    is_queue_empty(Queue *q);
void    queue_destroy(Queue *q);

#endif