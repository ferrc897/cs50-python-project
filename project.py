import random
import re

class Bloque:
    def __init__(self, bomb=False, flag=False, show=False, no_bomba=0):
        self.bomb = bomb
        self.flag = flag
        self.show = show
        self.no_bomba = no_bomba

    def __str__(self):
        if self.flag and not(self.show):
            return "🚩"
        if not(self.show):
            return "🟩"
        if self.show and self.bomb:
            return "💣"
        if self.show and self.no_bomba > 0 and not(self.bomb):
            numeros = ["1️⃣ ", "2️⃣ ", "3️⃣ ", "4️⃣ ", "5️⃣ ", "6️⃣ ", "7️⃣ ", "8️⃣ "]
            return numeros[self.no_bomba - 1]
        if self.show:
            return "🟫"

def elegir_dificultad():
    while True:
        try:
            print("1. Facil")
            print("2. Medio")
            print("3. Dificil")
            dif = input("Escoja la dificultad: ").lower()
            if dif == "1" or dif == "facil":
                return 8,10,10
            elif dif == "2" or dif == "medio":
                return 14,18,40
            elif dif == "3" or dif == "dificil":
                return 20,24,99
            else:
                pass
        except ValueError:
            pass

ALTURA_TABLERO, ANCHO_TABLERO, BOMBAS = elegir_dificultad()

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def main():
    tablero = crear_tablero()
    while True:
        tablero = movimiento(tablero)
        if perder(tablero):
            for i in range(ALTURA_TABLERO):
                    for j in range(ANCHO_TABLERO):
                        if tablero[i][j].bomb:
                            tablero[i][j].show = True
            dibujar_tablero(tablero)
            print("Perdiste :(")
            break
        if ganar(tablero):
            dibujar_tablero(tablero)
            print("Ganaste :)")
            break


def crear_tablero():
    """
    Devuelve el tablero en el que se jugará el juego
    """
    tablero = []
    for i in range(ALTURA_TABLERO):
        fila = []
        for j in range(ANCHO_TABLERO):
            fila.append(Bloque())
        tablero.append(fila)
    return tablero


def movimiento(tablero):
    """
    Recibe el tablero y elije donde revelar un bloque, poner bandera y colocar bombas
    
    """
    dibujar_tablero(tablero)
    while True:
        if primerMovimiento(tablero):
            modo = 1
            break
        try:
            print("Colocar bandera o revelar?")
            print("1. Revelar")
            print("2. Bandera")
            modo = int(input())
            if modo < 1 or modo > 2:
                raise ValueError
            break
        except ValueError:
            pass
    while True:
        try:
            coord = input("Escriba una coordenada: ")
            print()
            x , y = convertirCoord(coord)
            if modo == 1:
                tablero[y][x].show = True
            if modo == 2 and not(tablero[y][x].flag) and not(tablero[y][x].show):
                tablero[y][x].flag = True
            else:
                tablero[y][x].flag = False
            break
        except (IndexError, ValueError):
            pass
    tablero[y][x].no_bomba = contar_bombas(x,y,tablero)
    if primerMovimiento(tablero):
        tablero = setGame(tablero)
    tablero = revelar_bloques(tablero,x,y)
    return tablero



def primerMovimiento(tablero):
    """
    Recibe el tablero y devuelve verdadero si es el primer movimiento y falso si no
    """
    count = 0
    for i in range(ALTURA_TABLERO):
        for j in range(ANCHO_TABLERO):
            if tablero[i][j].bomb:
                count += 1
    if count == 0:
        return True
    else:
        return False
    

def setGame(tablero):
    """
    recibe el tablero y lo devuelve con las bombas colocadas aleatoriamente 
    """
    for i in range(BOMBAS):
        while True:
            try:
                x = random.randint(0, ANCHO_TABLERO - 1)
                y = random.randint(0, ALTURA_TABLERO - 1)
                if tablero[y][x].bomb:
                    raise ValueError
                elif revelado(tablero, x, y):
                    raise ValueError
                else:
                    break
            except ValueError:
                pass
        tablero[y][x].bomb = True
    return tablero

def num_flags(tablero):
    count = 0
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j].flag:
                count += 1
    return count


