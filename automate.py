import sys
from collections.abc import dict_items


def parse(lines):
    index = 0

    n = int(lines[index].strip()) # numarul de stari
    index += 1

    stari = lines[index].strip().split() # cele n stari
    index += 1

    m = int(lines[index].strip()) # numarul de tranzitii
    index += 1

    alfabet = set() # alfabetul
    dictionar = {} # procesarea tranzitiilor
    # dictionar pentru tranzitiile automatului de forma {stare_plecare1 { 'litera1' : [stare_finala1, stare_finala2], 'litera2' : [stare_finala1, stare_finala2] }, stare_plecare2 {} } s.a.m.d.
    for _ in range(m):
        trnz = lines[index].strip().split() # impartim in bucati pentru a formata tranzitiile in dictionar
        index += 1
        stare_plecare, stare_finala, litera = trnz[0], trnz[1], str(trnz[2])

        if stare_plecare not in dictionar:
            dictionar[stare_plecare] = {}
        if litera not in dictionar[stare_plecare]:
            dictionar[stare_plecare][litera] = []
        dictionar[stare_plecare][litera].append(stare_finala)

        if litera != 'lambda':
            alfabet.add(litera)

        stare_int = lines[index].strip() # stare initiala
        index += 1

        nr_stari_fin = int(lines[index].strip) # numarul de stari finala
        index += 1

        stari_fin = set(lines[index].strip().split()) # stari finala
        index += 1

        nr_cuvinte = int(lines[index].strip()) # numarul de cuvinte ce trebuie verificate
        index += 1

        cuvinte = [] # lista pentru cuvinte
        for _ in range(nr_cuvinte):
            cuvinte.append(lines[index].strip())
            index += 1

        return stari, dictionar, stare_int, stari_fin, cuvinte, alfabet # final de parsare

def dfa_run():


# de terminat tema asap si de facut repo pe github + de mers la sala si de mers la sport