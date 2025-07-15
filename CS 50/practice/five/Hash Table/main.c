// main.c

#include <stdio.h>
#include "hash_table.h"

int main(void) {
    ht_init(50); // Start with 50 buckets

    ht_insert("apple");
    ht_insert("banana");
    ht_insert("orange");

    printf("banana? %s\n", ht_search("banana") ? "yes" : "no");
    printf("grape? %s\n", ht_search("grape") ? "yes" : "no");

    ht_free();
    return 0;
}
