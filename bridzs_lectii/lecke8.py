import sys
from bridzs_doc import validate, build

DEALS = [
    dict(
        title="1. leosztás – 1SZ nyitás: gyenge kézzel passz",
        dealer="Észak",
        N="AQ4 KJ6 Q93 AT72", S="852 Q73 JT4 K863",
        W="763 T942 AK62 Q9", E="KJT9 A85 875 J54",
        auction=["1SZ", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "16 fp, egyenletes elosztás. (15–17 fp.)"),
            ("passz", "Dél 6 fp: 16 + 6 = 22, legfeljebb 17 + 6 = 23. 25 fp-hoz nincs esély. 0–7 fp-tal, 4 lapos vagy hosszú főszín nélkül passzolunk."),
        ],
        lead="♠B (Kelet)",
        play=[
            "Felvevő: Észak. A ♠D üt, a ♠A is ütés.",
            "Üsd ki a ♥A-t: a ♥K, ♥D után két kör ütésed van.",
            "Treff: ♣K, ♣A: Nyugat ♣D-ja leesik. A ♣10-et Kelet ♣B-je üti, de a negyedik treff magas.",
            "2 pikk + 2 kör + 3 treff = 7 ütés. Eredmény: az 1SZ teljesül.",
        ],
        lesson="1SZ-re 0–7 fp-tal passzolunk. Az erős kéz már elmondta az erejét, a gyenge kéz nem licitálhat csak azért, mert van 6 fp-ja.",
    ),
    dict(
        title="2. leosztás – 2SZ meghívás; a nyitó minimális",
        dealer="Észak",
        N="AT5 KQ8 KJ73 Q94", S="KQ7 94 Q852 JT75",
        W="432 A6532 64 AK2", E="J986 JT7 AT9 863",
        auction=["1SZ", "passz", "2SZ", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "15 fp, a nyitó minimuma."),
            ("2SZ", "8–9 fp, meghívás: »Ha a maximumon vagy, menj 3SZ-be.« Dél 8 fp-ja pont ehhez elég."),
            ("passz", "Észak 15 fp + Dél legfeljebb 9 fp = 24. Passz. 16–17 fp-tal 3SZ-t mondana."),
        ],
        lead="♥B (Kelet)",
        play=[
            "Felvevő: Észak. Nyugat a ♥A-val üt, és visszaad kört: a ♥K, ♥D üt. Dél két körrel nem segít, de Észak két ütést kap.",
            "Üsd ki a ♦A-t: a ♦K, ♦D, ♦B három ütés.",
            "♠K, ♠D, ♠A: három pikk ütés. Összesen 8.",
            "Ne próbálj treffet játszani: Nyugat ♣A-ja, ♣K-ja és a kör szín futna. Eredmény: 8 ütés. A 3SZ bukott volna.",
        ],
        lesson="1SZ–2SZ = 8–9 fp meghívás. A nyitó 15 fp-tal passzol, 16–17 fp-tal elfogadja. A gémhez kb. 25 fp kell.",
    ),
    dict(
        title="3. leosztás – 1SZ–3SZ",
        dealer="Észak",
        N="KQ5 AJ3 A962 Q84", S="A83 T72 QJ5 K753",
        W="642 K654 K74 A92", E="JT97 Q98 T83 JT6",
        auction=["1SZ", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "16 fp, egyenletes elosztás."),
            ("3SZ", "Dél 10 fp: 15 + 10 = 25 már biztos gém, de 17 + 10 = 27 még nem szlem. 10–15 fp-tal, 4 lapos vagy hosszú főszín nélkül egyenesen 3SZ."),
        ],
        lead="♠B (Kelet)",
        play=[
            "Felvevő: Észak. ♠D, ♠K, ♠A: három pikk ütés.",
            "Káró impassz: Dél kezéből ♦D, Nyugat kicsit tesz, a ♦D nyer. ♦B, majd a ♦A leejti a ♦K-t, és a ♦9 is magas: 4 káró ütés.",
            "♥A egy ütés.",
            "Treff: a ♣A kiütése után a ♣K, ♣D két ütést hoz.",
            "Vesztők: ♣A és a körök. Eredmény: 10 ütés.",
        ],
        lesson="1SZ–3SZ = 10–15 fp. Ezzel a nyitó passzol: a gém megvan, nincs szükség több licitre, és az ellenfelek semmit sem tudnak meg.",
    ),
    dict(
        title="4. leosztás – Stayman, nincs fit, meghívás",
        dealer="Észak",
        N="KJ6 AQ5 KQ83 Q92", S="Q853 K93 J62 K84",
        W="A2 7642 A54 AJT5", E="T974 JT8 T97 763",
        auction=["1SZ", "passz", "2♣", "passz", "2♦", "passz", "2SZ", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "17 fp, a nyitó maximuma."),
            ("2♣", "Stayman: Dél 4 lapos pikket keres, és 9 fp-ja van. Fit nélkül meghívásra elég."),
            ("2♦", "Nincs 4 lapos főszín."),
            ("2SZ", "8–9 fp meghívás, és nincs fit. A Stayman után a 2SZ nem jelent mást, csak többet tudunk: Dél 4 lapos pikket keresett."),
            ("3SZ", "Észak 17 fp, a maximumon van: elfogadja."),
        ],
        lead="♠10 (Kelet)",
        play=[
            "Felvevő: Észak. Nyugat a ♠A-val üt. A ♠K, ♠B, ♠D három pikk ütés.",
            "Üsd ki a ♦A-t: ♦K, ♦D, ♦B három ütés.",
            "♥A, ♥K, ♥D: három kör ütés. Összesen 9.",
            "Ne bonyolítsd: a treffhez nem kell nyúlni, mert Nyugat ♣A-ja mellé a ♣B, ♣10 is ütést hozna. Eredmény: 9 ütés.",
        ],
        lesson="Stayman nemcsak gém erővel lehetséges: 8–9 fp-tal és 4 lapos főszínnel is mondhatunk 2♣-t, majd 2SZ-vel meghívunk.",
    ),
    dict(
        title="5. leosztás – Stayman: a nyitónak mindkét főszíne megvan",
        dealer="Észak",
        N="AQ53 KJ42 A93 K8", S="KT74 96 KJ2 QJ73",
        W="62 QT73 7654 A42", E="J98 A85 QT8 T965",
        auction=["1SZ", "passz", "2♣", "passz", "2♥", "passz", "3SZ", "passz", "4♠", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "17 fp, 4-4 főszínekkel."),
            ("2♣", "Stayman: Dél 10 fp-tal 4 lapos pikket keres."),
            ("2♥", "4 lapos kör. Két 4 lapos főszínnel a kört mondjuk először. Ez még nem tagadja a pikket!"),
            ("3SZ", "Dél nem emeli a kört, tehát nincs körfit. De miért mondott Staymant? Mert 4 pikkje van."),
            ("4♠", "Észak ezt kikövetkezteti, és a 4-4 pikk fitbe javít."),
        ],
        lead="♣10 (Kelet)",
        play=[
            "Felvevő: Észak. Nyugat a ♣A-val üt, és folytatja: a ♣K és a ♣D, ♣B is magas.",
            "Húzd ki az adukat (♠A, ♠K, ♠D).",
            "Káró impassz: Észak ♦3-at indít Dél ♦KB felé. Ha Kelet kicsit tesz, a ♦B nyer, és nincs káró vesztő.",
            "Kör: Délről a ♥KB felé: Kelet ♥A-ja egy vesztő, a harmadik és negyedik kört Dél lopja.",
            "Vesztők: ♣A, ♥A. Eredmény: 10–11 ütés.",
        ],
        lesson="Ha a válaszadó Staymant mondott, majd 3SZ-t licitál, biztosan van 4 lapos főszíne: a másikat. A nyitó, ha mindkettő megvan, javít arra a színre.",
    ),
    dict(
        title="6. leosztás – Transzfer, majd passz",
        dealer="Észak",
        N="K8 AQ6 AJ53 K942", S="JT7643 85 96 Q73",
        W="Q5 97432 K742 AT", E="A92 KJT QT8 J865",
        auction=["1SZ", "passz", "2♥", "passz", "2♠", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "17 fp, egyenletes elosztás."),
            ("2♥", "Transzfer pikkre: legalább 5 pikk. Az erőről semmit sem mond, lehet teljesen gyenge is."),
            ("2♠", "Kötelező válasz."),
            ("passz", "Dél 3 fp-tal megáll. Ez a transzfer legnagyobb haszna: a 6 lapos pikk ütéseket hoz, míg 1SZ-ben Dél lapjai haszontalanok lennének."),
        ],
        lead="♥B (Kelet)",
        play=[
            "Felvevő: Észak. Az asztal kicsit tesz, Nyugat is, a ♥D üt. ♥A, a harmadik kört az asztalon lopod.",
            "Adu: ♠K: Kelet a ♠A-val üt, majd a ♠D is ütést kap. Dél maradék pikkjei magasak.",
            "Káró: ♦A, majd a harmadik kárót az asztalon lopod, ha még van adud.",
            "Treff: a ♣A egy vesztő, a ♣K és a ♣D ütést hoz.",
            "Vesztők: ♠A, ♠D, egy káró, ♣A. Eredmény: 9 ütés.",
        ],
        lesson="Gyenge kézzel, 5+ lapos főszínnel a transzfer után passzolunk. Így a részfelvétel a jobb, és az erős kéz marad rejtve.",
    ),
    dict(
        title="7. leosztás – Transzfer, majd meghívás",
        dealer="Észak",
        N="AJ5 KT7 KQ4 K863", S="Q73 AJ862 952 J5",
        W="642 Q93 A763 A42", E="KT98 54 JT8 QT97",
        auction=["1SZ", "passz", "2♦", "passz", "2♥", "passz", "2SZ", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "16 fp, egyenletes elosztás."),
            ("2♦", "Transzfer körre: legalább 5 kör."),
            ("2♥", "Kötelező válasz."),
            ("2SZ", "»Pontosan 5 köröm van és 8–9 fp-om. Meghívás.« Délnek 8 fp-ja van."),
            ("4♥", "Észak 16 fp, 3 lapos körrel: 5-3 fit és elég erő → gém. 2 lapos körrel és minimummal passzolna."),
        ],
        lead="♦B (Kelet)",
        play=[
            "Felvevő: Észak. Nyugat a ♦A-val üt, és visszaad kárót: ♦K, ♦D üt.",
            "Adu impassz: Dél felől indíts kis kört Észak ♥K10 felé. Nyugat kicsit tesz, a ♥10 nyer. ♥K, majd az asztal ♥A-ja leejti a ♥D-t.",
            "Pikk: az ♠A után a ♠D felé indíts, és a ♠K egy vesztő.",
            "Treff: a ♣K-val ütsz, a ♣B-t a ♣A viszi, a harmadik treffet az asztalon lopod.",
            "Vesztők: ♦A, ♠K, ♣A. Eredmény: 10 ütés.",
        ],
        lesson="Transzfer után a válaszadó erőt mutathat: 2SZ = 8–9 fp, 3SZ = 10+ fp, mindkettő pontosan 5 lappal. A nyitó dönt a színről és a szintről.",
    ),
    dict(
        title="8. leosztás – 4SZ: mennyiségi meghívás, és a nyitó elfogadja",
        dealer="Észak",
        N="AQ5 KJ3 A94 KT92", S="K82 AQ6 KQ85 Q53",
        W="643 7542 632 AJ4", E="JT97 T98 JT7 876",
        auction=["1SZ", "passz", "4SZ", "passz", "6SZ", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "17 fp, a nyitó maximuma."),
            ("4SZ", "Mennyiségi meghívás: 16–17 fp. Fit nélkül nem RKCB! »Ha a maximumon vagy, mondj 6SZ-t.«"),
            ("6SZ", "Észak 17 fp + Dél legalább 16 fp = 33 fp: kis szlem. 15 fp-tal passzolna, és 16 fp-tal is meggondolná."),
        ],
        lead="♠B (Kelet)",
        play=[
            "Felvevő: Észak. Csak a ♣A hiányzik. 3 pikk és 3 kör ütés biztos.",
            "Káró: ♦D, ♦K, ♦A, és a kárók 3-3-ban vannak: Dél ♦8-a is magas. 4 káró ütés.",
            "Treff: ♣10-et indíts: Kelet kicsit tesz, a ♣D-t Nyugat ♣A-ja üti. Utána a ♣K és a ♣9 is nyer.",
            "3 + 3 + 4 + 2 = 12 ütés. Eredmény: 12 ütés.",
        ],
        lesson="Mennyiségi meghívás: 1SZ–4SZ = 16–17 fp, 2SZ–4SZ = 11–12 fp. A nyitó csak a saját pontjait nézi: minimum = passz, maximum = 6SZ.",
    ),
]

