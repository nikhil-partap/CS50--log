#include <stdio.h>
#include <stdlib.h>
#include "queue.h"

// node , queue, queue_create, enqueue, dequeue, is_queue_empty, queue_distroy

typedef struct node{
    int data; 
    struct node *next;    
} Node;

struct Queue{
    Node *front;
    Node *back;
};

Queue *queue_create(){
    Queue *new_queue = malloc(sizeof(Queue));
    if(!new_queue){
        fprintf(stderr, "Memory Allocation Failed\n");
        exit(EXIT_FAILURE);
    }
    new_queue->back = new_queue->front = NULL;
    return new_queue;
}

void enqueue(Queue *q, int value){
    Node *new_node = malloc(sizeof(Node));
    if(!new_node){
        fprintf(stderr, "new_node memory allocation failed");
        exit(EXIT_FAILURE);
    }
    
    new_node->data = value;
    new_node->next = NULL;
    
    if(q->back){
        q->back->next = new_node;
    }else{
        q->front = new_node;
    }
    q->back = new_node;
}

bool dequeue(Queue *q, int *dequeue_value){
    if(is_queue_empty(q)){
        return false;
    }
    Node *temp = q->front;
    *dequeue_value = temp->data;
    q->front = q->front->next;

    if(!q->front){
        q->back = NULL;
    }

    free(temp);
    return true;    
}

bool is_queue_empty(Queue *q){
    return q->front == NULL;
}

void queue_destroy(Queue *q){
    int temp;
    while(dequeue(q, &temp));
    free(q);
}
