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
        numbers_form = [ch for ch in message.encode('utf8')]
        encode_form = []
        to_encode = []
        block = 0
        while numbers_form != []:
            to_encode.append(bytearray())
            for _ in range(0, 156):
                try:
                    to_encode[block].append(numbers_form.pop(0))
                except IndexError:
                    break
            block +=1
        for elem in to_encode:
            encode_form.append(str(pow(int.from_bytes(elem, byteorder='big'), int(key[0]), int(key[1]))))
        return ','.join(encode_form)

    def decrypt(self, encode_form):
        message = ""
        for elem in encode_form.split(','):
            pre_chr = pow(int(elem), self.__d, self.__n)
            pre_chr = pre_chr.to_bytes(156, 'big')
            for elem in pre_chr:
                if elem != 0:
                    message += chr(elem)
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
