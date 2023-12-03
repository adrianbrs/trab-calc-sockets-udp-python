import socket
import os
import math
from encoder import Operation, IncomingMessage, OutgoingMessage

# Cria o socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Escuta qualquer IP em uma porta específica
udp.bind(("", int(os.environ.get("PORT", "8888"))))

# Cria uma classe para efetuar as operações
class Calculator:
  def __init__(self) -> None:
    self.operations = {
      Operation.SUM: self.sum,
      Operation.SUB: self.sub,
      Operation.MUL: self.mul,
      Operation.DIV: self.div,
      Operation.SQRT: self.sqrt,
      Operation.POW: self.pow,
      Operation.LOG: self.log
    }

  def calc(self, operation: Operation, values: list[int | float]):
    return self.operations[operation](*values)

  def sum(self, v1, v2):
    return v1 + v2

  def sub(self, v1, v2):
    return v1 - v2
  
  def mul(self, v1, v2):
    return v1 * v2
  
  def div(self, v1, v2):
    return v1 / v2
  
  def sqrt(self, v1):
    return math.sqrt(v1)
  
  def pow(self, v1, v2):
    return v1 ** v2
  
  def log(self, v1, v2):
    return math.log(v1, v2)
  
calculator = Calculator()

try:
  while True:
    # Recebe os argumentos para calcular do cliente
    max_size = IncomingMessage.get_max_bytes()
    raw_request, attr = udp.recvfrom(max_size)
    
    if raw_request is None:
      break

    try:
      # Decodifica a requisição
      request = IncomingMessage.decode(raw_request)

      print("Request: ", request.operation, request.values)

      # Comando para encerrar o servidor
      if request.operation == Operation.EXIT:
        break

      # Calcula o resultado
      result = calculator.calc(request.operation, request.values)

      print("Result: ", result)

      # Cria uma mensagem de resposta
      response = OutgoingMessage(result)

      # Envia a resposta para o cliente
      udp.sendto(response.encode(), attr)

      print("Response sent")

    except Exception as e:
      print("Erro ao decodificar a mensagem", e)
      udp.sendto("Erro ao decodificar a mensagem".encode(), attr)
      continue

except KeyboardInterrupt:
  print("Servidor encerrado por interrupção do teclado")

finally:
  udp.close()
  print("Servidor fechado")