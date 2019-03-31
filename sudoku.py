# Karol Perec
import random
import numpy
import copy
import itertools
import matplotlib.pyplot as plt


def zaladuj_plansze(nazwa_pliku):
    plik = open(nazwa_pliku, 'r')
    plansza = [[0] * 9 for _ in range(9)]

    i = 0
    for linia in plik:
        plansza[i] = linia.split()
        i += 1
        if i==9:
            break

    indeksy_nieustalone = []
    for i in range(9):
        indeksy = []
        for j in range(9):
            plansza[i][j] = int(plansza[i][j])
            if plansza[i][j] == 0:
                indeksy.append(j)
        indeksy_nieustalone.append(indeksy)

    plik.close()
    return plansza, indeksy_nieustalone


def nadpisz_plansze(nazwa_pliku, plansza):
    plik = open(nazwa_pliku, 'w')
    for i in range(9):
        indeksy = []
        for j in range(9):
            plik.write(str(plansza[i][j]) + ' ')
        plik.write('\n')
    plik.close()


def inicjalizacja(rozmiar_roju, plansza):
    roj = []

    for _ in range(rozmiar_roju):
        czastka = copy.deepcopy(plansza)
        for i in range(9):
            permutacja = numpy.random.permutation([1, 2, 3, 4, 5, 6, 7, 8, 9])
            j = 0
            for cyfra in permutacja:
                if cyfra in czastka[i]:
                    continue
                else:
                    while (czastka[i][j] != 0):
                        j += 1
                    czastka[i][j] = cyfra
        roj.append(czastka)

    return roj


def funkcja_dostosowania(roj):
    dostosowanie_roju = []
    for czastka in roj:
        dostosowanie = 0
        for i in range(9):
            dostosowanie += len(set(czastka[i]))

        for i in range(9):
            dostosowanie += len(set([col[i] for col in czastka]))

        for i in range(3):
            for j in range(3):
                kwadrat = [czastka[y][x] for y in range(3*i, 3*i+3) for x in range(3*j, 3*j+3)]
                dostosowanie += len(set(kwadrat))

        dostosowanie_roju.append(dostosowanie)

    return dostosowanie_roju


def swap(wiersz, wartosc, swap_index):
    swap_index_2 = wiersz.index(wartosc)
    wiersz[swap_index], wiersz[swap_index_2] = wiersz[swap_index_2], wiersz[swap_index]
    return wiersz


def kombinacja_wypukla(roj, nlc, glc, parametr_poznawczy, parametr_zbiorowy, rozmiar_roju):
    roj_ = copy.deepcopy(roj)
    nlc_ = copy.deepcopy(nlc)
    glc_ = copy.deepcopy(glc)

    for r in range(rozmiar_roju):
        for i in range(9):
            maska = [0] * 9
            for j in range(9):              #losowanie maski
                losowanie = random.random()
                if losowanie < parametr_zbiorowy:
                    maska[j] = 3
                elif losowanie >= (1-parametr_poznawczy):
                    maska[j] = 2
                else:
                    maska[j] = 1

            for swap_index in range(9):
                if maska[swap_index] == 1:
                    wartosc = roj_[r][i][swap_index]
                    nlc_[r][i] = swap(nlc_[r][i], wartosc, swap_index)
                    glc_[i] = swap(glc_[i], wartosc, swap_index)
                elif maska[swap_index] == 2:
                    wartosc = nlc_[r][i][swap_index]
                    roj_[r][i] = swap(roj_[r][i], wartosc, swap_index)
                    glc_[i] = swap(glc_[i], wartosc, swap_index)
                elif maska[swap_index] == 3:
                    wartosc = glc_[i][swap_index]
                    roj_[r][i] = swap(roj_[r][i], wartosc, swap_index)
                    nlc_[r][i] = swap(nlc_[r][i], wartosc, swap_index)

    return roj_


def mutacja(roj, indeksy_nieustalone, prawdopodobienstwo_mutacji):
    for czastka in roj:
        for i in range(9):
            if random.random() < prawdopodobienstwo_mutacji:
                index1, index2 = random.sample(indeksy_nieustalone[i], 2)
                czastka[i][index1], czastka[i][index2] = czastka[i][index2], czastka[i][index1]

    return roj


