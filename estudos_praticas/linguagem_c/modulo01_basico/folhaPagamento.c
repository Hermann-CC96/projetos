/*
    Este programa que realiza o exemplo de calculo de folha de pagamento,
    o usuario entra com dois valores reais (b e c) e o resultado do produto é
    colocado em variavel real (a).
*/

#include <stdio.h>

int main(void){
    float a, b, c;
    //float lido;

    printf("Digite dois valores real: ");
    scanf("%f %f", &b, &c);

    a = b * c;

    printf("O valor de pagamento eh: %.2f", a);

return 0;
}