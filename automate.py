# -*- coding: utf-8 -*-

def parsare(lines):
    index = 0

    n = int(lines[index].strip())  # cate stari are automatul
    index += 1

    stari = lines[index].strip().split()  # lista cu numele starilor
    index += 1

    m = int(lines[index].strip())  # cate tranzitii avem
    index += 1

    alfabet = set()  # tin minte ce simboluri apar (pentru bonus)
    dictionar = {}
    # structura dictionar:
    # { stare_plecare: { simbol: [stare_dest1, stare_dest2, ...] } }
    # la DFA o sa fie mereu o singura stare destinatie, dar las lista
    # ca sa refolosesc parsarea si la NFA / NFA-lambda

    for _ in range(m):
        trnz = lines[index].strip().split()
        index += 1
        stare_plecare, stare_finala, litera = trnz[0], trnz[1], str(trnz[2])

        # daca litera e scrisa ca lambda (sau varianta ciudata cu Î»), o normalizez
        if litera == "Î»" or litera == "λ":
            litera = "lambda"

        if stare_plecare not in dictionar:
            dictionar[stare_plecare] = {}
        if litera not in dictionar[stare_plecare]:
            dictionar[stare_plecare][litera] = []
        dictionar[stare_plecare][litera].append(stare_finala)

        if litera != 'lambda':
            alfabet.add(litera)  # lambda nu face parte din alfabet

    stare_int = lines[index].strip()  # starea de start
    index += 1

    nr_stari_fin = int(lines[index].strip())  # cate stari finale sunt
    index += 1

    stari_fin = set(lines[index].strip().split())  # multimea starilor finale
    index += 1

    nr_cuvinte = int(lines[index].strip())  # cate cuvinte trebuie verificate
    index += 1

    cuvinte = []
    for _ in range(nr_cuvinte):
        cuvinte.append(lines[index].strip())
        index += 1

    return stari, dictionar, stare_int, stari_fin, cuvinte, alfabet


# ========================== DFA ==========================

def run_dfa(dictionar, stare_int, stari_fin, cuvant):
    stare_curenta = stare_int
    tranzitii_fol = []

    # cazul special: cuvantul gol -> acceptat doar daca q0 e stare finala
    if cuvant == '':
        return stare_curenta in stari_fin, []

    for simbol in cuvant:
        if stare_curenta in dictionar and simbol in dictionar[stare_curenta]:
            dest = dictionar[stare_curenta][simbol][0]  # DFA => o singura destinatie
            tranzitii_fol.append((stare_curenta, simbol, dest))
            stare_curenta = dest
        else:
            return False, tranzitii_fol  # nu exista tranzitie => respins

    acceptat = stare_curenta in stari_fin
    return acceptat, tranzitii_fol


def proc_dfa(fisier_input, fisier_output):
    with open(fisier_input, 'r') as f:
        lines = f.readlines()

    stari, dictionar, stare_int, stari_fin, cuvinte, alfabet = parsare(lines)

    print(f"[DFA] Alfabet: {sorted(alfabet)}")

    rezultate = []
    for cuvant in cuvinte:
        acceptat, tranz_fol = run_dfa(dictionar, stare_int, stari_fin, cuvant)
        rezultate.append("DA" if acceptat else "NU")

        if acceptat:
            print(f"[DFA] Cuvant '{cuvant}' ACCEPTAT. Tranzitii folosite: {tranz_fol}")
        else:
            print(f"[DFA] Cuvant '{cuvant}' RESPINS.")

    with open(fisier_output, 'w') as f:
        f.write(f"{sorted(alfabet)}\n")  # bonus: afisam alfabetul
        for r in rezultate:
            f.write(r + '\n')


# ========================== NFA ==========================

def run_nfa(dictionar, stare_int, stari_fin, cuvant):
    # in loc de o singura stare curenta, tin o multime de stari posibile
    stari_curente = {stare_int}
    tranzitii_fol = []

    if cuvant == '':
        return bool(stari_curente & stari_fin), []

    for simbol in cuvant:
        stari_noi = set()
        tranz_pas = []

        for stare in stari_curente:
            for dest in dictionar.get(stare, {}).get(simbol, []):
                stari_noi.add(dest)
                tranz_pas.append((stare, simbol, dest))

        tranzitii_fol.extend(tranz_pas)
        stari_curente = stari_noi

        if not stari_curente:
            return False, tranzitii_fol  # am ramas fara stari => respins

    acceptat = bool(stari_curente & stari_fin)
    return acceptat, tranzitii_fol


