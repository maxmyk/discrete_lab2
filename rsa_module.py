"""
Алгоритм RSA обміну ключами та відповідне кодування повідомлень цими ключами.
Для кодування забороняється використовувати сторонні бібліотеки. Алгоритми
обміну ключам та кодування бул розглянуті в лекціях.
"""

from BigPrimeGen import PrimeNumber


class RSA():

    def __init__(self) -> None:
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
        self.__e = PrimeNumber(20)
        self.__d = pow(self.__e, -1, mod=self.__pq)

    def encrypt(self, message, key):
        numbers_form = [bin(ch)[2:] for ch in message.encode('utf8')]
        for elem in enumerate(numbers_form):
            while len(numbers_form[elem[0]]) < 8:
                numbers_form[elem[0]] = '0'+numbers_form[elem[0]]
        encode_form = []
        numbers_form = ''.join(numbers_form)
        to_encode = []
        for i in range(0, len(numbers_form), 8):
            to_encode.append(int(numbers_form[0+i:8+i]))
        for elem in to_encode:
            encode_form.append(str(pow(elem, int(key[0]), int(key[1]))))
        return ','.join(encode_form)

    def decrypt(self, encode_form):
        message = ""
        for elem in encode_form.split(','):
            pre_chr = str(pow(int(elem), self.__d, self.__n))
            message += chr(int(pre_chr[-8:], 2))
        return message
    
    @property
    def e(self):
        return self.__e

    @property
    def n(self):
        return self.__n

    def get_public_key(self):
        return self.__pub_key

# ------------


if __name__ == '__main__':
    a = RSA()
    enc_form = a.encrypt('Maks and Bodia', a.get_public_key())
    dec_form = a.decrypt(enc_form)
    print(dec_form)
