# Calculadora com sockets - UPF 2023/2

> Trabalho da disciplina de Ubiquitous Computing envolvendo Socket UDP em Python

## Empacotamento dos dados

### Mensagem de entrada (request)

<table>
  <tr>
    <th colspan="5" align="center"><a href="./encoder.py#L121">IncomingMessage</a></th>
  </tr>
  <tr>
    <td colspan="5" align="center">max 35 bytes</td>
  </tr>
  <tr>
    <td colspan="3"></td>
    <td colspan="2" align="center">(opcional conforme operador)</td>
  </tr>
  <tr>
    <td colspan="2" align="center">2 bytes</td>
    <td align="center">max 16 bytes</td>
    <td align="center">1 byte</td>
    <td align="center">max 16 bytes</td>
  </tr>
  <tr>
    <td align="center">byte 0</td>
    <td align="center">byte 1</td>
    <td align="center">byte 2+n1</td>
    <td align="center">byte 2+n1+1</td>
    <td align="center">byte 2+n1+1+n2</td>
  </tr>
  <tr>
    <td align="center">operador</td>
    <td align="center">tipo val 1 | n1</td>
    <td align="center">valor 1</td>
    <td align="center">tipo val 2 | n2</td>
    <td align="center">valor 2</td>
  </tr>
</table>

### Mensagem de saída (response)

<table>
  <tr>
    <th colspan="2" align="center"><a href="./encoder.py#L158">OutgoingMessage</a></th>
  </tr>
  <tr>
    <td colspan="2" align="center">max 17 bytes</td>
  </tr>
  <tr>
    <td align="center">byte 0</td>
    <td align="center">byte 1+n1</td>
  </tr>
  <tr>
    <td align="center">tipo val 1 | n1</td>
    <td align="center">valor 1</td>
  </tr>
</table>

### Operações

<table>
  <tr>
    <th colspan="3" align="center"><a href="./encoder.py#L33">Operation</a></th>
  </tr>
  <tr>
    <th align="center">código</th>
    <th align="center">operação</th>
    <th align="center">argumentos</th>
  </tr>
  <tr>
    <td align="center"><code>0x01</code></td>
    <td align="center"><code>+</code></td>
    <td align="center"><code>2</code></td>
  </tr>
  <tr>
    <td align="center"><code>0x02</code></td>
    <td align="center"><code>-</code></td>
    <td align="center"><code>2</code></td>
  </tr>
  <tr>
    <td align="center"><code>0x03</code></td>
    <td align="center"><code>*</code></td>
    <td align="center"><code>2</code></td>
  </tr>
  <tr>
    <td align="center"><code>0x04</code></td>
    <td align="center"><code>/</code></td>
    <td align="center"><code>2</code></td>
  </tr>
  <tr>
    <td align="center"><code>0x05</code></td>
    <td align="center"><code>sqrt</code></td>
    <td align="center"><code>1</code></td>
  </tr>
  <tr>
    <td align="center"><code>0x06</code></td>
    <td align="center"><code>pow</code></td>
    <td align="center"><code>2</code></td>
  </tr>
  <tr>
    <td align="center"><code>0xFF</code></td>
    <td align="center"><code>exit</code></td>
    <td align="center"><code>0</code></td>
  </tr>
</table>

### Tipos de valores

<table>
  <tr>
    <th colspan="2" align="center"><a href="./encoder.py#L58">ValueType</a></th>
  </tr>
  <tr>
    <th align="center">código</th>
    <th align="center">tipo</th>
  </tr>
  <tr>
    <td align="center"><code>0x0</code></td>
    <td align="center"><code>int</code></td>
  </tr>
  <tr>
    <td align="center"><code>0x1</code></td>
    <td align="center"><code>float</code></td>
  </tr>
</table>

## Entrada

```bash
<operador> <valor1> [<valor2>, ...]
```
