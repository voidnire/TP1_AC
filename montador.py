import sys

# Erin Dante de Oliveira Vasconcelos
# 22251136

REGISTRADORES = {
    "x0": 0, "zero": 0, "x1": 1, "ra": 1, "x2": 2, "sp": 2,
    "x3": 3, "gp": 3, "x4": 4, "tp": 4,
    "x5": 5, "t0": 5, "x6": 6, "t1": 6, "x7": 7, "t2": 7,
    "x8": 8, "s0": 8, "fp": 8, "x9": 9, "s1": 9,
    "x10": 10, "a0": 10, "x11": 11, "a1": 11, "x12": 12, "a2": 12,
    "x13": 13, "a3": 13, "x14": 14, "a4": 14, "x15": 15, "a5": 15,
    "x16": 16, "a6": 16, "x17": 17, "a7": 17,
    "x18": 18, "s2": 18, "x19": 19, "s3": 19, "x20": 20, "s4": 20,
    "x21": 21, "s5": 21, "x22": 22, "s6": 22, "x23": 23, "s7": 23,
    "x24": 24, "s8": 24, "x25": 25, "s9": 25, "x26": 26, "s10": 26,
    "x27": 27, "s11": 27,
    "x28": 28, "t3": 28, "x29": 29, "t4": 29, "x30": 30, "t5": 30,
    "x31": 31, "t6": 31,
}

# instrucoes formato R
INSTR_R = { #op->7b,
    "add":  dict(opcode=0b0110011, funct3=0b000, funct7=0b0000000),
    "sub":  dict(opcode=0b0110011, funct3=0b000, funct7=0b0100000),
    "sll":  dict(opcode=0b0110011, funct3=0b001, funct7=0b0000000),
    "slt":  dict(opcode=0b0110011, funct3=0b010, funct7=0b0000000),
    "sltu": dict(opcode=0b0110011, funct3=0b011, funct7=0b0000000),
    "xor":  dict(opcode=0b0110011, funct3=0b100, funct7=0b0000000),
    "srl":  dict(opcode=0b0110011, funct3=0b101, funct7=0b0000000),
    "sra":  dict(opcode=0b0110011, funct3=0b101, funct7=0b0100000),
    "or":   dict(opcode=0b0110011, funct3=0b110, funct7=0b0000000),
    "and":  dict(opcode=0b0110011, funct3=0b111, funct7=0b0000000),
    "mul":  dict(opcode=0b0110011, funct3=0b000, funct7=0b0000001),
    "div":  dict(opcode=0b0110011, funct3=0b100, funct7=0b0000001),
    "rem":  dict(opcode=0b0110011, funct3=0b110, funct7=0b0000001),
}

INSTR_I_ARIT = {
    "addi":  dict(opcode=0b0010011, funct3=0b000),
    "slti":  dict(opcode=0b0010011, funct3=0b010),
    "sltiu": dict(opcode=0b0010011, funct3=0b011),
    "ori":   dict(opcode=0b0010011, funct3=0b110),
    "andi":  dict(opcode=0b0010011, funct3=0b111),
    "slli":  dict(opcode=0b0010011, funct3=0b001, funct7=0b0000000),  # shamt em vez de imm12
    "srli":  dict(opcode=0b0010011, funct3=0b101, funct7=0b0000000),
    "srai":  dict(opcode=0b0010011, funct3=0b101, funct7=0b0100000),
}

INSTR_I_LOAD = {
    "lb": dict(opcode=0b0000011, funct3=0b000), #f3: tamanho dado e sinal ou ext 0
    "lh": dict(opcode=0b0000011, funct3=0b001), # 2by
    "lw": dict(opcode=0b0000011, funct3=0b010), # 4by
    "lbu": dict(opcode=0b0000011, funct3=0b100), # unsigned
    "lhu": dict(opcode=0b0000011, funct3=0b101), # 2by
    "jalr": dict(opcode=0b1100111, funct3=0b000), #pra pseudo
}

