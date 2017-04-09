#ifndef RUNNING_STATS_H
#define RUNNING_STATS_H

typedef struct Statistics {
	double max;
	double min;
	double avg;
	double var;
} Statistics;

void stats_reset();
void stats_process(double, Statistics*);

#endif
