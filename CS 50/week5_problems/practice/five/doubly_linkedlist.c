#include <stdio.h>
#include <stdlib.h>

// 1 2 45 3 1
// delete 3
// add 5 at end and add 9 at beginnnig



typedef struct node
{
    int data;
    struct node* prev;
    struct node* next;
} node;

node* create_node (int value)
{
    node* new_node = malloc(sizeof(node));
    if(new_node == NULL)
    {
        printf("Memory Allocation Failed\n");
        return NULL;
    }

    new_node->data = value;
    new_node->next = NULL;
    new_node->prev = NULL;
    return new_node;
}

void delete_node(node **head, int value)
{
    if (head == NULL)
    {
        return;
    }
    
    node *current = *head;
    while(current != NULL)
    {
        if (current->data == value)
        {
            if ( current->next == NULL)
            {
                node *temp = current;
                current->prev->next = NULL;
                free(temp);
                return;
            }
            else if (current->prev == NULL)
            {
                node *temp = current;
                *head = current->next;
                if (*head != NULL)
                (*head)->prev = NULL;
                free(temp);
                return;
            }
            else
            {
                node *temp = current;
                current->prev->next = current->next;
                free(temp);
                return;
            }
        }
        current = current->next;
    }
}

void insert_at_beginnnig (node **head, int value )
{
    node *new_node = create_node(value);
    new_node->next = *head; 

    if(*head != NULL)
    {
    (*head)->prev = new_node;
    }
    *head = new_node;
}

void insert_at_end (node **head, int value)
{
    node *new_node = create_node(value);
    if(*head == NULL)
    {
        *head = new_node;
        return;

    }
    node *temp = *head;

    while( temp->next != NULL)
    {
        temp = temp->next;
    }    
    
    temp->next = new_node;
    new_node->prev = temp;    
}

int main (void)
{
    node *head = NULL;

    insert_at_end(&head, 1);
    insert_at_end(&head, 2);
    insert_at_end(&head, 45);
    insert_at_end(&head, 3);
    insert_at_end(&head, 1);

    delete_node(&head, 3);
    insert_at_end(&head, 5);
    insert_at_beginnnig(&head, 9);

    node* temp = head;
    while ( temp != NULL)
    {
        printf("%d ->", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");

}