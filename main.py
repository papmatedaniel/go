import random


class Tabla:

    def __init__(self):

        # self.tabla = [["." for _ in range(10)] for _ in range(10)]
        self.tabla = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                     ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'X']]
        self.tabla[9][9] = "X"

    def kiir(self):
        [print(*i) for i in self.tabla]


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


gotabla = Tabla()
print(gotabla.kiir())
print(gotabla.objektumszelektalo("."))
print(gotabla.objektumszelektalo("X"))