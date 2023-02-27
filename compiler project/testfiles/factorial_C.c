#include <stdio.h>

int factorial(int n)
{
    if(n == 0) {
   		return +1;
   	}
    else {
		return (n * factorial(n - 1));
    }
}

int main()
{
	int n;
	printf("Enter a number for the factorial function: ");
	scanf("%d",&n);
	printf("\n");
	printf("The factorial of %d is: %d", n, factorial(n));
	return 0;
}