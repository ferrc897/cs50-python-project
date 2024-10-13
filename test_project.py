from project import convertirCoord, Bloque

ALTURA_TABLERO = 9
ANCHO_TABLERO = 9
BOMBAS = 10

def test_convertirCoord():
    assert(convertirCoord("a1")) == 0, 0
    assert(convertirCoord("B3")) == 1, 2
