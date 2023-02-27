#include <stdio.h>

int main() {
	// Exception will be thrown due to undeclared array size
	int a[3] = {10, 20, 30};
	printf("Value of a[2]: ");

	char b = 'b';
	float c = b * 2;

	a[2] = c;

	printf("%d\n", a[2]);

	float x[4] = {1.5, 2.5, 3.5, 4.5};
	printf("Value of x[0]: %f\n", x[0]);
	x[0] = 5.5;
	printf("Value of reassigned x[0]: %f\n", x[0]);

	return 0;
}