#ifndef F0_H
#define F0_H

#include <stddef.h>

#define FEAT_MAX 5

void f0_init(size_t frame_size, int _sample_rate);
void f0_free();
void f0_start();
void f0_end();
void f0_process(const short *in_buf);
void f0_features(double feat[FEAT_MAX]);

#endif