def dibujar_tablero(tablero):
    """""
    Recibe el tablero e imprime cada elemento que lo conforma
    """""
    print(f"🚩 {BOMBAS - num_flags(tablero)}")
    print()
    print(" ", end = "")
    for i in range(ANCHO_TABLERO):
        print(" "+letters[i], end="")
    print()
    for i in range(ALTURA_TABLERO):
        if i < 9:
            print(i + 1,end=" ")
        else:
            print(i+1,end="")
        for j in range(ANCHO_TABLERO):
            print(tablero[i][j], end="")
        print()
    

def convertirCoord(coord):
    """""
    Recibe las coordenas y devuelve números enteros para convertir el bloque de la matriz en una bandera o revelarlo
    """""

    matches = re.search(r"^[a-z][1-9][0-9]?$", coord)
    if not(matches):
        raise ValueError
    coord = list(coord)
    if len(coord) == 2:
        x,y = coord[0], coord[1]
    else:
        x,y = coord[0], coord[1] + coord[2]
    y = int(y) - 1
    if x.lower() in letters:
        x = letters.index(x.lower())
    else:
        raise ValueError
    if y < 0 or y > ALTURA_TABLERO:
        raise ValueError
    return x, y


def revelado(tablero, x, y):
    """
    Recibe el tablero, la coordenada x y y para devolver si hay algun bloque revelado alrededor de donde se quiere colocar la bomba
    """
    for i in range(-1, 2):
        try:
            if tablero[y - 1][x + i].show:
                return True
        except IndexError:
            pass
    for i in range(-1, 2):
        try:
            if tablero[y][x + i].show:
                return True
        except IndexError:
            pass
    for i in range(-1, 2):
        try:
            if tablero[y + 1][x + i].show:
                return True
        except IndexError:
            pass
    return False


def contar_bombas(x,y,tablero):
    """
    recibe las coordenadas x,y y el tablero y Cuenta las bombas alrededor de un bloque
    """
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            try:
                if y+i < 0 or x+j < 0:
                    raise ValueError
                if tablero[y+i][x+j].bomb:
                    count += 1
            except(ValueError, IndexError):
                pass
    return count

            

def perder(tablero):
    """
    Recible el tablero y checa si se ha revelado un bloque, en dado caso devuelve verdadero y se acaba el juego
    """
    for i in range(ALTURA_TABLERO):
        for j in range(ANCHO_TABLERO):
            if tablero[i][j].bomb and tablero[i][j].show:
                return True


def ganar(tablero):
    count = 0
    for i in range(ALTURA_TABLERO):
        for j in range(ANCHO_TABLERO):
            if tablero[i][j].show:
                count += 1
    if count == ALTURA_TABLERO * ANCHO_TABLERO - BOMBAS:
        return True


def revelar_bloques(tablero, x, y):
    if tablero[y][x].no_bomba == 0:
        for i in range(y, ALTURA_TABLERO):
            for j in range(x,ANCHO_TABLERO):
                tablero[i][j].show = True
                tablero[i][j].no_bomba = contar_bombas(j,i,tablero)
                if tablero[i][j].no_bomba > 0:
                    break
            if tablero[i][j].no_bomba > 0:
                break
        
        for j in range(x,ANCHO_TABLERO):
            for i in range(y,ALTURA_TABLERO):
                tablero[i][j].show = True
                tablero[i][j].no_bomba = contar_bombas(j,i,tablero)
                if tablero[i][j].no_bomba > 0:
                    break
            if tablero[i][j].no_bomba > 0:
                break

        for i in range(y, 0,-1):
            for j in range(x,ANCHO_TABLERO):
                tablero[i][j].show = True
                tablero[i][j].no_bomba = contar_bombas(j,i,tablero)
                if tablero[i][j].no_bomba > 0:
                    break
            if tablero[i][j].no_bomba > 0:
                break
        
        for j in range(x,0,-1):
            for i in range(y,ALTURA_TABLERO):
                tablero[i][j].show = True
                tablero[i][j].no_bomba = contar_bombas(j,i,tablero)
                if tablero[i][j].no_bomba > 0:
                    break
            if tablero[i][j].no_bomba > 0:
                break
    return tablero


if __name__ == "__main__":
    main()