def proc_nfa(fisier_input, fisier_output):
    with open(fisier_input, 'r') as f:
        lines = f.readlines()

    stari, dictionar, stare_int, stari_fin, cuvinte, alfabet = parsare(lines)

    print(f"[NFA] Alfabet: {sorted(alfabet)}")

    rezultate = []
    for cuvant in cuvinte:
        acceptat, tranz_fol = run_nfa(dictionar, stare_int, stari_fin, cuvant)
        rezultate.append("DA" if acceptat else "NU")

        if acceptat:
            print(f"[NFA] Cuvant '{cuvant}' ACCEPTAT. Tranzitii folosite: {tranz_fol}")
        else:
            print(f"[NFA] Cuvant '{cuvant}' RESPINS.")

    with open(fisier_output, 'w') as f:
        f.write(f"{sorted(alfabet)}\n")
        for r in rezultate:
            f.write(r + '\n')


# ======================= NFA-LAMBDA =======================

def lambda_closure(stari_initiale, dictionar):
    # gasesc toate starile in care pot ajunge doar prin tranzitii lambda
    # folosesc o stiva ca sa explorez in adancime
    inchidere = set(stari_initiale)
    stiva = list(stari_initiale)

    while stiva:
        stare_curenta = stiva.pop()
        for dest in dictionar.get(stare_curenta, {}).get('lambda', []):
            if dest not in inchidere:
                inchidere.add(dest)
                stiva.append(dest)

    return inchidere


def run_nfa_lambda(dictionar, stare_int, stari_fin, cuvant):
    # primul pas: lambda-closure pe starea initiala
    # (pot ajunge in alte stari chiar inainte sa citesc primul simbol)
    stari_curente = lambda_closure({stare_int}, dictionar)
    tranzitii_fol = []

    if cuvant == '':
        return bool(stari_curente & stari_fin), []

    for simbol in cuvant:
        stari_dupa_simbol = set()
        tranz_pas = []

        # fac tranzitia pe simbolul curent din fiecare stare posibila
        for stare in stari_curente:
            for dest in dictionar.get(stare, {}).get(simbol, []):
                stari_dupa_simbol.add(dest)
                tranz_pas.append((stare, simbol, dest))

        # dupa fiecare simbol, aplic din nou lambda-closure
        stari_curente = lambda_closure(stari_dupa_simbol, dictionar)
        tranzitii_fol.extend(tranz_pas)

        if not stari_curente:
            return False, tranzitii_fol

    acceptat = bool(stari_curente & stari_fin)
    return acceptat, tranzitii_fol


def proc_nfa_lambda(fisier_input, fisier_output):
    with open(fisier_input, 'r') as f:
        lines = f.readlines()

    stari, dictionar, stare_int, stari_fin, cuvinte, alfabet = parsare(lines)

    print(f"[NFA-λ] Alfabet: {sorted(alfabet)}")

    rezultate = []
    for cuvant in cuvinte:
        acceptat, tranz_fol = run_nfa_lambda(dictionar, stare_int, stari_fin, cuvant)
        rezultate.append("DA" if acceptat else "NU")

        if acceptat:
            print(f"[NFA-λ] Cuvant '{cuvant}' ACCEPTAT. Tranzitii folosite: {tranz_fol}")
        else:
            print(f"[NFA-λ] Cuvant '{cuvant}' RESPINS.")

    with open(fisier_output, 'w') as f:
        f.write(f"{sorted(alfabet)}\n")
        for r in rezultate:
            f.write(r + '\n')


# ========================== MAIN ==========================

proc_dfa('dfa_input.txt', 'dfa_output.txt')
print()
proc_nfa('nfa_input.txt', 'nfa_output.txt')
print()
proc_nfa_lambda('nfa_lambda_input.txt', 'nfa_lambda_output.txt')