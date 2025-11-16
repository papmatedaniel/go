import random
import os

class Tabla:

    def __init__(self):
        self.tabla = [["." for _ in range(10)] for _ in range(10)]
        self.jatekosok = []
        self.alakzatok = ["X", "O"]

    def kiir(self):
        [print(*i) for i in self.tabla]

    def tablafrissites(self):
        '''Frissíti a tábla állapotát'''
        print(self.objektumszelektalo("X"))


    def mellettekord(self, halmaz):
        mellettielemek = set()
        for i in halmaz:
            mellettielemek.add((i[0], i[1]+1))
            mellettielemek.add((i[0], i[1]-1))
            mellettielemek.add((i[0]+1, i[1]))
            mellettielemek.add((i[0]-1, i[1]))
        return mellettielemek


    def objektumszelektalo(self, karakter):
        lista = self.tabla
        """A bitmapből kigyűjti az adott objektum koordinátáit, 
        és az objektumok koordinátáit listába rakja"""
        objektum_lista = []  #Ide rakjuk a különálló objektumok koordinátáit
        for y in range(len(lista)):  #Végig iterálunk a filon(y tengely)
            for x in range(len(lista[y])): #Végig iterálunk a file akutális során
                if lista[y][x] == karakter:  #Ha a bitmap adott karaktere == a keresett karakterrel(0 vagy 1)
                    objektum_lista.append({(x,y)})  #Új setbe belerakva hozzáadjuk a koordinátát a sorhoz

        while True:
            """
            A ciklus célja, hogy az olyan objektumokat kiszűrje, egybekapcsolja
            amit az előző for ciklus nem tudott egybe kapcsolni
            """
            zaszlo2 = True
            for index_1, elem_1 in enumerate(objektum_lista):  
                for index_2, elem_2 in enumerate(objektum_lista):
                    # Egymással összehasonlítjuk az elemeket
                    if index_2 != index_1 and elem_2 & self.mellettekord(elem_1):  #Ha van metszet, és nem magukkal hasonlítjuk össze
                        elem_1.update(elem_2) #Az első elemet frissítjük a 2 elem hozzáadásával
                        del objektum_lista[index_2]  #Töröljük a második elemet.
                        zaszlo2 = False
                        break
            if zaszlo2:
                return objektum_lista  #Vissza adjuk az objektumok listáját(itt már nincs redundáns objektum elem)

    def nevbeker(self) -> str:
        '''Bekéri a neveket a játékosoktól'''
        nevek = []
        while len(nevek) != 2:
            nev = input("Add meg a neved. (2-7) karakter hosszúságban: ")
            if nev not in nevek:
                nevek.append(nev)
            else:
                print("EZT MÁR MEGADTAD")
        return nevek


    def letesz(self, alakzat):
        '''Bábuk letevése'''
        iranyok = [(0,1), (0,-1), (-1, 0), (1, 0)]
        ellentet = dict()
        if alakzat == "X":
            ellentet["X"] = "O"
        else:
            ellentet["O"] = "X"

        while True:
            elemek = []
            x, y = map(int, input("Add meg a koordinátákat space-el elválasztva: ").split())

            # ŐR 1: Tartományon kívüli koordináták
            if not (0 <= x <= 9 and 0 <= y <= 9):
                print("Túl nagy/kicsi számot adtál meg")
                continue  # Kezdjük újra a ciklust

            # ŐR 2: A mező már foglalt
            if self.tabla[y][x] != ".":
                print("IDE MÁR TETTEK")
                continue  # Kezdjük újra a ciklust

            # Szomszédok összegyűjtése (ez a logika nem változik)
            for x_irany, y_irany in iranyok:
                if (0 <= (x_irany + x) <= 9 and 0 <= (y_irany + y) <= 9):
                    elemek.append(self.tabla[y + y_irany][x + x_irany])

            # ŐR 3: Öngyilkos lépés ellenőrzése
            if elemek.count(ellentet[alakzat]) == len(elemek):
                print("Ez egy öngyilkos lépés, tegyél máshová")
                continue  # Kezdjük újra a ciklust

            # --- SIKERES ESET ("Happy Path") ---
            # Ha idáig eljutottunk, a lépés érvényes.
            self.tabla[y][x] = alakzat
            break  # Kilépünk a (while True) ciklusból

    def levesz(self):
        '''Leveszi az élettelen objektumokat'''
        pass







gotabla = Tabla()
gotabla.jatekosok = gotabla.nevbeker()
os.system("clear") | os.system("cls")
while True:
    for i in range(2):
        print(gotabla.jatekosok[i])
        print(gotabla.kiir())
        gotabla.letesz(gotabla.alakzatok[i])
        # os.system("clear") | os.system("cls")