BASICS_8 = [
    ("1SZ nyitás: ", "15–17 fp, egyenletes elosztás. Az 5 lapos szín is belefér."),
    ("Válaszok, 4 lapos vagy hosszú főszín nélkül: ", "0–7 fp = passz; 8–9 fp = 2SZ (meghívás); 10–15 fp = 3SZ; 16–17 fp = 4SZ (mennyiségi meghívás)."),
    ("2♣ = Stayman: ", "4 lapos főszín és 8+ fp. Válaszok: 2♦ = nincs 4 lapos főszín; 2♥ = 4 kör (a pikk is lehet); 2♠ = 4 pikk."),
    ("Stayman után: ", "2SZ = 8–9 fp, 3SZ = 10+ fp, nincs fit. Ha a nyitónak a másik főszíne is megvan, javít rá."),
    ("Transzfer: ", "2♦ = 5+ kör, 2♥ = 5+ pikk. A nyitó kötelezően a jelzett színt mondja."),
    ("Transzfer után: ", "passz = gyenge; 2SZ = 5 lap, 8–9 fp; 3SZ = 5 lap, 10+ fp; 4 a színben = 6+ lap, gém."),
    ("A nyitó dönt: ", "3+ lappal a főszínt, 2 lappal az SZ-t választja; 15 fp = passz a meghívásra, 16–17 fp = elfogadás."),
]

GLOSS_8 = [
    ("mennyiségi meghívás", "quantitative invitation"),
    ("részfelvétel", "partscore"),
]

if __name__ == "__main__":
    validate(DEALS)
    build(DEALS, sys.argv[1], "A 2/1 licitrendszer (Two over One Game Force) – 8. lecke: 8 gyakorló leosztás",
          "A 8. lecke témái", BASICS_8, GLOSS_8)
