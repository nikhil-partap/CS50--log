#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include "stack.h"
typedef struct node{
    int data;
    struct stack *next; 
} Node;
static Node *top = NULL;
// push , pop , is_empty , free_stack , peek

void push(int value){
    Node *new_node = malloc(sizeof(Node));
    if(!new_node){
        printf(stderr, "Memory allocatiion fail in push function\n");
        exit(EXIT_FAILURE);
    }
    new_node->data = value;
    new_node->next = top;
    top = new_node; 
}

bool pop(int *popped_value){
    if(is_empty())return false;

    
}




