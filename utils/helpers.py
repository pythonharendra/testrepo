import random
import math



def generate_random_number():
    digits = [i for i in range(0, 10)]

    random_str = ""

    for i in range(6):

        index = math.floor(random.random() * 10)
        
        random_str += str(digits[index])
    return random_str



def generate_otp():
    otp=""
    for i in range(6):
        otp+=str(random.randint(1,9))
    return otp 



   
