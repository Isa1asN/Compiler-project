#include <stdio.h>

int main() {
	// Pointer type declarations and assignments 

	char char_array[1];

	int a = 8;
	int c = a + 3;

	printf("%s", "Enter a character: ");
	scanf("%c", &char_array[0]);

	a = c + a * char_array[0];

	printf("\n%d\n", a);

	char q = 'c';
	char* p_q = &q;
	float f = 3.1;
	char d_p_q = *p_q;
	int f_c_i = d_p_q + f;
	
	printf("%d\n", f_c_i);

	return 0;
}
