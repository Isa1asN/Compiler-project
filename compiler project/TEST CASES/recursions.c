#include <stdio.h>

//function that adds consecutive integers recursively

int sum(int n) {
    if (n != 0){
        // sum() function calls itself
        return n + sum(n-1); }
    else {
        return n;}
}



int main(){
	printf(sum(3));
	return 0;
}
