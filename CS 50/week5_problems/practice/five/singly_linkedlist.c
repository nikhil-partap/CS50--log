// Write a C program that:
//     Creates a singly linked list of 5 nodes.
//     Each node should store an integer value from 1 to 5.
//     Traverse and print all values in the list.
// expected output 
// 1 -> 2 -> 3 -> 4 -> 5 -> NULL


#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int data;
    struct node* next;
} node;

node* create_node(int value)
{
    node* new_node = malloc(sizeof(node));
    if(new_node == NULL)
    {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    new_node->data = value;
    new_node->next = NULL;
    return new_node;
}

void print_node(node* head)
{
    node* temp = head;
    while(temp != NULL)
    {
        printf("%d ->", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}



void insert_at_end(node **head, int value)
{
    node* new_node = create_node(value);
    if (*head == NULL) 
    {
        *head = new_node;
        return;
    }

    node* temp = *head;
    while(temp->next != NULL)
    {
        temp = temp->next;
    }
    temp->next = new_node;
}


void insert_at_beginning(node **head, int value)
{
    node *new_node = create_node (value);
     new_node->next =  *head;
    *head = new_node;
}

int search(node *head, int target)
{
    node *temp = head;
    while(temp != NULL)
    {
        if(temp->data == target)
        {
            printf("Found\n");
            return 1;
        }
        temp = temp->next;
    }
    printf("Not Found\n");
    return 0;
}

void delete_node(node **head, int value)
{
    if (*head == NULL)
    return;

    if (*head != NULL && (*head)->data == value)
    {
        node *temp = *head;
        *head =(*head)->next;
        free(temp);
        return;
    }
    node *current = *head;
    while(current->next != NULL)
    {
        if(current->next->data == value)
        {
            node *temp = current->next;
            current->next = current->next->next;
            free(temp);
            return;
        }
        current = current->next;
    }
}






int main(void)
{
    node* head = create_node(1);
    head->next = create_node(2);
    head->next->next = create_node(3);
    head->next->next->next = create_node(4);
    head->next->next->next->next = create_node(5);

    print_node(head);

    node* temp;
    while(head != NULL)
    {
        temp = head;
        head = head->next;
        free(temp);
    }
    return 0;
}
 


