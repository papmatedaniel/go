import os


class Tabla:

    def __init__(self) -> None:
        self.tabla = [["." for _ in range(10)] for _ in range(10)]
        self.jatekosok = []
        self.alakzatok = ["X", "O"]
        self.iranyok = [(0,1), (0,-1), (-1, 0), (1, 0)]

    def kiir(self) -> None:
        '''Kinyomtatja a tablat'''
        print(" ", end=" ")
        for i in range(10):
            print(i, end=" ")
        print()
        for index in range(len(self.tabla)):
            print(index, *self.tabla[index])


    def mellettekord(self, halmaz: set[tuple[int, int]]) -> set[tuple[int, int]]:
        '''Vissza adja az objektum melletti elemek koordintáit'''
        return {(x+xx, y+yy) for xx, yy in self.iranyok for x, y in halmaz if self.tartomany(x+xx, y+yy)}


    def objektumszelektalo(self, karakter: str) -> list[set[tuple[int, int]]]:
        """A bitmapből kigyűjti az adott objektum koordinátáit, 
        és az objektumok koordinátáit listába rakja"""
        lista = self.tabla
        objektum_lista: list[set[tuple[int, int]]]  = []  #Ide rakjuk a különálló objektumok koordinátáit
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

    def nevbeker(self) -> list[str]:
        '''Bekéri a neveket a játékosoktól'''
        nevek: list[str] = []
        while len(nevek) != 2:
            nev = input("Add meg a neved. (2-7) karakter hosszúságban: ")
            if not 2 <= len(nev) <= 7:
                print("Túl rövid vagy hosszú nevet adtál meg")
                continue
            if nev in nevek:
                print("EZT MÁR MEGADTAD")
                continue
            nevek.append(nev)
        return nevek
    
    def ellentet(self, alakzat: str) -> str:
        return "O" if alakzat == "X" else "X"
    
    def tartomany(self, x: int, y: int) -> bool:
        return 0 <= x <= 9 and 0 <= y <= 9


    def letesz(self, alakzat: str) -> None:
        '''Bábuk letevése'''
        while True:
            x, y = map(int, input("Add meg a koordinátákat space-el elválasztva: ").split())

            # ŐR 1: Tartományon kívüli koordináták
            if not self.tartomany(x, y):
                print("Túl nagy/kicsi számot adtál meg")
                continue  # Kezdjük újra a ciklust

            # ŐR 2: A mező már foglalt
            if self.tabla[y][x] != ".":
                print("IDE MÁR TETTEK")
                continue  # Kezdjük újra a ciklust

        # javítás alatt a függvény

    def levesz(self, alakzat: str) -> bool:
        '''Leveszi az élettelen objektumokat'''
        objektumok = self.objektumszelektalo(self.ellentet(alakzat))
        volt_levetel = False
        for objektum in objektumok:
            szomszedok = self.mellettekord(objektum)

            van_mellette = any(self.tabla[y][x] == "." for x, y in szomszedok)
            if not van_mellette:
                for x, y in objektum:
                    self.tabla[y][x] = "."
                volt_levetel = True
        return volt_levetel

        


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
            # clear()


if __name__ == "__main__":
    main()
