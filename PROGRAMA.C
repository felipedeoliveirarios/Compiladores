#include<stdio.h>
#include<stdbool.h>

typedef int inteiro;
typedef float real;
typedef char lit[128];

int main(){
lit A;
inteiro B;
inteiro D;
real C;



printf("%s", "Digite B");
scanf("%d", &B);
printf("%s", "Digite A:");
scanf("%s", &A);
bool T0 = 2 > B;
if( T0){
bool T1 = 4 <= B;
if( T1){
printf("%s", "B esta entre 2 e 4");
}
}
float T3 = 1 + B;
B = T3;
bool T2 = 2 > B;
while (T2){
}
float T4 = 1 + B;
B = T4;
float T5 = 2 + B;
B = T5;
float T6 = 3 + B;
B = T6;
D = B;
C = 5.0;
printf("%s", "\nB=\n");
printf("%d", D);
printf("%s", "\n");
printf("%f", C);
printf("%s", "\n");
printf("%s", A);

return 0;
}
