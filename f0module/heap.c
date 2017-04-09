#include <unistd.h>
#include <stdlib.h>
#include <assert.h>

#include "heap.h"

// Init the heap struct
void heap_init(Heap *heap, size_t max_size, int (*cmp_f)(int,int))
{
	*heap = (Heap){
		.size = max_size,
		.length = 0,
		.cmp = cmp_f,
		.data = malloc(sizeof(Type) * max_size)
	};
	assert(heap->data && heap->cmp);
}

void heap_reset(Heap *heap) {
	heap->length = 0;
}

void heap_free(Heap *heap) {
	if (heap->data) {
		free(heap->data);
	}
	heap->length = 0;
}

// Inserts new element to the heap
void heap_push(Heap *heap, Type value)
{
	size_t i, parent;

	// Find out where to put the element and put it
	for(i = heap->length++; i; i = parent)
	{
		parent = (i - 1) / 2;
		if (heap->cmp(heap->data[parent],value)) break;
		heap->data[i] = heap->data[parent];
	}
	heap->data[i] = value;
}

// Removes the root
void heap_pop(Heap *heap)
{
	size_t i, swap, other;

	Type tmp = heap->data[--heap->length];

	// Reorder the elements
	for(i = 0; 1; i = swap)
	{
		// Find the child to swap with
		swap = 2*i + 1;
		if (swap >= heap->length) break; // If there are no children, the heap is reordered
		other = swap + 1;
		if ((other < heap->length) && heap->cmp(heap->data[other], heap->data[swap])) {
			 swap = other;
		}

		if (heap->cmp(tmp, heap->data[swap])) break;

		heap->data[i] = heap->data[swap];
	}
	heap->data[i] = tmp;
}
