MorseAlph = { 'A':'.-', 'B':'-...',
              'C':'-.-.', 'D':'-..', 'E':'.',
              'F':'..-.', 'G':'--.', 'H':'....',
              'I':'..', 'J':'.---', 'K':'-.-',
              'L':'.-..', 'M':'--', 'N':'-.',
              'O':'---', 'P':'.--.', 'Q':'--.-',
              'R':'.-.', 'S':'...', 'T':'-',
              'U':'..-', 'V':'...-', 'W':'.--',
              'X':'-..-', 'Y':'-.--', 'Z':'--..',
              '1':'.----', '2':'..---', '3':'...--',
              '4':'....-', '5':'.....', '6':'-....',
              '7':'--...', '8':'---..', '9':'----.',
              '0':'-----', ', ':'--..--', '.':'.-.-.-',
              '?':'..--..', '/':'-..-.', '-':'-....-',
              '(':'-.--.', ')':'-.--.-'}


class Morse:
    @staticmethod
    def encrypt(my_string):
        encoded = ''
        for char in my_string.upper():
            if char != ' ':
                if char in MorseAlph.keys():
                    encoded += MorseAlph[char] + ' '
            else:
                encoded += ' '
        return encoded

    @staticmethod
    def decrypt(my_string):
        my_string += ' '
        decipher = ''
        citext = ''
        for char in my_string:
            if char != ' ':
                i = 0
                citext += char
            else:
                i += 1
                if i == 2 :
                    decipher += ' '
                else:
                    decipher += list(MorseAlph.keys())[list(MorseAlph.values()).index(citext)]
                    citext = ''
        return decipher