#include <stdio.h>

int main() {
	char* printing = "Printing: ";
	int a = 5;

	printf(printing);
	printf("while loop\n");
	while(a > 0) {
		if(a == 5) {
			printf("\t Start of loop\n");
		}
		else if (a >= 3) {
			printf("\t First part of the loop \n");
		}
		else while(a > 0) {
			printf("\t Looping within else while\n");
			a = a - 1;
		}
		a = a - 1;
	}

	printf("\n");

	for(int b = a + 1; b <= (a + 5); b += 1) {
		printf("%s %d\n", "Running for loop, b =", b);
	}

	return 0;
}