INSTR_S = {
    "sb": dict(opcode=0b0100011, funct3=0b000),
    "sh": dict(opcode=0b0100011, funct3=0b001),
    "sw": dict(opcode=0b0100011, funct3=0b010),
}

INSTR_B = {
    "beq": dict(opcode=0b1100011, funct3=0b000),
    "bne": dict(opcode=0b1100011, funct3=0b001),
    "blt": dict(opcode=0b1100011, funct3=0b100),
    "bge": dict(opcode=0b1100011, funct3=0b101),
    "bltu": dict(opcode=0b1100011, funct3=0b110),
    "bgeu": dict(opcode=0b1100011, funct3=0b111),
}

INSTR_U = {
    "lui": dict(opcode=0b0110111),
    "auipc": dict(opcode=0b0010111),
}

DIRETIVOS = ['.word', '.half', '.byte', '.zero', '.space','.align','.globl']

# ---------------------------- ASM TO HEX  ----------------------------

def code_r(instrucao):
  opcode = INSTR_R[instrucao[0]]["opcode"]
  funct3 = INSTR_R[instrucao[0]]["funct3"]
  funct7 = INSTR_R[instrucao[0]]["funct7"]
  rd = REGISTRADORES[instrucao[1]]
  rs1 = REGISTRADORES[instrucao[2]]
  rs2 = REGISTRADORES[instrucao[3]]

  word = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
  return f"0x{word:08x}"


