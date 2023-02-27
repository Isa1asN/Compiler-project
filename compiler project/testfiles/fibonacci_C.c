
#include <stdio.h>

int fib(int n) {
    if (n == 0) {
        return 0;
    } else if (n == 1) {
        return 1;
    }
    int b = fib(n-1) + fib(n-2);
    return b;
}

// Main function
int main() {

    int n;
    printf("Enter the n-th Fibonacci number (0 not included): ");
    scanf("%d",&n);
    printf("The %d-th Fibonacci number is: %d", n, fib(n));

    return 0;
}
