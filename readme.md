# Calculadora com sockets - UPF 2023/2

> Trabalho da disciplina de Ubiquitous Computing envolvendo Socket UDP em Python

## Empacotamento dos dados

<style>
table {
  width: 100%;
}
table th, table td {
  border: 1px solid currentColor !important;
  border-collapse: collapse;
}
table th, table td {
  text-align: center;
}
</style>

### Mensagem de entrada (request)

<table>
  <tr>
    <th colspan="5"><a href="./encoder.py#L121">IncomingMessage</a></th>
  </tr>
  <tr>
    <td colspan="5">max 35 bytes</td>
  </tr>
  <tr>
    <td colspan="3"></td>
    <td colspan="2">(opcional conforme operador)</td>
  </tr>
  <tr>
    <td colspan="2">2 bytes</td>
    <td>max 16 bytes</td>
    <td>1 byte</td>
    <td>max 16 bytes</td>
  </tr>
  <tr>
    <td>byte 0</td>
    <td>byte 1</td>
    <td>byte 2+n1</td>
    <td>byte 2+n1+1</td>
    <td>byte 2+n1+1+n2</td>
  </tr>
  <tr>
    <td>operador</td>
    <td>tipo val 1 | n1</td>
    <td>valor 1</td>
    <td>tipo val 2 | n2</td>
    <td>valor 2</td>
  </tr>
</table>

### Mensagem de saída (response)

<table>
  <tr>
    <th colspan="2"><a href="./encoder.py#L158">OutgoingMessage</a></th>
  </tr>
  <tr>
    <td colspan="2">max 17 bytes</td>
  </tr>
  <tr>
    <td>byte 0</td>
    <td>byte 1+n1</td>
  </tr>
  <tr>
    <td>tipo val 1 | n1</td>
    <td>valor 1</td>
  </tr>
</table>

### Operações

<table>
  <tr>
    <th colspan="3"><a href="./encoder.py#L33">Operation</a></th>
  </tr>
  <tr>
    <th>código</th>
    <th>operação</th>
    <th>argumentos</th>
  </tr>
  <tr>
    <td><code>0x01</code></td>
    <td><code>+</code></td>
    <td><code>2</code></td>
  </tr>
  <tr>
    <td><code>0x02</code></td>
    <td><code>-</code></td>
    <td><code>2</code></td>
  </tr>
  <tr>
    <td><code>0x03</code></td>
    <td><code>*</code></td>
    <td><code>2</code></td>
  </tr>
  <tr>
    <td><code>0x04</code></td>
    <td><code>/</code></td>
    <td><code>2</code></td>
  </tr>
  <tr>
    <td><code>0x05</code></td>
    <td><code>sqrt</code></td>
    <td><code>1</code></td>
  </tr>
  <tr>
    <td><code>0x06</code></td>
    <td><code>pow</code></td>
    <td><code>2</code></td>
  </tr>
  <tr>
    <td><code>0xFF</code></td>
    <td><code>exit</code></td>
    <td><code>0</code></td>
  </tr>
</table>

### Tipos de valores

<table>
  <tr>
    <th colspan="2"><a href="./encoder.py#L58">ValueType</a></th>
  </tr>
  <tr>
    <th>código</th>
    <th>tipo</th>
  </tr>
  <tr>
    <td><code>0x1</code></td>
    <td><code>int</code></td>
  </tr>
  <tr>
    <td><code>0x2</code></td>
    <td><code>float</code></td>
  </tr>
</table>

## Entrada

```bash
<operador> <valor1> [<valor2>, ...]
```