def mutacja2(roj, indeksy_nieustalone, prawdopodobienstwo_mutacji, plansza):
    for czastka in roj:
        for i in range(9):
            if random.random() < prawdopodobienstwo_mutacji:
                mozliwe_kombinacje = []
                kombinacje = itertools.combinations(indeksy_nieustalone[i], 2)

                for swap_index in kombinacje:
                    if mozliwy_swap(i, swap_index,czastka[i][swap_index[0]], czastka[i][swap_index[1]],plansza)==True:
                        mozliwe_kombinacje.append(list(swap_index))

                if mozliwe_kombinacje != []:
                    index1, index2 = random.choice(mozliwe_kombinacje)
                    czastka[i][index1], czastka[i][index2] = czastka[i][index2], czastka[i][index1]

    return roj

def mutacja2_rev(roj, indeksy_nieustalone, prawdopodobienstwo_mutacji, plansza):
    for czastka in roj:
        for i in range(8, -1, -1):
            if random.random() < prawdopodobienstwo_mutacji:
                mozliwe_kombinacje = []
                kombinacje = itertools.combinations(indeksy_nieustalone[i], 2)

                for swap_index in kombinacje:
                    if mozliwy_swap(i, swap_index,czastka[i][swap_index[0]], czastka[i][swap_index[1]],plansza)==True:
                        mozliwe_kombinacje.append(list(swap_index))

                if mozliwe_kombinacje != []:
                    index1, index2 = random.choice(mozliwe_kombinacje)
                    czastka[i][index1], czastka[i][index2] = czastka[i][index2], czastka[i][index1]

    return roj


def mozliwy_swap(nr_wiersza, swap_index, wartosc1, wartosc2, plansza):
    plansza_ = copy.deepcopy(plansza)
    plansza_[nr_wiersza][swap_index[0]] = wartosc2
    plansza_[nr_wiersza][swap_index[1]] = wartosc1

    if len(set([col[swap_index[0]] for col in plansza_]))\
            == len(set([col[swap_index[0]] for col in plansza])):
        return False
    if len(set([col[swap_index[1]] for col in plansza_]))\
            == len(set([col[swap_index[1]] for col in plansza])):
        return False

    if nr_wiersza<3:
        i=0
    elif nr_wiersza>5:
        i=2
    else:
        i=1

    if swap_index[0]<3:
        j=0
    elif swap_index[0]>5:
        j=2
    else:
        j=1

    if len(set([plansza_[y1][x1] for y1 in range(3 * i, 3 * i + 3) for x1 in range(3 * j, 3 * j + 3)]))\
        == len(set([plansza[y2][x2] for y2 in range(3 * i, 3 * i + 3) for x2 in range(3 * j, 3 * j + 3)])):
        return False

    if swap_index[1]<3:
        j=0
    elif swap_index[1]>5:
        j=2
    else:
        j=1

    if len(set([plansza_[y1][x1] for y1 in range(3 * i, 3 * i + 3) for x1 in range(3 * j, 3 * j + 3)])) \
            == len(set([plansza[y2][x2] for y2 in range(3 * i, 3 * i + 3) for x2 in range(3 * j, 3 * j + 3)])):
        return False

    return True


def aktualizacja_nlc(roj, nlc, dostosowanie_nlc, rozmiar_roju):
    dostosowanie_roju = funkcja_dostosowania(roj)
    for i in range(rozmiar_roju):
        if (dostosowanie_roju[i] >= dostosowanie_nlc[i]):
            nlc[i] = roj[i]
            dostosowanie_nlc[i] = dostosowanie_roju[i]

    return nlc, dostosowanie_nlc


def aktualizacja_glc(nlc, dostosowanie_nlc):
    glc_index = int(numpy.argmax(dostosowanie_nlc))
    glc = nlc[glc_index]
    dostosowanie_glc = dostosowanie_nlc[glc_index]

    return glc, dostosowanie_glc

