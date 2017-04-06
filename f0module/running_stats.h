#ifndef RUNNING_STATS_H
#define RUNNING_STATS_H

typedef struct Statistics {
	double max;
	double min;
	double avg;
	double var;
} Statistics;

void reset_stats();
void running_stats(double, Statistics*);

#endif
