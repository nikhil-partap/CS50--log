#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hash_table.h"
// hash, ht_init, ht_insert, ht_search, ht_free

typedef struct node{
    char *key;
    struct node *next;    
} node;

static node **table = NULL;
static int buckets = 0;

static unsigned hash(const char *key){
    unsigned int hash = 5381;
    
    int c;
    while((c = *key++)){
    hash = hash*33 + c;
    return hash % buckets;
    }
}

void ht_init (int buckets_count){
    buckets = buckets_count;
    table = calloc(buckets, sizeof(node *));

    if(!table){
        fprintf(stderr, "hashtable memory allocaton failed");
        exit(EXIT_FAILURE);
    }
}

bool ht_insert (const char *key){
    unsigned int index = hash(key);

    for(node *n = table[index]; n !=NULL; n = n->next){
        if (strcmp(n->key, key) == 0)
        return false;
    }
    node *new_node = malloc(sizeof(node));
    if(!new_node) return false;

    new_node->key = strdup(key);
    if(!new_node->key){
        free(new_node);
        return false;
    }
    new_node->next = table[index];
    table[index] = new_node;
    return true;
}

bool ht_search(const char *key){
    unsigned int index = hash(key);
    for(node *n = table[index]; n != NULL; n = n->next) {
        if(strcmp(n->key, key) == 0)
        return true;
    }
    return false;
}

void ht_free(void){
    for(int i = 0; i < buckets; ++i){
        node *n = table[i];
        while (n){
            node *temp = n;
            n = n->next;
            free(temp->key);
            free(temp);
        }
    }

    free(table);
    table = NULL;
    buckets = 0;
}