def konczaca_mutacja(glc_):
    indeksy_zduplikowanych = []

    glc = copy.deepcopy(glc_)

    for i in range(9):
        kolumna = [col[i] for col in glc]
        if len(set(kolumna)) != 9:
            duplikat = set([x for x in kolumna if kolumna.count(x) > 1])

            for j in range(9):
                if glc[j][i] == list(duplikat)[0]:
                    indeks_zduplikowanego = [j, i]
                    indeksy_zduplikowanych.append(indeks_zduplikowanego)
    kolumna0 = [col[0] for col in indeksy_zduplikowanych]
    szukany_indeks = list(set([it for it in kolumna0 if kolumna0.count(it) > 1]))



    if szukany_indeks != []:
        szuk_ind = []
        for i in range(len(indeksy_zduplikowanych)):
            if indeksy_zduplikowanych[i][0] == szukany_indeks[0]:
                szuk_ind.append(indeksy_zduplikowanych[i])

        glc[szuk_ind[0][0]][szuk_ind[0][1]], glc[szuk_ind[1][0]][szuk_ind[1][1]] \
            = glc[szuk_ind[1][0]][szuk_ind[1][1]], glc[szuk_ind[0][0]][szuk_ind[0][1]]

    elif glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[2][1]]==glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[0][1]]:
            glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[0][1]], glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[2][1]] \
                = glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[2][1]], glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[0][1]]
            glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[0][1]], glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[2][1]] \
                = glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[2][1]], glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[0][1]]

    elif glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[3][1]]==glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[0][1]]:
        glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[0][1]], glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[3][1]] \
            = glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[3][1]], glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[0][1]]
        glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[0][1]], glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[3][1]] \
            = glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[3][1]], glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[0][1]]

    elif glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[2][1]]==glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[1][1]]:
        glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[1][1]], glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[2][1]] \
            = glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[2][1]], glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[1][1]]
        glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[1][1]], glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[2][1]] \
            = glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[2][1]], glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[1][1]]

    elif glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[3][1]]==glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[1][1]]:
        glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[1][1]], glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[3][1]] \
            = glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[2][1]], glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[1][1]]
        glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[1][1]], glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[3][1]] \
            = glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[3][1]], glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[1][1]]
    else:
        szuk_ind2 = []
        sprawdzane_indeksy = [[kolumna0[0],glc[kolumna0[0]].index(glc[indeksy_zduplikowanych[2][0]][indeksy_zduplikowanych[2][1]])],
                              [kolumna0[1],glc[kolumna0[1]].index(glc[indeksy_zduplikowanych[3][0]][indeksy_zduplikowanych[3][1]])],
                              [kolumna0[2],glc[kolumna0[2]].index(glc[indeksy_zduplikowanych[0][0]][indeksy_zduplikowanych[0][1]])],
                              [kolumna0[3],glc[kolumna0[3]].index(glc[indeksy_zduplikowanych[1][0]][indeksy_zduplikowanych[1][1]])]]

        kolumna1 = [col[1] for col in sprawdzane_indeksy]

        szukany_indeks2 = list(set([it for it in kolumna1 if kolumna1.count(it) > 1]))
        if szukany_indeks2 != []:
            for i in range(len(sprawdzane_indeksy)):
                if sprawdzane_indeksy[i][1] == szukany_indeks2[0]:
                    szuk_ind2.append(sprawdzane_indeksy[i])
                    szuk_ind2.append([indeksy_zduplikowanych[i][0], indeksy_zduplikowanych[i][1]])
        else:
            return glc_

        glc[szuk_ind2[0][0]][szuk_ind2[0][1]], glc[szuk_ind2[1][0]][szuk_ind2[1][1]] \
            = glc[szuk_ind2[1][0]][szuk_ind2[1][1]], glc[szuk_ind2[0][0]][szuk_ind2[0][1]]
        glc[szuk_ind2[2][0]][szuk_ind2[2][1]], glc[szuk_ind2[3][0]][szuk_ind2[3][1]] \
            = glc[szuk_ind2[3][0]][szuk_ind2[3][1]], glc[szuk_ind2[2][0]][szuk_ind2[2][1]]

    if funkcja_dostosowania([glc])[0] != 243:
        return glc_
    else:
        return glc



