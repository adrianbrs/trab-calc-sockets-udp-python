# Calculadora com sockets - UPF 2023/2
> Trabalho da disciplina de Ubiquitous Computing envolvendo Socket UDP em Python

# Empacotamento dos dados

## Mensagem de entrada
|-------------------------------------------------------------------- max 35 bytes -----------------------------------------------------------------------|
|-------------------------------------------------------------------------------------------|---------------- (opcional conforme operador) ---------------|
|--------------------------------------- 2 bytes ------------|-------  max 16 bytes --------|----------- 1 byte -----------|-------  max 16 bytes --------|
|---------- byte 0 -----------|---------- byte 1 ------------|--------- byte 2+n1 ----------|-------  byte 2+n1+1 ---------|------  byte 2+n1+1+n2 -------|
|         operador            |  tipo val 1   |       n1     |           valor 1            | tipo val 2   |       n2      |           valor 2            |
|-----------------------------|------------------------------|------------------------------|------------------------------|------------------------------|

## Mensagem de saída
|----------------------- max 17 bytes ------------------------|
|---------- byte 0 ------------|--------- byte 1+n1 ----------|
|  tipo val 1   |       n1     |           valor 1            |
|------------------------------|------------------------------|

## Operadores

| código | operador | argumentos |
| 0x00   |   "+"    |     2      |
| 0x01   |   "-"    |     2      |
| 0x02   |   "*"    |     2      |
| 0x03   |   "/"    |     2      |
| 0x04   |  "sqrt"  |     1      |
| 0x05   |  "pow"   |     2      |
| 0x06   |  "log"   |     2      |
| 0xFF   |  "exit"  |     0      |

## Tipos de valores
0x0 - int
0x1 - float

# Entrada
<operador> <valor1> [<valor2>, ...]