def code_i(instrucao): #arit
  op, rd = instrucao[0],REGISTRADORES[instrucao[1]]
  rs1, imm = REGISTRADORES[instrucao[2]], int(instrucao[3], 0)

  info = INSTR_I_ARIT[op]
  opcode = info["opcode"]
  funct3 = info["funct3"]

  if "funct7" in info: # Deslocamentos: monta os 12 bits juntando funct7 (7 bits) + shamt (5 bits)
    imm_12 = (info["funct7"] << 5) | (imm & 0x1F)
  else:
    # Imediato normal: 12 bits com sinal
    imm_12 = imm & 0xFFF

  word = (imm_12 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
  return f"0x{word:08x}"


def code_i_l(instrucao): # imm rsi f3 rd opcode
  op, rd = instrucao[0],REGISTRADORES[instrucao[1]]

  imm,rs1 = int(instrucao[2], 0), REGISTRADORES[instrucao[3]]

  opcode = INSTR_I_LOAD[op]["opcode"]
  funct3 = INSTR_I_LOAD[op]["funct3"]

  imm_12 = imm & 0xFFF
  word = (imm_12 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
  return f"0x{word:08x}"


def code_s(instrucao): #sw rs2, offset(rs1)
  op, rs2 = instrucao[0],REGISTRADORES[instrucao[1]]

  # offset_str = instrucao[2]
  # imm_str, rs1_str = offset_str.split('(')
  # rs1_str = rs1_str.replace(')', '')

  imm, rs1 = int(instrucao[2],0), REGISTRADORES[instrucao[3]]

  opcode = INSTR_S[op]["opcode"]
  funct3 = INSTR_S[op]["funct3"]


  imm_12 = imm & 0xFFF
  imm_4_0 = imm_12 & 0x1F         # 5 bits inferiores
  imm_11_5 = (imm_12 >> 5) & 0x7F # 7 bits superiores

  word = (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
  return f"0x{word:08x}"

# beq rs1, rs2, label
def code_b(instrucao, labels, pc):
  op = instrucao[0]

  rs1 = REGISTRADORES[instrucao[1]]
  rs2 = REGISTRADORES[instrucao[2]]
  label = instrucao[3]

  if label in labels: # offset = lbl_adrss - PCinst
    offset = labels[label] - pc
  else:
    offset = int(label, 0)

  opcode = INSTR_B[op]["opcode"]
  funct3 = INSTR_B[op]["funct3"]

  imm_13 = offset & 0x1FFF
  imm_12   = (imm_13 >> 12) & 0x1 # 1 bit
  imm_10_5 = (imm_13 >> 5)  & 0x3F # 6 bits
  imm_4_1  = (imm_13 >> 1)  & 0xF # 4 bits
  imm_11   = (imm_13 >> 11) & 0x1 # 1 bit

  word = (
        (imm_12   << 31) |
        (imm_10_5 << 25) |
        (rs2      << 20) |
        (rs1      << 15) |
        (funct3   << 12) |
        (imm_4_1  << 8)  |
        (imm_11   << 7)  |
        opcode
    )

  return f"0x{word:08x}"

def code_u(instrucao): #lui rd, immediate
  op = instrucao[0]
  rd = REGISTRADORES[instrucao[1]]
  imm_31_12 = int(instrucao[2], 0) & 0xFFFFF

  opcode = INSTR_U[op]["opcode"]

  word = (imm_31_12 << 12) | (rd << 7) | opcode

  return f"0x{word:08x}"

def expandir_li(tokens): # li rd, imm
  rd = tokens[1] # vai pra 2 inst
  imm_str = tokens[2]
  imm = int(tokens[2], 0)

  lo = imm & 0xFFF
  if lo >= 0x800:
    lo -= 0x1000
    hi = ((imm - lo) >> 12) & 0xFFFFF
  else:
    hi = (imm >> 12) & 0xFFFFF

  hi_str = str(hi)
  lo_str = str(lo)

  return ["lui", rd, hi_str], ["addi", rd, rd, lo_str]

def code_la(tokens, pc_auipc):  # la rd, label
  rd = tokens[1]
  label = tokens[2]


  offset = labels[label] - pc_auipc

  #divide hi lo e trata ext. sinal
  lo = offset & 0xFFF
  if lo >= 0x800:
    lo -= 0x1000
    hi = ((offset - lo) >> 12) & 0xFFFFF
  else:
    hi = (offset >> 12) & 0xFFFFF

  # codes individuais
  auipc = ["auipc", rd, str(hi)] # adiciona hi depois
  addi = ["addi", rd, rd, str(lo)] # lo depois

  hex_auipc = code_u(auipc)
  hex_addi = code_i(addi)

  return hex_auipc, hex_addi

# --------- AUXILIAR: FIXA DE BYTES DATA SECTION ---------------------
def escreve_bytes(buffer, valor, n_bytes):
  valor = int(valor, 0) & ((1 << (8 * n_bytes)) - 1)  # trata negativos
  for i in range(n_bytes):
    buffer.append((valor >> (8 * i)) & 0xFF)  # little-endian

# ----------------------------------------------

if len(sys.argv) != 3:
    print("Não não!\npython montador.py input.asm output.txt\n")
    sys.exit(1)

arquivo_entrada = sys.argv[1]
arquivo_saida = sys.argv[2]

labels = {}
codigo_asm = []
dados = bytearray() # buffer de bytes seção .data
# ^ para guardar bytes de tamanhos variados

pc_text = 0x00000000
pc_data = 0x00200000

current_section = ".text"

with open(arquivo_entrada, "r") as codigo:
  for linha in codigo:
    linha_clean = linha.split('#')[0].strip()
    if not linha_clean:
      continue

    if linha_clean == ".text":
      current_section = '.text'
      continue
    elif linha_clean == ".data":
      current_section = '.data'
      continue


    tokens = linha_clean.replace(',', ' ').replace('(', ' ').replace(')', ' ').split()
    if not tokens:
        continue

    if tokens[0].endswith(':'): # labels
      label = tokens[0][:-1]
      if current_section == ".text":
        labels[label] = pc_text
      else:
        labels[label] = pc_data
      tokens = tokens[1:]

    if not tokens:
      continue

    # SEÇÃO DATA -----------------------------------
    if current_section == ".data":
      dir_ = tokens[0]
      vals = tokens[1:]

      if dir_ == ".word":
        for v in vals:
          escreve_bytes(dados, v, 4)
        pc_data += 4 * len(vals)

      elif dir_ == ".half":
        for v in vals:
          escreve_bytes(dados, v, 2)
        pc_data += 2 * len(vals)

      elif dir_ == ".byte":
        for v in vals:
          escreve_bytes(dados, v, 1)
        pc_data += 1 * len(vals)

      elif dir_ in (".zero", ".space"):
        n = int(vals[0], 0)
        dados.extend([0] * n)
        pc_data += n

      elif dir_ == ".align":
        n = int(vals[0], 0)
        alinhamento = 1 << n
        resto = pc_data % alinhamento
        if resto != 0:
          preenchimento = alinhamento - resto
          dados.extend([0] * preenchimento)
          pc_data += preenchimento

      elif dir_ == ".globl":
        pass  # não produz saída

      continue  # nunca cai em codigo_asm_text

# FIM SEÇÃO DATA-------------------------

# SEÇÃO TEXT -----------------------------------
    # PSEUDO INSTRUÇÕES
    if tokens[0] == 'la':
      pc_text +=4

    elif tokens[0] == 'mv':
      tokens[0] = 'addi'
      tokens.append('0')

    elif tokens[0] == 'j':
      label = tokens[1]
      tokens[0] = 'beq'
      tokens[1] = 'zero'
      tokens.append('zero')
      tokens.append(label)

    elif tokens[0] == 'jr':#jr rs
      #jalr x0, 0(rs)
      tokens[0] = 'jalr'
      rs = tokens[1]
      tokens[1] = 'x0'
      tokens.append('0')
      tokens.append(rs)

    elif tokens[0] == 'li': # li rd, imm
      rd = tokens[1]
      imm_str = tokens[2]
      imm = int(tokens[2], 0)

      if -2048 <= imm <= 2047:
        tokens[0] = 'addi'
        tokens[2] = 'zero'
        tokens.append(imm_str) # ['addi', rd, 'zero', imm_str]
      else:
        lui, addi = expandir_li(tokens)
        codigo_asm.append(lui)
        pc_text += 4
        tokens = addi

    codigo_asm.append(tokens)
    pc_text += 4 # 4 bytes por inst


# ----------------------------------------------

pc = 0x00000000
codigo_hex = []
# pcs_hex = []
# pcs_hex.append(pc)

# IDENTIFICA TIPO DE INSTRUCAO E CODIFICA
for instrucao in codigo_asm:
  op = instrucao[0]

  if op in INSTR_R:
    hex_str = code_r(instrucao)
    codigo_hex.append(hex_str)
    pc += 4

  elif op in INSTR_I_ARIT:
    hex_str = code_i(instrucao)
    codigo_hex.append(hex_str)
    pc += 4

  elif op in INSTR_I_LOAD:
    hex_str = code_i_l(instrucao)
    codigo_hex.append(hex_str)
    pc += 4

  elif op in INSTR_S:
    hex_str = code_s(instrucao)
    codigo_hex.append(hex_str)
    pc += 4

  elif op in INSTR_B:
    hex_str = code_b(instrucao, labels, pc)
    codigo_hex.append(hex_str)
    pc += 4

  elif op == "ecall":
    codigo_hex.append("0x00000073")
    pc += 4

  # PSEUDOINSTRUÇÕES
  elif op in INSTR_U:
    hex_str = code_u(instrucao)
    codigo_hex.append(hex_str)
    pc += 4

  elif op == "la": # la rd, label
    hex_auipc,hex_addi = code_la(instrucao, pc)
    codigo_hex.append(hex_auipc)
    codigo_hex.append(hex_addi)
    pc += 8
    

# CODIGO SECAO DATA
codigo_hex_data = []
for i in range(0, len(dados), 4):
    bloco = dados[i:i+4] # remontando fita de bytes em lil' endian
    while len(bloco) < 4:
        bloco = bloco + bytearray([0])  # padding se sobrar bytes incompletos
    palavra = bloco[0] | (bloco[1] << 8) | (bloco[2] << 16) | (bloco[3] << 24)
    codigo_hex_data.append(f"0x{palavra:08x}")

codigo_hex_final = codigo_hex + codigo_hex_data




# for hex_str in codigo_hex_final:
#   print(hex_str)

with open(arquivo_saida, "w", encoding="utf-8") as file:
    for hex_str in codigo_hex_final:
        file.write(hex_str + '\n')

# :)
