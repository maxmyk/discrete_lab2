"""
Алгоритм RSA обміну ключами та відповідне кодування повідомлень цими ключами.
Для кодування забороняється використовувати сторонні бібліотеки. Алгоритми
обміну ключам та кодування бул розглянуті в лекціях.
"""

from random import randint


class RSA():

    def __init__(self) -> None:
        # self.keylen = keylen
        # self.__p = randint(1, self.keylen//2) * 2 - 1
        # self.__q = randint(1, self.keylen//2) * 2 - 1
        self.__p = randint(10 ** 6, 10 ** 12)
        self.__q = randint(10 ** 6, 10 ** 12)
        self.__keygen()

    def __keygen(self):
        """
        Generates keys
        """

        while not prime_checker(self.__p):
            self.__p = randint(10 ** 6, 10 ** 12)

        while not prime_checker(self.__q):
            self.__q = randint(10 ** 6, 10 ** 12)

        self.__n = self.__p * self.__q
        print(self.__p, self.__q)
        self.__pq = (self.__p - 1) * (self.__q - 1)
        print(self.__pq)
        self.__e = randint(1, 200)
        while not prime_checker(self.__e):
            self.__e = randint(1, 200)
        print(self.__e)
        while 1:
            try:
                self.__d = pow(self.__e, -1, mod=self.__pq)
                break
            except ValueError:
                self.__e = randint(1, 200)
                while not prime_checker(self.__e):
                    self.__e = randint(1, 200)

    def encode(self, message):
        numbers_form = [ord(message[i]) for i in range(len(message))]
        encode_form = []
        for elem in numbers_form:
            encode_form.append(str(pow(elem, self.__e, self.__n)))
        return encode_form

        # bin_data = [int(bin(ch)[2:]) for ch in message.encode('utf8')]
        """ bin_data = [bin(ch)[2:] for ch in message.encode('utf8')]
        longest_chr = len(max(bin_data, key=lambda x: len(x)))
        for elem in enumerate(bin_data):
            while len(bin_data[elem[0]]) < longest_chr:
                bin_data[elem[0]]+='2'
            bin_data[elem[0]] = int(bin_data[elem[0]])
        for elem in bin_data:
            encode_form.append(str(pow(elem, self.__e, self.__n)))
        return encode_form """
        # str_data = "".join(bin_data)
        # int_data = int(str_data)
        # return pow(int_data, self.__e, self.__n)
        # bin_data = [int_data**self.__e%self.__n for int_data in bin_data]
        # return bin_data
        # return int_data**self.__e%self.__n

    def decode(self, encode_form):
        messenge = ""
        for elem in encode_form:
            messenge += chr(pow(int(elem), self.__d, self.__n))
        return messenge

    def get_pq(self):
        return self.__p, self.__q

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


def ext_euclidean(a: int, b: int):
    """
    Extended Euclidean algorithm
    """
    oldolds, olds, oldoldt, oldt = 1, 0, 0, 1
    while b != 0:
        q = a // b
        r = a % b
        a = b
        b = r
        s = oldolds - q * olds
        t = oldoldt - q * oldt
        oldolds = olds
        oldoldt = oldt
        olds = s
        oldt = t
    return a, oldolds, oldoldt


def euclidean(a: int, b: int):
    """
    GCD - Euclidean algorithm
    """
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """
    LCM - Lowest common multiplier using GCD
    """
    return a // euclidean(a, b) * b


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


a = RSA()
enc_form = a.encode('Maks and Bodia')
print(enc_form)
dec_form = a.decode(enc_form)
print(dec_form)
# print(ext_euclidean(252, 198))
# 463513
# print(prime_checker(649879456898563))
# print(prime_checker(463513))
# {gcd(a,b)is x, and (oldolds)⋅ a + (oldoldt)⋅b = x}
# a = RSA()
# x, y = a.get_pq()
# print(a.get_pq(), prime_checker(x), prime_checker(y))
