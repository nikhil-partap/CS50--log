#ifndef HASH_TABLE_H
#define HASH_TABLE_H

#include <stdbool.h>

// it initilise the table by malloc size according to the no of buckets
void ht_init(int bucket_count);

// inserts a node at the front of the sequence 
bool ht_insert(const char *key);

// search for element using key  
bool ht_search(const char *key);

// free all the data all nodes all tables starting from the front of linked list
void ht_free(void);


#endif 