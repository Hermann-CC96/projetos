/*
    Autor: Hermenigildo Correia Cá
    Data: 01/06/2024
    Descrição: Programa que realiza operações matemáticas básicas com dois números inteiros.
*/


#include <stdio.h>

int main(void){
	int num1, num2;
	
	printf("Digite dois numeros inteiros: ");
    scanf("%d %d", &num1, &num2);

	printf("A soma eh: %d\n", num1 + num2);
	printf("O produto eh: %d\n", num1 * num2);
	printf("A diferenca eh: %d\n", num1 - num2);
	printf("O qupociente eh: %d\n", num1 / num2);
	printf("O resto eh: %d\n", num1 % num2);

return 0;
}

