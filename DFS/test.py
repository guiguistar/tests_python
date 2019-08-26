# coding: utf-8

def f(nombre):
    if nombre <= 7:
        return 7
    if nombre <= 11:
        return 11
    if nombre <= 16:
        return 16
    if nombre <= 21:
        return 21
    return 0

def nombre_minimum_bits(nombre):
    return len(bin(nombre)[2:])

def nombre_bits(nombre):
    return f(nombre_minimum_bits(nombre))

def representation(nombre):
    N = nombre_bits(nombre)
    chaine = bin(nombre)[2:]
    
    if N == 7:
        return chaine.rjust(8,'0')
    elif N == 11:
        chaine = chaine.rjust(11,'0')
        return '110' + chaine[:5] + ' 10' + chaine[5:]
    elif N == 16:
        chaine = chaine.rjust(16,'0')
        return '1110' + chaine[:4] + ' 10' + chaine[4:10] + ' 10' + chaine[10:]
    elif N == 21:
        chaine = chaine.rjust(21,'0')
        return '11110' + chaine[:3] + ' 10' + chaine[3:9] + ' 10' + chaine[9:15] + ' 10' + chaine[15:]
    else:
        pass

if __name__ == '__main__':
    print(nombre_bits(0x2000))
    print(nombre_bits(129))
