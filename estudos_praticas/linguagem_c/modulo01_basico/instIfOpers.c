/*Usando instrução if, operadpres relacionais e de igualidade.
*/

#include <stdio.h>

    int main(void){
    int num1, num2;

    printf("entre com dois numeros inteiros \n");
    scanf("%d %d", &num1, &num2); //Lê dois numeros inteiros.

    if(num1 == num2){
        printf("Os numeros %d e %d sao iguais \n", num1, num2);
    }
    if (num1 != num2){
        printf("Os numeros %d e %d sao diferentes \n", num1, num2);
    }
    if(num1 > num2){
        printf("O numero %d e maior que o numero %d \n", num1, num2);
    }
    if(num1 < num2){
        printf("O numero %d e menor que o numero %d \n", num1, num2);
    }
    if(num1 >= num2){
        printf("O numero %d e maior ou igual ao numero %d \n", num1, num2);
    }
    if(num1 <= num2){
        printf("O numero %d e menor ou igual ao numero %d \n", num1, num2);
    }

return 0;

}