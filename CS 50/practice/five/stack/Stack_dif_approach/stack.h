#ifndef STACK_H
#define STACK_H

#include<stdbool.h>

//this add a new_node to the stack and store the int(value) in new_node->data 
void push(int value);

// this free the top node and update the top to point at the next node 
bool pop(int *popped_value);

// check if the top points to NULL or if the stack is empty
bool is_empty(void);

// it free all the node in the stack starting from the top node with the help of pop function 
void free_stack (void);

// it takes a look at the data stored in the top node 
bool peek(int *top_value);

#endif // STACK_H