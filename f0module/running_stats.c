#include "running_stats.h"

#include <limits.h>
#include <float.h>

static double average = 0.0;
static double variance = 0.0;
static double maxim = 0.0;
static double minim = DBL_MAX;
static unsigned int nsamples = 0;

void stats_reset() {
	average = 0.0;
	variance = 0.0;
	maxim = 0.0;
	minim = DBL_MAX;
	nsamples = 0;
}

void stats_process(double value, Statistics *stats) {
	double d;
	if (nsamples < UINT_MAX) {
		++nsamples;
		average += (value - average) / nsamples;
		d = value - average;
		variance += d * d;
		if (nsamples>=2) {
			stats->avg = average;
			stats->var = variance/(nsamples-1);
		}
	}
	if (value > maxim) {
		maxim = value;
	}
	if (value < minim) {
		minim = value;
	}
	stats->max = maxim;
	stats->min = minim;
}
