# Feladatsor – Tron játék Python Turtle segítségével

**Téma:** Python, függvények, változók, halmazok, eseménykezelés és egyszerű játéklogika  
**Ajánlott szint:** kezdő–középhaladó  
**Munkaforma:** egyéni vagy páros munka

## Tanulási célok

A feladatok végére képes leszel:
- megérteni egy több függvényből álló Python-program felépítését;
- felismerni a változók, feltételek, ciklusok, függvények és halmazok szerepét;
- megérteni a billentyűzetes eseménykezelést a Turtle modulban;
- módosítani egy meglévő programot, majd saját funkcióval bővíteni;
- tesztelni és dokumentálni a változtatásaidat.

## Előkészület

1. Nyisd meg a projektet: https://github.com/englert/pythontron
2. Olvasd el a `tron_turtle.py` fájlt, és futtasd a saját gépeden:
   ```bash
   python3 tron_turtle.py
   ```
3. Ha a program nem indul el, ellenőrizd, hogy van-e grafikus asztali környezeted és telepítve van-e a Python Tk támogatása.
4. Módosítás előtt készíts másolatot a fájlról, vagy dolgozz külön Git-ágon.

**Fontos:** először próbáld megérteni a meglévő kódot. Ne egyszerre változtass meg sok mindent: egy módosítás után indítsd újra és teszteld a játékot.

---

## 1. szint – Ismerkedés a programmal

### 1. feladat – A program részei
Keresd meg a kódban az alábbi részeket, és írd le a sorszámukat vagy a függvény nevét!

1. A játékablak létrehozása.
2. A két játékos teknősének létrehozása.
3. A pálya szélének megrajzolása.
4. A pontszám kiírása.
5. Az új menet előkészítése.
6. Az ütközés vizsgálata.
7. A győztes kihirdetése.
8. A billentyűk hozzárendelése a műveletekhez.
9. A program fő eseményciklusa.

### 2. feladat – Változók és konstansok
Magyarázd el saját szavaiddal, mire szolgál az alábbi változó vagy konstans!

- `WIDTH`
- `HEIGHT`
- `STEP`
- `TICK`
- `LIMIT_X`
- `LIMIT_Y`
- `blue_dir`
- `blue_cells`
- `state`
- `score_blue`

Ezután válaszolj: melyik változók tárolnak számot, melyek tárolnak koordinátát, melyek tárolnak több értéket, és melyik jelöli a játék állapotát?

### 3. feladat – A játék állapotai
A program a `state` változóban tárolja a játék állapotát.

1. Keresd meg, hol kapja meg a `state` a `"start"`, `"countdown"`, `"playing"` és `"gameover"` értékeket.
2. Készíts állapotdiagramot vagy felsorolást arról, milyen sorrendben követik egymást ezek az állapotok.
3. Mi történik, ha a játékos Entert nyom meg játék közben? Miért?

### 4. feladat – Függvények
Válassz ki három függvényt, és mindegyikhez írj egy-két mondatos leírást:
- `draw_arena()`
- `draw_hud()`
- `show_start()`
- `reset_round()`
- `set_direction()`
- `finish_round()`
- `next_position()`
- `collides()`
- `move_riders()`
- `tick()`

---

## 2. szint – Értsd meg a mozgást!

### 5. feladat – Koordináták
A Turtle ablakban a koordinátarendszer origója a képernyő közepe.

1. Mit jelent a `(0, 0)` koordináta?
2. Melyik irányba nő az x koordináta?
3. Melyik irányba nő az y koordináta?
4. Mit jelent a `(-1, 0)` irányvektor? És a `(0, 1)`?
5. Számold ki, hogy a `(20, -10)` helyről hová lép a játékos, ha az iránya `(1, 0)`, a `STEP` pedig 10.

### 6. feladat – A `next_position()` függvény
Vizsgáld meg a `next_position(pos, direction)` függvényt!

1. Milyen paramétereket kap?
2. Mit ad vissza?
3. Miért hasznos, hogy a függvény nem mozgatja közvetlenül a teknőst, csak kiszámítja a következő koordinátát?
4. Készíts három saját példát bemenettel és a hozzá tartozó eredménnyel!

### 7. feladat – Billentyűzetes irányítás
Keresd meg a `screen.onkeypress(...)` sorokat!

1. Melyik billentyűkkel irányítható a kék játékos?
2. Melyik billentyűkkel irányítható a piros játékos?
3. Mit csinál a `lambda` a billentyűkezelő sorokban?
4. Miért előnyös külön függvénybe szervezni az irányváltás ellenőrzését?

**Kiegészítés:** rendeld a kék játékoshoz a `T`, `F`, `G`, `H` billentyűket is. Teszteld, hogy a játék a régi billentyűkkel is működik-e!

### 8. feladat – Miért nem fordulhat vissza azonnal?
A `set_direction()` függvény megpróbálja megakadályozni, hogy a játékos azonnal az ellenkező irányba forduljon.

1. Melyik feltétel vizsgálja ezt?
2. Miért lenne problémás az azonnali visszafordulás egy ilyen játékban?
3. Próbáld ki, mi történik, ha ideiglenesen eltávolítod ezt az ellenőrzést. Utána állítsd vissza az eredeti kódot!

---

## 3. szint – Ütközések és adatszerkezetek

### 9. feladat – Miért használunk halmazt?
A program a `blue_cells` és `red_cells` változókban tárolja a játékosok korábbi pozícióit.

