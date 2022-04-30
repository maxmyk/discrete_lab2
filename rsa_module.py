"""
Алгоритм RSA обміну ключами та відповідне кодування повідомлень цими ключами.
Для кодування забороняється використовувати сторонні бібліотеки. Алгоритми
обміну ключам та кодування бул розглянуті в лекціях.
"""

from random import randint
from BigPrimeGen import PrimeNumber


class RSA():

    def __init__(self) -> None:
        # self.keylen = keylen
        # self.__p = randint(1, self.keylen//2) * 2 - 1
        # self.__q = randint(1, self.keylen//2) * 2 - 1
        self.__p = PrimeNumber()
        self.__q = PrimeNumber()
        self.__keygen()

        self.__sec_key = (self.__d, self.__n)
        self.__pub_key = (self.__e, self.__n)

    def __keygen(self):
        """
        Generates keys
        """
        self.__n = self.__p * self.__q
        self.__pq = (self.__p - 1) * (self.__q - 1)
        self.__e = randint(1, 200)
        while not prime_checker(self.__e):
            self.__e = randint(1, 200)
        while 1:
            try:
                self.__d = pow(self.__e, -1, mod=self.__pq)
                break
            except ValueError:
                self.__e = randint(1, 200)
                while not prime_checker(self.__e):
                    self.__e = randint(1, 200)

    def encode(self, message):
        numbers_form = [bin(ch)[2:] for ch in message.encode('utf8')]
        longest_chr = len(max(numbers_form, key=lambda x: len(x)))
        for elem in enumerate(numbers_form):
            while len(numbers_form[elem[0]]) < longest_chr:
                numbers_form[elem[0]] = '0'+numbers_form[elem[0]]
        encode_form = []
        numbers_form = ''.join(numbers_form)
        to_encode = []
        for i in range(0, len(numbers_form), longest_chr*2):
            to_encode.append(int(numbers_form[0+i:longest_chr*2+i]))
        for elem in to_encode:
            encode_form.append(str(pow(elem, self.__e, self.__n)))
        return encode_form

    def decode(self, encode_form):
        message = ""
        for elem in encode_form:
            pre_chr = str(pow(int(elem), self.__d, self.__n))
            mem = chr(int(pre_chr[-7:], 2))
            pre_chr = pre_chr[:-7]
            message += chr(int(pre_chr[-7:], 2))+mem
        return message

    def get_public_key(self):
        return self.__pub_key

    """ def generate_signature(self, encoded_msg_digest: bytes):
        int_data = uint_from_bytes(encoded_msg_digest)
        return pow(int_data, self.d, self.n)
    
    def verify_signature(self, digital_signature: int):
        int_data = pow(digital_signature, self.e, self.n)
        return uint_to_bytes(int_data)

    def encrypt(self, binary_data: bytes):
        int_data = uint_from_bytes(binary_data)
        return pow(int_data, self.e, self.n)
        
    def decrypt(self, encrypted_int_data: int):
        int_data = pow(encrypted_int_data, self.d, self.n)
        return uint_to_bytes(int_data) """
# ------------


# def ext_euclidean(a: int, b: int):
#     """
#     Extended Euclidean algorithm
#     """
#     oldolds, olds, oldoldt, oldt = 1, 0, 0, 1
#     while b != 0:
#         q = a // b
#         r = a % b
#         a = b
#         b = r
#         s = oldolds - q * olds
#         t = oldoldt - q * oldt
#         oldolds = olds
#         oldoldt = oldt
#         olds = s
#         oldt = t
#     return a, oldolds, oldoldt


# def euclidean(a: int, b: int):
#     """
#     GCD - Euclidean algorithm
#     """
#     while b != 0:
#         a, b = b, a % b
#     return a


# def lcm(a, b):
#     """
#     LCM - Lowest common multiplier using GCD
#     """
#     return a // euclidean(a, b) * b


# def invmod(a, b):
#     """
#     Modular multiplicative inverse
#     """
#     gcd_num, x, _ = ext_euclidean(a, b)
#     if gcd_num == 1 and x < 0:
#         x += b
#     return x


def prime_checker(num):
    """
    Checks if number is prime
    """
    # if (factorial(num-1)+1) % num == 0:
    #     return True
    # return False
    if num == 0 or num == 1:
        return False
    max_div = int(num**0.5)
    prime = [True for _ in range(max_div + 1)]
    p = 2
    while (p * p <= max_div):
        if prime[p]:
            if num % p == 0:
                return False
            for i in range(p ** 2, max_div + 1, p):
                prime[i] = False
        p += 1
    prime[0] = False
    prime[1] = False
    for p in range(max_div + 1):
        if prime[p]:
            if num % p == 0:
                return False
    return True

if __name__ == '__main__':
    a = RSA()
    enc_form = a.encode('Maks and Bodia')
    # print(enc_form)
    dec_form = a.decode(enc_form)
    print(dec_form)
    # print(a.get_public_key())
    # print(ext_euclidean(252, 198))
    # 463513
    # print(prime_checker(649879456898563))
    # print(prime_checker(463513))
    # {gcd(a,b)is x, and (oldolds)⋅ a + (oldoldt)⋅b = x}
    # a = RSA()
    # x, y = a.get_pq()
    # print(a.get_pq(), prime_checker(x), prime_checker(y))
