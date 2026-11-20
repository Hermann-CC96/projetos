/*
    Autor: Hermenigildo Correia Cá
    Data: 01/06/2024
    Descrição: Programa que compara dois números inteiros e exibe o maior.
*/

#include <stdio.h>

int main(void){
    int num1, num2;

    printf("Digite dois numeros inteiros: ");
    scanf("%d %d", &num1, &num2);

    if(num1 > num2){
        printf("O maior numero eh: %d\n", num1);
    } else if(num2 > num1){
            printf("O maior numero eh: %d\n", num2);
        } else {
            printf("Os numeros sao iguais.\n");
        }
return 0;
}