1. Mit tárol egy koordinátapár, például `(120, -40)`?
2. Mit jelent a Pythonban a `set` adatszerkezet?
3. Miért hasznos a `set` a már bejárt koordináták tárolására?
4. Mit csinál a `blue_cells.add(bpos)` sor?
5. Miért kell a két játékos korábbi pozícióit külön tárolni?

### 10. feladat – Az ütközésvizsgálat
Olvasd el a `collides(pos, own, other)` függvényt!

1. Milyen kétféle ütközést vizsgál?
2. Miért kapja meg a függvény a saját és a másik játékos koordinátáit is?
3. Mit jelent a `return True` és a `return False`?
4. Mi történik a játékban, ha az egyik játékos ütközik?
5. Mi történik, ha mindkét játékos egyszerre ütközik?

**Tesztelés:** játsszatok legalább három menetet, és jegyezzétek fel, hogy falnak, saját fénycsíknak vagy a másik játékos fénycsíkjának ütközött-e a vesztes!

### 11. feladat – Pontszám
Keresd meg, hol növekszik a `score_blue` és a `score_red` értéke!

1. Mikor kap pontot a kék játékos?
2. Mikor kap pontot a piros játékos?
3. Döntetlen esetén mi történik a pontszámmal?
4. Miért nem szabad minden képkockában növelni a pontszámot?

---

## 4. szint – Módosítsd a játékot!

### 12. feladat – Állítható sebesség
A játék sebességét a `TICK` konstans befolyásolja.

1. Állítsd át az értékét `0.09`-re. Milyen változást tapasztalsz?
2. Próbáld ki a `0.03` értéket is.
3. Írj rövid következtetést arról, hogyan függ össze a `TICK` értéke és a játék sebessége.

**Kihívás:** készíts három nehézségi szintet: könnyű, normál és gyors. A választott szint határozza meg a `TICK` értékét.

### 13. feladat – Saját színvilág
Változtasd meg a játékosok színét és a háttér színét!

- Válassz két jól megkülönböztethető játékosszínt.
- Válassz hozzájuk illő háttérszínt.
- Ellenőrizd, hogy a fénycsíkok jól láthatók maradnak-e.
- A változtatás után készíts képernyőképet a játékról.

### 14. feladat – Játék végi statisztika
Bővítsd a játékot úgy, hogy a menet végén a győztes neve mellett a menet sorszáma is megjelenjen!

Segítség:
1. Hozz létre egy `round_number` változót.
2. Növeld az értékét minden új menet kezdetekor.
3. A `finish_round()` függvényben írd ki az aktuális menet sorszámát.
4. Teszteld, hogy új menet indításakor helyesen változik-e az érték.

### 15. feladat – Rajt előtti visszaszámlálás
A program már tartalmaz háromtól induló visszaszámlálást.

1. Keresd meg a visszaszámlálást megvalósító kódrészt a `tick()` függvényben.
2. Módosítsd úgy, hogy 5-től számoljon vissza.
3. Ellenőrizd, hogy a mozgás csak a „RAJT!” felirat után indul-e el.
4. Magyarázd el, miért használ a program `time.monotonic()` függvényt.

---

## 5. szint – Önálló fejlesztési kihívások

Válassz legalább **egy** feladatot!

### 16. feladat – Szüneteltetés
Készíts szüneteltetést a szóköz billentyűvel. Szünetben egyik játékos se mozogjon, és jelenjen meg a „SZÜNET” felirat. Újabb szóközre folytatódjon a játék.

### 17. feladat – Győzelem több pontig
A játék ne csak egy menetet játsszon. Az nyerje a mérkőzést, aki először eléri az 5 pontot. A végső győzelem után jelenjen meg egy külön üzenet.

### 18. feladat – Kezdőpozíciók és pályaméret
Módosítsd a pálya méretét és a játékosok kezdőpozícióját. Ügyelj arra, hogy mindkét játékos a pályán belül induljon, és legyen elég helyük a mozgáshoz.

### 19. feladat – Saját ötlet
Találj ki egy új funkciót! Például:
- második pályatípus;
- akadályok a pályán;
- egyjátékos mód egyszerű számítógépes ellenféllel;
- a menet végén rövid statisztika;
- játékindítás nehézségi szint kiválasztásával.

A megoldásodhoz készíts rövid leírást arról, mit változtattál, mely függvényeket érintetted, és hogyan tesztelted.

---

## Beadandó

A munkád tartalmazza:

1. A válaszokat az 1–11. feladat kérdéseire.
2. Legalább két működő kódmódosítást a 12–15. feladatok közül.
3. Legalább egy megoldott fejlesztési kihívást a 16–19. feladatok közül.
4. Egy rövid tesztelési naplót legalább három esettel.
5. Egy képernyőképet a módosított játékról.

## Értékelési javaslat – 20 pont

- A kód megértése és a kérdések megválaszolása: **6 pont**
- Két kisebb módosítás helyes megvalósítása: **4 pont**
- Önálló fejlesztési feladat: **6 pont**
- Tesztelés és a változtatások dokumentálása: **2 pont**
- Átlátható, olvasható kód és beszédes változónevek: **2 pont**

**Tanári megjegyzés:** a feladatsor fokozatosan halad a kód olvasásától az önálló fejlesztésig. Az 1–11. feladat elsősorban megértést ellenőriz, a 12–15. feladat kisebb módosításokat gyakoroltat, a 16–19. feladat pedig differenciálásra és tehetséggondozásra is alkalmas.
