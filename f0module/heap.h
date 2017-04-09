#ifndef HEAP_H
#define HEAP_H

#include <stddef.h>

typedef double Type;

typedef struct Heap
{
	size_t size;
	size_t length;
	int (*cmp)(int,int);
	Type *data;
} Heap;

void heap_init(Heap *heap, size_t max_size, int (*cmp_f)(int,int));
void heap_push(Heap *heap, Type value);
void heap_pop(Heap *heap);
void heap_reset(Heap *heap);
void heap_free(Heap *heap);

static inline Type heap_root(Heap *heap) {
	return *heap->data;
}

#endif
