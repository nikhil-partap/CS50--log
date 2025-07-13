#include<stdio.h>
#include<stdlib.h>
#include "stack.h"
// structure of each stack box
typedef struct node{
    int data;
    struct node *next; 
} Node;
static Node *top = NULL;
// push , pop , is_empty , free_stack , peek

void push(int value){
    Node *new_node = malloc(sizeof(Node));
    if(!new_node){
        fprintf(stderr, "Memory allocatiion fail in push function\n");
        exit(EXIT_FAILURE);
    }
    new_node->data = value;
    new_node->next = top;
    top = new_node; 
}

bool pop(int *popped_value){
    if(is_empty())return false;

    *popped_value = top->data;
    Node *temp = top;
    top = top->next;
    free(temp);
    return true;
}
bool is_empty(void){
    return !top;
}

void free_stack (void){
    while(!is_empty()){
        int temp; 
        pop(&temp);
    }
}

bool peek(int *top_value){
    if(is_empty()){
        fprintf(stderr, "The stack is already empty\n");
        return false;
    }
    *top_value = top->data;
    return true;
}


