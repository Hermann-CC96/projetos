/* Programa para somar dois números
Este é um programa simples em C, que solicita ao usuario que ensira dois numeros inteiros e em sequida calcula 
a soma desses dois numeros e exibe o resultado na tela.
O programa é um exemplo de como utilizar a função printf() para exiber a mensagem na tela e a função scanf()
para ler a entrada de dados do usurio.
O programa também ensina os conceitos basicos de como declarar as variaveis e como utilizar operadores aritmeticos.
*/

#include <stdio.h>

int main(void) {
    int num1, num2, soma;

    printf("Digite o primeiro numero: ");
    scanf("%d", &num1);
    printf("Digite o segundo numero: ");
    scanf("%d", &num2);

    soma = num1 + num2;
    printf("A soma de %d + %d eh: %d\n", num1, num2, soma);
    return 0;

}
