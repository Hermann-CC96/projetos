/*
    Autor: Hermenigildo Correia Cá
    Data: 01/06/2024
    Descrição: Programa que calcula a soma, o produto, a média, menore maior de três números inteiros.
*/

#include <stdio.h>

int main(void){
    int num1, num2, num3, soma, produto, maior, menor;
    
    float media;

    printf("Digite tres numeros inteiros: ");
    scanf("%d %d %d", &num1, &num2, &num3);

    soma = num1 + num2 + num3;
    produto = num1 * num2 * num3;
    media = (num1 + num2 + num3)/3.0;

    if(num1 > num2 && num1 > num3){
        maior = num1;
    }else if(num2 > num1 && num2 > num3){
        maior = num2;
    }else{
        maior = num3;   
    }

    if(num1 < num2 && num1 < num3){
        menor = num1;
    }else if(num2 < num1 && num2 < num3){
        menor = num2;
    }else{
        menor = num3;
    }

    printf("Soma = %d\n", soma);
    printf("Produto = %d\n", produto); 
    printf("Media = %.2f\n", media);
    printf("O maior numero eh: %d\n", maior);
    printf("O menor numero eh: %d\n", menor);

return 0;
}