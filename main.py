import random
import os

class Tabla:

    def __init__(self) -> None:
        self.tabla = [["." for _ in range(10)] for _ in range(10)]
        self.jatekosok = []
        self.alakzatok = ["X", "O"]

    def kiir(self) -> None:
        '''Kinyomtatja a tablat'''
        print(" ", end=" ")
        for i in range(10):
            print(i, end=" ")
        print()
        for index, elem in enumerate(self.tabla):
            print(index, *self.tabla[index])

    def tablafrissites(self) -> None:
        '''Frissíti a tábla állapotát'''
        print(self.objektumszelektalo("X"))


    def mellettekord(self, halmaz) -> set:
        mellettielemek = set()
        for i in halmaz:
            mellettielemek.add((i[0], i[1]+1))
            mellettielemek.add((i[0], i[1]-1))
            mellettielemek.add((i[0]+1, i[1]))
            mellettielemek.add((i[0]-1, i[1]))
        return mellettielemek


    def objektumszelektalo(self, karakter: str) -> list:
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
            if not 2 <= len(nev) <= 7:
                print("Túl rövid vagy hosszú nevet adtál meg")
                continue
            if  nev in nevek:
                print("EZT MÁR MEGADTAD")
                continue
            nevek.append(nev)
        return nevek
    
    def ellentet(self, alakzat: str) -> dict:
        ellentet = dict()
        if alakzat == "X":
            ellentet["X"] = "O"
        else:
            ellentet["O"] = "X"
        return ellentet[alakzat]


    def letesz(self, alakzat: str) -> None:
        '''Bábuk letevése'''
        iranyok = [(0,1), (0,-1), (-1, 0), (1, 0)]


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
            if elemek.count(self.ellentet(alakzat)) == len(elemek):
                if alakzat == "X":
                    self.tabla[y][x] = "\033[31m" + alakzat + "\033[0m"
                else:
                    self.tabla[y][x] = "\033[34m" + alakzat + "\033[0m"
                

                if not self.levesz(alakzat):
                    print("Ez egy öngyilkos lépés, tegyél máshová")
                    self.tabla[y][x] = "."
                    continue  # Kezdjük újra a ciklust

            # --- SIKERES ESET ("Happy Path") ---
            # Ha idáig eljutottunk, a lépés érvényes.
            if alakzat == "X":
                self.tabla[y][x] = "\033[31m" + alakzat + "\033[0m"
            else:
                self.tabla[y][x] = "\033[34m" + alakzat + "\033[0m"
            break  # Kilépünk a (while True) ciklusból

    def levesz(self, alakzat) -> bool:
        '''Leveszi az élettelen objektumokat'''
        objektumok = self.objektumszelektalo(self.ellentet(alakzat))

        iranyok = [(0,1), (0,-1), (-1, 0), (1, 0)]
        melletti = dict()
        for index, objektum in enumerate(objektumok):
            melletti[index] = False
            zaszlo = False
            for x_irany, y_irany in iranyok:
                for x, y in objektum:
                    if (0 <= (x_irany + x) <= 9 and 0 <= (y_irany + y) <= 9):
                        if self.tabla[y + y_irany][x + x_irany] == ".":
                            melletti[index] = True
                            zaszlo = True
                            break
                if zaszlo:
                    break

        for index, elem in melletti.items():
            if elem == False:
                for x, y in objektumok[index]:
                    self.tabla[y][x] = "."
                return True
        return False

        


def clear():
    if os.name == "nt":      # Windows
        os.system("cls")
    else:                    # Linux, macOS, stb.
        os.system("clear")




def main():
    '''Fő játékciklus'''
    gotabla = Tabla()
    gotabla.jatekosok = gotabla.nevbeker()
    clear()
    while True:
        for alakzat in gotabla.alakzatok:
            print(gotabla.jatekosok[gotabla.alakzatok.index(alakzat)])
            print(gotabla.kiir())
            gotabla.letesz(alakzat)
            clear()


if __name__ == "__main__":
    main()
