import sys
# initialize state : 5*5
state =[ [0]*5 for i in range(5)]
# SBox from Ex_5
SBox = [132, 53, 10, 187, 38, 145, 66, 23, 130, 51, 8, 115, 36, 249, 82, 21, 128, 49, 6, 113, 34, 247, 98, 19, 126, 65, 4, 111, 32, 245, 96, 17, 230, 81, 2, 109, 48, 243, 94, 15, 228, 79, 0, 213, 64, 241, 92, 31, 226, 77, 254, 211, 62, 239, 196, 47, 224, 75, 14, 209, 122, 237, 194, 45, 222, 73, 30, 207, 58, 253, 192, 43, 220, 177, 28, 205, 56, 13, 190, 41, 236, 175, 26, 203, 160, 11, 188, 39, 252, 173, 24, 219, 158, 9, 186, 143, 250, 171, 22, 235, 156, 7, 202, 141, 248, 169, 20, 233, 154, 5, 218, 139, 246, 185, 124, 231, 152, 3, 216, 137, 244, 201, 60, 229, 168, 107, 214, 135, 242, 199, 120, 227, 184, 105, 212, 151, 90, 197, 118, 225, 182, 103, 210, 167, 88, 195, 134, 223, 180, 101, 208, 165, 86, 193, 150, 71, 178, 29, 206, 163, 84, 191, 148, 69, 176, 133, 54, 161, 12, 189, 146, 67, 174, 131, 52, 159, 116, 37, 144, 251, 172, 129, 50, 157, 114, 35, 142, 99, 170, 127, 234, 155, 112, 33, 140, 97, 18, 125, 232, 153, 110, 217, 138, 95, 16, 123, 80, 1, 108, 215, 136, 93, 200, 121, 78, 255, 106, 63, 240, 91, 198, 119, 76, 183, 104, 61, 238, 89, 46, 117, 74, 181, 102, 59, 166, 87, 44, 221, 72, 179, 100, 57, 164, 85, 42, 149, 70, 27, 204, 55, 162, 83, 40, 147, 68, 25]

def snum(i):
    # Convert student number to string for indexing
    str_number = str(152125749)

    # Get the ith digit from the end of student number
    digit = int(str_number[-i]) % 5

    # if the result is 0，set it to 1
    result = digit if digit != 0 else 1

    return result


def AES_style_operation():
    global SBox
    global state

    # repeat for six rounds
    for _ in range(6):
        # 1. SubBytes
        for i in range(5):
            for j in range(5):
                state[i][j] = SBox[state[i][j]]
        # 2. ShiftRows
        # row 0 of state: no shift
        # row i of state: rotate left with snum(i) steps (i=1,2,3,4)
        for i in range(1, 5):
            state[i] = state[i][snum(i):] + state[i][:snum(i)]
        # 3. MixColumns
        # matrix derived from my student number
        my_matrix = [[1,5,2,1,2],[5,7,4,9,1],[5,2,1,2,5],[7,4,9,1,5],[2,1,2,5,7]]
        # Multiply the current S modulo 256 with my own matrix
        result_matrix = [[0 for _ in range(5)] for _ in range(5)]
        # my_matrix*state unsure
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    result_matrix[i][j] += my_matrix[i][k] * state[k][j]
        # save results in state
        for i in range(5):
            for j in range(5):
                state[i][j] = result_matrix[i][j] % 256


def read_file_and_convert_to_integers(file_path):
    # read file in 10-byte-block
    block_size = 10
    # count block numbers
    block_count = 0
    global state

    with open(file_path, 'rb') as file:
        # read file in 10-byte-block, put it in chunk
        while True:
            chunk = file.read(block_size)
            # if the end of file is met, chunk is an empty string
            if not chunk:
                break  # End of file

            # Pad the last block with zeros if needed
            if len(chunk) < block_size:
                chunk += bytes([0] * (block_size - len(chunk)))

            # Convert bytes to integers
            integers = [int(byte) % 256 for byte in chunk]
            #print("Block:", integers)



            # Add the first input block as 10 integers to the first two rows of state (initialization/absorptions)
            # Add the first 5 integers into the first row
            for i in range(5):
                state[0][i] = (state[0][i] + integers[i]) % 256
            # Add the next 5 integers into the second row
            for i in range(5):
                state[1][i] = (state[1][i] + integers[5+i]) % 256

            # Do AES-style personalized operations to the matrix, repeating them for six rounds
            AES_style_operation()
            #count the number of blocks
            block_count += 1


def squeeze_output():
    global state
    global num_output
    output = ""
    #print("rounds", int(num_output/10)+1)
    for _ in range(int(num_output/10)+1):
        # 1. squeeze the 10 first bytes from the state
        for i in range(5):
            output += format(state[0][i], '02x')
        for i in range(5):
            output += format(state[1][i], '02x')

        AES_style_operation()

    return output



# Extract command-line arguments
# name of a file
file_name = sys.argv[1] if len(sys.argv) > 1 else None
# number of desired output bytes
num_output = int(sys.argv[2]) if len(sys.argv) > 2 else 0

read_file_and_convert_to_integers(file_name)
#print("num_output", num_output)
#print(squeeze_output())
print(squeeze_output()[:num_output*2])
#print(file_name)
