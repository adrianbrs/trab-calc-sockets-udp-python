import socket
import os
from encoder import Operation, IncomingMessage, OutgoingMessage

# Cria o socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define o endereço do servidor
server = ('127.0.0.1', int(os.environ.get("PORT", "8888")))

# Mapeia um símbolo para uma operação
op_symbol_map = {
  "exit": Operation.EXIT,
  "+": Operation.SUM,
  "-": Operation.SUB,
  "*": Operation.MUL,
  "/": Operation.DIV,
  "sqrt": Operation.SQRT,
  "pow": Operation.POW,
  "log": Operation.LOG
}

available_operations = [op for op in op_symbol_map.keys() if op != "exit"]

def get_request(user_input: str):
  op_symbol, *values = user_input.split(" ")

  if op_symbol not in op_symbol_map:
    err_msg = f"Operação inválida: {op_symbol}\n\n";
    err_msg += "Operações disponíveis:\n"

    for op in available_operations:
      op_values = [f"value{i+1}" for i in range(op_symbol_map[op].get_args())];
      err_msg += f"  {op} <{'> <'.join(op_values)}>\n"

    raise ValueError(err_msg)

  operation = op_symbol_map[op_symbol]

  # Mapeia os valores para o tipo correto
  values = [int(v) if "." not in v else float(v) for v in values]

  return IncomingMessage(operation, values)

print("# Calculadora #")
print("Operações disponíveis:", ", ".join(available_operations))
print("Para fechar o servidor e sair, digite 'exit'")
print("")
print("Digite a operação no formato: <operador> [<valor> ...]")

try:
  # Cria uma requisição baseado na entrada do usuário
  request = get_request(input("> "))

  # Envia a mensagem para o servidor
  udp.sendto(request.encode(), server)

  # Comando para encerrar o servidor
  if request.operation == Operation.EXIT:
    print("Servidor fechado")
    udp.close()
    exit()

  # Aguarda a resposta do servidor
  raw_response = udp.recv(OutgoingMessage.get_max_bytes())

  # Decodifica a resposta do servidor
  try:
    response = OutgoingMessage.decode(raw_response)
    print("Resultado:", response.value)
  except:
    print("Erro:", raw_response.decode())
except Exception as e:
  print("Erro:", e)

udp.close()