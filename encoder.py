from enum import Enum
import struct
import math

# Mensagem de entrada
# |-------------------------------------------------------------------- max 35 bytes -----------------------------------------------------------------------|
# |-------------------------------------------------------------------------------------------|---------------- (opcional conforme operador) ---------------|
# |--------------------------------------- 2 bytes ------------|-------  max 16 bytes --------|----------- 1 byte -----------|-------  max 16 bytes --------|
# |---------- byte 0 -----------|---------- byte 1 ------------|--------- byte 2+n1 ----------|-------  byte 2+n1+1 ---------|------  byte 2+n1+1+n2 -------|
# |         operador            |  tipo val 1   |       n1     |           valor 1            | tipo val 2   |       n2      |           valor 2            |
# |-----------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
#
# Mensagem de saída
# |----------------------- max 17 bytes ------------------------|
# |---------- byte 1 ------------|--------- byte 2+n1 ----------|
# |  tipo val 1   |       n1     |           valor 1            |
# |------------------------------|------------------------------|
#
# Operadores
# | código | operador | argumentos |
# | 0x00   |   "+"    |     2      |
# | 0x01   |   "-"    |     2      |
# | 0x02   |   "*"    |     2      |
# | 0x03   |   "/"    |     2      |
# | 0x04   |  "sqrt"  |     1      |
# | 0x05   |  "pow"   |     2      |
# | 0xFF   |  "exit"  |     0      |
#
# Tipos de valores
# 0x0 - int
# 0x1 - float

class Operation(Enum):
  SUM = 0x00
  SUB = 0x01
  MUL = 0x02
  DIV = 0x03
  SQRT = 0x04
  POW = 0x05
  LOG = 0x06
  EXIT = 0xFF

  def get_code(self) -> int:
    return self.value
  
  def get_args(self) -> int:
    args = {
      "SUM": 2,
      "SUB": 2,
      "MUL": 2,
      "DIV": 2,
      "SQRT": 1,
      "POW": 2,
      "LOG": 2,
      "EXIT": 0
    }
    return args[self.name]

class ValueType(Enum):
  INT = 0x0
  FLOAT = 0x1

  @staticmethod
  def from_value(value: int | float):
    """
    Retorna o tipo de valor de acordo com o tipo do valor passado
    """
    if isinstance(value, int):
      return ValueType.INT
    elif isinstance(value, float):
      return ValueType.FLOAT
    else:
      raise ValueError("Tipo de valor inválido")
  
  @staticmethod
  def encode(value: int | float) -> bytes:
    """
    Retorna um array de bytes com o valor codificado no formato
    | tipo | n |  valor  |
    |  byte 1  | n bytes |
    """
    value_type = ValueType.from_value(value)
    arr = bytearray([])

    if value_type == ValueType.INT:
      byte_length = math.ceil(value.bit_length() / 8)
      value_bytes = value.to_bytes(byte_length, "little", signed=True)
    elif value_type == ValueType.FLOAT:
      value_bytes = bytearray(struct.pack("<d", value))
      byte_length = len(value_bytes)
    else:
      raise ValueError("Tipo de valor inválido")
    
    if byte_length > 16:
        raise ValueError("Valor muito grande")
    
    type_and_length_byte = value_type.value << 4 | byte_length
    arr.append(type_and_length_byte)
    arr.extend(value_bytes)
    
    return bytes(arr)
    
  @staticmethod
  def decode(data: bytes) -> int | float:
    """
    Retorna o valor decodificado de acordo com o array de bytes passado
    """
    type_and_length_byte = data[0]
    value_type = ValueType(type_and_length_byte >> 4)
    value_byte_length = type_and_length_byte & 0xF
    value_bytes = data[1:1 + value_byte_length]
    
    if value_type == ValueType.INT:
      value = int.from_bytes(value_bytes, "little", signed=True)
    elif value_type == ValueType.FLOAT:
      value = struct.unpack("<d", value_bytes)[0]
    else:
      raise ValueError("Tipo de valor inválido")
    
    return value, value_byte_length + 1

class IncomingMessage:
  def __init__(self, operation: Operation, values: list[int | float]) -> None:
    self.operation = operation
    self.values = values

  def encode(self) -> bytes:
    code = self.operation.get_code()
    args = self.operation.get_args()
    arr = bytearray([code])

    if len(self.values) != args:
      arg_names = [f"valor{i + 1}" for i in range(args)]
      raise ValueError(f"Número de argumentos inválido, utilize: <{'> <'.join(arg_names)}>")

    for i in range(args):
      value = self.values[i]
      arr.extend(ValueType.encode(value))

    return bytes(arr)

  @staticmethod
  def get_max_bytes():
    return 35
  
  @staticmethod
  def decode(data: bytes) -> "IncomingMessage":
    operation = Operation(data[0])
    args = operation.get_args()
    values: list[int | float] = []

    byte_idx = 1
    for _ in range(args):
      value, length = ValueType.decode(data[byte_idx:])
      values.append(value)
      byte_idx += length

    return IncomingMessage(operation, values)
  
class OutgoingMessage:
  def __init__(self, value: int | float) -> None:
    self.value = value

  def encode(self) -> bytes:
    return ValueType.encode(self.value)

  @staticmethod
  def get_max_bytes():
    return 17
  
  @staticmethod
  def decode(data: bytes) -> "OutgoingMessage":
    value, _ = ValueType.decode(data)
    return OutgoingMessage(value)