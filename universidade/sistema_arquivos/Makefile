# Compilacao da versao Linux/WSL (emulacao da memoria em arquivo).
#
#   make            compila o programa do enunciado        -> ./sa_teste
#   make run        recria PARTICAO.BIN e executa
#   make testes     compila e roda os testes automaticos   -> ./sa_testes
#   make MEM=32768  simula uma AT24C256 (padrao: AT24C512 = 65536)
#   make testes SAN=   (sem verificadores de memoria; use no MinGW/Windows)
#   make clean

CXX      ?= g++
MEM      ?= 65536
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17 -Isrc -DMEM_TAMANHO=$(MEM)UL

SAN      ?= -fsanitize=address,undefined
SA_SRC   = src/sa.cpp src/sa_api.cpp linux/memoria_linux.cpp

all: sa_teste

sa_teste: src/main.cpp $(SA_SRC) src/*.h
	$(CXX) $(CXXFLAGS) src/main.cpp $(SA_SRC) -o $@

sa_testes: linux/testes.cpp $(SA_SRC) src/*.h
	$(CXX) $(CXXFLAGS) $(SAN) linux/testes.cpp $(SA_SRC) -o $@

run: sa_teste
	rm -f PARTICAO.BIN
	./sa_teste

testes: sa_testes
	rm -f PARTICAO.BIN
	./sa_testes

clean:
	rm -f sa_teste sa_testes PARTICAO.BIN
