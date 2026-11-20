/*
    Este programa calcula o produto de três números inteiros (x, y, z)
    fornecido pelo usuário, e exibe o resultado na tela.
*/

#include <stdio.h>

int main(void) {

    int x, y, z, resultado;
    int lidos;

    printf("Digite tres numeros inteiros: ");
    lidos = scanf("%d %d %d", &x, &y, &z);

    if (lidos != 3) {
        printf("Erro ao ler os numeros! Digite apenas inteiros.\n");
        return 1;
    }

    resultado = x * y * z;

    printf("O produto de %d, %d e %d eh: %d\n", x, y, z, resultado);

return 0;
}