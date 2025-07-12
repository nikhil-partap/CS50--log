#include<stdio.h>
#define size 100

int stack[size];
int top = -1;

void push(int data){
    if (top >= size - 1)    {
        printf("stack overflow");
        return; 
    }
    stack[++top] = data;
}

int pop(void){
    if(top < 0 ){
        printf("stack is empty");
        return -1;
    }
    return stack[top--];
}

int peek(void){
    if(top < 0){
        printf("stack is empty");
        return -1;
    }
    return stack[top];
}

int is_empty(void){
    return top == -1;
}

int main(void){
    push(1);
    push(2);
    push(3);
    
    printf("%i\n", pop());

    printf("%i\n", stack[top]);
}

