/*
    Autor: Hermnigildo Correia Cá
    Data: 19/11/2026
    Descrição: Programa que imprime o maior e menor numero inteiro, o usuário entra com cinco inteiro.
*/

#include <stdio.h>

int main(void){
    int num1, num2, num3, num4, num5;
    int maior = 0, menor = 0;

    printf("Digite cinco numeros inteiro: ");
    scanf("%d %d %d %d %d", &num1, &num2, &num3, &num4, &num5);

    maior = num1;
    menor = num1;

    //Verifica o segundo numero
    if(num2 > maior){
        maior = num2;
    }
    if(num2 < menor){
        menor = num2;
    }

    //Verifica o tericeiro numero
    if(num3 > maior){
        maior = num3;
    }
    if(num3 < menor){
        menor = num3;
    }

    //Verifica o quarto numero
    if(num4 > maior){
        maior = num4;
    }
    if(num4 < menor){
        menor = num4;
    }

    //Verifica o quinto numero
    if(num5 > maior){
        maior = num5;
    }
    if(num5 < menor){
        menor = num5;
    }

    printf("O maior numero eh: %d\n", maior);
    printf("O menor numero eh: %d\n", menor);

return 0;
}
