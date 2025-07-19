// Implements a dictionary's functionality
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>  

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;
int size_count = 0;
// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int index = hash(word);
    for(node *n = table[index]; n != NULL; n = n->next) {
        if(strcasecmp(n->word, word) == 0)
        return true;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // return toupper(word[0]) - 'A';
    unsigned int hash = 5381;
    int c ;
    while((c = *word++)){
    hash = hash*33 + toupper(c);
    }
    return hash % N;
}
// github - https://github.com/nikhil-partap

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    char data[LENGTH + 1];
    FILE *file = fopen(dictionary, "r");
    if (file == NULL){
        fprintf(stderr, "could not read %s\n",dictionary);
        return false;
    }
    while (fscanf(file, "%45s", data) != EOF) {

        unsigned int index = hash(data);

        node *new_node = malloc(sizeof(node));
        if(!new_node) return false;

        strcpy(new_node->word, data);

        new_node->next = table[index];
        table[index] = new_node;
        size_count ++;
    }
    fclose(file);
    return true;

}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return size_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for(int i = 0; i < N; i ++){
        node *n = table[i];
        while(n){
            node *temp = n;
            n = n->next;
            free(temp);
        }
    }
    return true;
}
