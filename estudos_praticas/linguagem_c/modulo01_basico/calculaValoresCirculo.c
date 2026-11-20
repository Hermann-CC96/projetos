/*
    Autor: Hermenigildo Correia Ca
    data: 18/11/2026
    Descrição: Programa que calcula e imprime o diâmetro, o valor da circonferência e a área do círculo.
*/

#include <stdio.h>

int main(void){
    float raio, pi = 3.14159;
    float diametro, circonferencia, area;

    printf("Digite o valor de raio: ");
    scanf("%f", &raio);

    diametro = 2*raio;
    circonferencia = 2*pi*raio;
    area = pi*(raio*raio);

    printf("O valor do diametro eh: %.2f\n", diametro);
    printf("O valor da circonferencia eh: %.2f\n", circonferencia);
    printf("O valor da area eh: %.2f\n", area);

return 0;
}
