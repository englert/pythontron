# Python Tron

Kétjátékos Tron-fénycsík játék Pythonban, két megvalósítással.

## 1. Ursina változat

Az Ursina játékmotoros, 3D-s változat indítása:

```bash
python -m pip install -r requirements.txt
python tronursina.py
```

## 2. Turtle változat

A Python beépített `turtle` modulját használó, egyszerűbb 2D-s változat indítása:

```bash
python tron_turtle.py
```

A Turtle-változathoz külön Python-csomag telepítése nem szükséges. Linuxon grafikus asztali környezet és Tk támogatás kell hozzá.

## Irányítás

- **Kék játékos:** W, A, S, D
- **Piros játékos:** nyílbillentyűk
- **ENTER:** indítás / új menet
- **ESC:** kilépés

A játékosoknak kerülniük kell a pálya szélét és mindkét fénycsíkot.
