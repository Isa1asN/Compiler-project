#include <stdio.h>

int main() {
	int a = (3 + 4) * 6 / 2 - 7;
	printf("int a = (3 + 4) * 6 / 2 - 7 = %d\n", a);

	float f = 16.9 + a * 2 / 4;
	printf("float f = 16.9 + a * 2 / 4 = %f\n", f);

	char c = f + 200 / 2;
	printf("char c = f + 200 / 2 = %c\n", c);

	return a;
}
