#include <stdio.h>

int func(int a) {
	if (a > 3) {
		return 10;
	}
	else {
		return 5;
	}
}

int main() {

	int a = 5;
	while(a > 0) {
		printf("a = %d\n", func(a));
		a = a - 1;
	}

	return 0;
}
