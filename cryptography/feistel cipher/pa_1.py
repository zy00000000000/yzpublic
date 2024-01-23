# Define constants
ROUNDS = 16

def list_to_string(mylist):
    result_string = ""
    for num in mylist:
        result_string += chr(num+65)
    return result_string

def get_shape_of_two_dimension_vector(matrix):
    # 使用 len() 函数获取二维列表的长度，即行数
    num_rows = len(matrix)

    # 使用 len() 函数获取每行的长度，即列数（假设每行的长度相同）
    num_columns = len(matrix[0])

    # 输出维度
    print(f"维度: {num_rows}x{num_columns}")

# Bit material and Mult list
bit_material = "615137ea41722dc5aa42745d"
mult_hex = bit_material[:16]  # Take the first 16 hex digits
Mult = [int(hex_digit, 16) + 1 for hex_digit in mult_hex] # Get the first 16 numbers in range 1-16

# Plaintext and Key
plaintext = "ITISNOTTOOTRICKY"
key = "KEYSAREESSENTIAL"

# Convert key to a numerical 4x4 matrix
numlist = [ord(x) - 65 for x in key]  # Make a list of numbers from letters
plaintextlist  = [ord(x) - 65 for x in plaintext]  # Make a list of numbers from letters
keymatrix = [numlist[i:i+4] for i in range(0, 16, 4)]  # Reshape to a 4x4 matrix

# 将每个十六进制字符拆分为4位二进制列表
binary_matrix = []
hxarray = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1],
            [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
            [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
            [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1],
            [0, 0, 0, 1], [0, 0, 1, 0]]

#Take 8 following hex digits from bit material as rows of an 8x4 matrix
for hex_char in bit_material[16:]:
    binary_matrix.append(hxarray[int(hex_char, 16)])


# 初始化结果矩阵
result_matrix = [[0 for _ in range(4)] for _ in range(8)]

# 进行矩阵乘法
for i in range(8):
    for j in range(4):
        for k in range(4):
            result_matrix[i][j] += binary_matrix[i][k] * keymatrix[k][j]

# 对结果进行模 26 运算
for i in range(8):
    for j in range(4):
        result_matrix[i][j] %= 26


#Input to round 0
Right_half = plaintextlist[8:]
Left_half = plaintextlist[0:8]

for r in range(16):
    round_key = [row[r % 4] for row in result_matrix]
    for i in range(8):
        Left_half[i] = (Left_half[i] + Mult[r]*Right_half[i] + round_key[i]) % 26
    temp = Right_half
    Right_half = Left_half
    Left_half = temp
    print(f"input to round {r+1} : {list_to_string(Left_half)} {list_to_string(Right_half)}")




