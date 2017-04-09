#include "median.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "heap.h"

static Heap low_heap;
static Heap high_heap;
static size_t count;
static double current_median;

static int cmp_less_than(int a, int b) { return a <= b; }
static int cmp_higher_than(int a, int b) { return a >= b; }

static double compute_current_median() {
	if (count == 1) {
		current_median = heap_root(&low_heap);
	} else if (count == 2) {
		current_median = (heap_root(&low_heap) + heap_root(&high_heap)) / 2;
	} else {
		if (low_heap.length == high_heap.length) {
			current_median = (heap_root(&low_heap) + heap_root(&high_heap)) / 2;
		} else if (low_heap.length > high_heap.length) {
			current_median = heap_root(&low_heap);
		} else {
			current_median = heap_root(&high_heap);
		}
	}
	return current_median;
}

void median_init(size_t window_size) {
	heap_init(&low_heap, 1+window_size/2, &cmp_higher_than);
	heap_init(&high_heap, 1+window_size/2, &cmp_less_than);
	count = 0;
	current_median = 0.0;
}

void median_reset() {
	heap_reset(&low_heap);
	heap_reset(&high_heap);
	count = 0;
	current_median = 0.0;
}

void median_free() {
	heap_free(&low_heap);
	heap_free(&high_heap);
	count = 0;
	current_median = 0.0;
}

void median_process(double val) {
	double root;
	if (count == 0) {
		heap_push(&low_heap, val);
		++count;
	} else if (count == 1) {
		heap_push(&high_heap, val);
		++count;
		if (val < heap_root(&low_heap)) {
			Heap tmp = low_heap;
			low_heap = high_heap;
			high_heap = tmp;
		}
	} else {
		if (val <= current_median) {
			heap_push(&low_heap, val);
		} else {
			heap_push(&high_heap, val);
		}
		++count;
		if (low_heap.length > high_heap.length + 1) {
			root = heap_root(&low_heap);
			heap_push(&high_heap, root);
			heap_pop(&low_heap);
		} else if (high_heap.length > low_heap.length + 1) {
			root = heap_root(&high_heap);
			heap_push(&low_heap, root);
			heap_pop(&high_heap);
		}
	}
	compute_current_median();
}

double median_get() {
	return current_median;
}
