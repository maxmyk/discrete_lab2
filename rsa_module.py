"""
Алгоритм RSA обміну ключами та відповідне кодування повідомлень цими ключами.
Для кодування забороняється використовувати сторонні бібліотеки. Алгоритми
обміну ключам та кодування бул розглянуті в лекціях.
"""

from BigPrimeGen import PrimeNumber


class RSA():

    def __init__(self) -> None:
        self.__p = PrimeNumber(128)
        self.__q = PrimeNumber(128)
        self.__keygen()

        self.__sec_key = (self.__d, self.__n)
        self.__pub_key = (self.__e, self.__n)

    def __keygen(self):
        """
        Generates keys
        """
        self.__n = self.__p * self.__q
        self.__pq = (self.__p - 1) * (self.__q - 1)
        self.__e = PrimeNumber(30)
        self.__d = pow(self.__e, -1, mod=self.__pq)

    def encrypt(self, message, key):
        from sys import byteorder
        numbers_form = [ch for ch in message.encode("utf-8", "strict")]
        encode_form = []
        to_encode = []
        block = 0
        while numbers_form != []:
            to_encode.append(bytearray())
            for _ in range(0, 16):
                try:
                    to_encode[block].append(numbers_form.pop(0))
                except IndexError:
                    break
            block += 1
        for elem in to_encode:
            to_encode_int = int.from_bytes(elem, byteorder=byteorder)
            encoded_int = pow(to_encode_int, int(key[0]), int(key[1]))
            encode_form.append(str(encoded_int))
        return ','.join(encode_form)

    def decrypt(self, encode_form):
        from sys import byteorder
        message = b""
        for elem in encode_form.split(','):
            decoded_int = pow(int(elem), self.__d, self.__n)
            decoded_msg_bytes = decoded_int.to_bytes(16, byteorder=byteorder)
            message += decoded_msg_bytes
        return message.decode("utf-8", "strict").strip('\x00')

    def hash(self, string):
        hash = 0
        for i in range(len(string)):
            hash = (hash * 229 ^ ord(string[i]) * 897) & 0xFFFFFFFF
        return hash

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
    enc_form = a.encrypt(
        "hi", a.get_public_key())
    dec_form = a.decrypt(enc_form)
