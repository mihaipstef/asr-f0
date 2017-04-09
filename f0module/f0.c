#include "f0.h"
#include <assert.h>
#include "running_stats.h"
#include "median.h"
#include "sphinxbase/yin.h"

static yin_t *yin = NULL;
static int started = 0;
static int sample_rate;
static Statistics f0_stats;

static const double VOICE_THRESH = 0.1;
static const double SEARCH_RANGE = 0.2;
static const int SMOOTH_WINDOW = 2;
static const double MAX_F0 = 350;
static const double MIN_F0 = 85;

void f0_init(size_t frame_size, int _sample_rate) {
	yin = yin_init(frame_size, VOICE_THRESH, SEARCH_RANGE, SMOOTH_WINDOW);
	median_init(frame_size);
	stats_reset();
	sample_rate = _sample_rate;
	started = 0;
	assert(yin);
}

void f0_free() {
	if (yin) {
		yin_free(yin);
	}
	median_free();
}

void f0_start() {
	yin_start(yin);
	median_reset();
	stats_reset();
	started = 1;
}

void f0_end() {
	yin_end(yin);
	started = 0;
}

void f0_process(const short *in_buf) {
	unsigned short period, bestdiff;
	double f0, voice_prob;
	if (started) {
		yin_write(yin, in_buf);
		if (yin_read(yin, &period, &bestdiff)) {
			voice_prob = bestdiff > 32768 ? 0.0 : 1.0 - (double)bestdiff / 32768;
			if (period > 0) {
				f0 = (double)sample_rate / period;
				if (f0 >= MIN_F0 && f0 <= MAX_F0) {
					stats_process(f0, &f0_stats);
					median_process(f0);
				}
			}
		}
	}
}

void f0_features(double feat[FEAT_MAX]) {
	feat[0] = median_get();
	feat[1] = f0_stats.avg;
	feat[2] = f0_stats.var;
	feat[3] = f0_stats.min;
	feat[4] = f0_stats.max;
}
