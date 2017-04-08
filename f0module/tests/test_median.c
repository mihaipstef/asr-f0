#include "median.h"
#include <stdio.h>

int main() {
	median_init(10);

	median_process(3.0);
	printf("%f\n",median_get());
	median_process(7.0);
	printf("%f\n",median_get());
	median_process(4.0);
	printf("%f\n",median_get());
	median_process(1.0);
	printf("%f\n",median_get());
	median_process(2.0);
	printf("%f\n",median_get());
	median_process(6.0);
	printf("%f\n",median_get());
	median_process(5.0);
	printf("%f\n",median_get());

}
