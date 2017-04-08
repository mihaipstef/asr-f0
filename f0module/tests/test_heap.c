#include "heap.h"
#include <stdio.h>

int cmp1(int a, int b) { return a >= b; }
int cmp2(int a, int b) { return a <= b; }


int main(){
	Heap heap;
	heap_init(&heap, 10, &cmp2);

	heap_push(&heap, 5.0);
	printf("%f\n",heap_root(&heap));
	heap_push(&heap, 1.0);
	printf("%f\n",heap_root(&heap));
	heap_push(&heap, 2.0);
	printf("%f\n",heap_root(&heap));
	heap_push(&heap, 6.0);
	printf("%f\n",heap_root(&heap));
	heap_pop(&heap);
	printf("%f\n",heap_root(&heap));
	heap_push(&heap, 1.0);
	printf("%f\n",heap_root(&heap));
	heap_push(&heap, 9.0);
	printf("%f\n",heap_root(&heap));

}
