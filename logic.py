import random

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password




def preguntas():
    pregunta = random.randint(0, 2)
    if pregunta== 0:
        return "HEADS"
    else:
        return "TAILS"