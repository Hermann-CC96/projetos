# Os arquivos do sistema de arquivos ficam na pasta ../../src e sao COMPARTILHADOS
# com a versao Linux. Aqui so entra a camada de memoria especifica do ESP32.
idf_component_register(
    SRCS "memoria_esp32.cpp"
         "../../src/main.cpp"
         "../../src/sa.cpp"
         "../../src/sa_api.cpp"
    INCLUDE_DIRS "." "../../src"
)
