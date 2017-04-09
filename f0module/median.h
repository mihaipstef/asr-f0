#ifndef MEDIAN_H
#define MEDIAN_H

#include <stddef.h>

void median_init(size_t window_size);

void median_reset();

void median_free();

void median_process(double val);

double median_get();

#endif