if __name__ == '__main__':

    nazwa_pliku_planszy = input("Podaj nazwę pliku z planszą: ")
    rozmiar_roju = int(input("Rozmiar roju (optymalna wartość: 100): "))
    prawdopodobienstwo_mutacji = float(input("Prawdopodobieństwo mutacji [0.0-1.0] (optymalna wartość: 0.5): "))
    liczba_iteracji = int(input("Maksymalna liczba iteracji (optymalna wartość: 1000): "))
    parametr_poznawczy = float(input("Parametr zbiorowy fi1 [0.0-1.0] (optymalna wartość: 0.15): ")) # parametr poznawczy (kognitywny) - jak ufa nlc
    parametr_zbiorowy = float(input("Parametr zbiorowy fi2 [0.0-" + str(1-parametr_poznawczy) + "] (optymalna wartość: 0.85): ")) # parametr zbiorowy (socjalny) - jak ufa ngc
    print("\n")
    parametr_inercji = (1 - parametr_zbiorowy - parametr_poznawczy) # parametr inercji - jak bardzo ufa swojej aktualnej pozycji

    #inicjalizacja algorytmu
    najlepsze_dostosowania = []
    wektor_iteracji = []

    plansza, indeksy_nieustalone = zaladuj_plansze(nazwa_pliku_planszy)
    roj = inicjalizacja(rozmiar_roju, plansza)
    nlc = copy.deepcopy(roj)
    dostosowanie_nlc = funkcja_dostosowania(nlc)
    glc, dostosowanie_glc = aktualizacja_glc(nlc, dostosowanie_nlc)

    for iteracja in range(liczba_iteracji):
        roj = kombinacja_wypukla(roj, nlc, glc, parametr_poznawczy, parametr_zbiorowy, rozmiar_roju)
        roj = mutacja2(roj, indeksy_nieustalone, prawdopodobienstwo_mutacji, plansza)
        nlc, dostosowanie_nlc = aktualizacja_nlc(roj, nlc, dostosowanie_nlc, rozmiar_roju)
        glc, dostosowanie_glc = aktualizacja_glc(nlc, dostosowanie_nlc)

        if dostosowanie_glc >= 241:
            if dostosowanie_glc != 243:
                glc = konczaca_mutacja(glc)
                if funkcja_dostosowania([glc])[0] != 243:
                    continue
                print("Iteracja numer " + str(iteracja+1) + " | Funkcja dostosowania najlepszej czastki: 243")
                najlepsze_dostosowania.append(243)
                wektor_iteracji.append(int(iteracja+1))
                print('\n Znaleziono rozwiązanie: ')
                for i in range(9):
                    print(glc[i])
                break
            print("Iteracja numer " + str(iteracja + 1) + " | Funkcja dostosowania najlepszej czastki: 243")
            najlepsze_dostosowania.append(dostosowanie_glc)
            wektor_iteracji.append(iteracja + 1)
            print('\n Znaleziono rozwiązanie: ')
            for i in range(9):
                print(glc[i])
            break

        print("Iteracja numer " + str(iteracja + 1) + " | Funkcja dostosowania najlepszej czastki: "
              + str(dostosowanie_glc))
        najlepsze_dostosowania.append(dostosowanie_glc)
        wektor_iteracji.append(iteracja+1)

    if funkcja_dostosowania([glc])[0] != 243:
        print('\n Nie znaleziono pełnego rozwiązania: ')
        for i in range(9):
            print(glc[i])

    plt.figure(1)
    plt.plot(wektor_iteracji, najlepsze_dostosowania, 'k-')
    plt.xlabel('Iteracja algorytmu')
    plt.ylabel('Funkcja dostosowania najlepszej czastki')

    plt.xlim(1, wektor_iteracji[-1])
    plt.ylim(najlepsze_dostosowania[0], 243)
    plt.show()

    opcja = input("Czy nadpisać plik rozwiązaniem? [t/n]: ")
    if opcja=="t":
        nadpisz_plansze(nazwa_pliku_planszy, glc)
