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
        numbers_form = []
        for ch in message:
            numbers_form.append(ord(ch))
        encode_str = ''
        ind = 0
        while ind < len(numbers_form):
            temp = str(numbers_form[ind])
            while len(temp) < 4:
                temp = '0' + temp
            encode_str += temp
            ind += 1
        encode_form = ''
        ln = len(str(key[1]))
        last_ind = 0
        for i in range(len(encode_str)):
            if i % ln == 0 and i != 0:
                encode_form += str(pow(int(encode_str[i - ln: i]), int(key[0]), int(key[1]))) + ','
                last_ind = i
        if last_ind == 0:
            encode_form = str(pow(int(encode_str), int(key[0]), int(key[1])))
        else:
            try:
                encode_form += str(pow(int(encode_str[last_ind:]), int(key[0]), int(key[1])))
            except:
                pass
        # encode_form = str(pow(int(encode_str), key[0], key[1]))
        return encode_form.strip(',')

    def decrypt(self, encode_form):
        message = ""
        msg = ''
        for i in encode_form.split(','):
            msg += str(pow(int(i), self.__d, self.__n))
        # msg = str(pow(int(encode_form), self.__d, self.__n))
        count = 0
        last_ind = 0
        for i in range(len(msg) - 1, -1, -1):
            count += 1
            if count == 4:
                message = chr(int(msg[i:i + count])) + message
                last_ind = i
                count = 0
        if last_ind != 0:
            message = chr(int(msg[0:last_ind])) + message
        try:
            if last_ind == 0 and message == '':
                message = chr(int(msg)) + message
        except:
            pass
        return message

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


# if __name__ == '__main__':
#     a = RSA()
#     enc_form = a.encrypt('sadsadsadssafhdjsfhdjkghfjghfjghfjghjfgadsa', a.get_public_key())
#     dec_form = a.decrypt(enc_form)
#     print(dec_form)
