import sys
from bridzs_doc import validate, build

DEALS = [
    dict(
        title="1. leosztás – Gyenge 2♥: rossz illeszkedésnél passz",
        dealer="Észak",
        N="84 KJT963 72 Q95", S="AJ72 5 KQ83 J874",
        W="QT93 A84 AT5 K63", E="K65 Q72 J964 AT2",
        auction=["2♥", "passz", "passz", "passz"],
        explain=[
            ("2♥", "Gyenge kettes: 6 lapos kör, 5–10 fp (itt 6 fp). Észak ezzel a kézzel 1-es szinten nem nyithat."),
            ("passz", "Dél 11 fp-ja szép, de a körben szingli van. 11 + legfeljebb 10 = 21 fp: gémre nincs esély. Új színt mondani értelmetlen, csak rontanánk. Gyenge kettes után a rossz illeszkedés = passz."),
        ],
        lead="♦4 (Kelet)",
        play=[
            "Felvevő: Észak. Az asztalon a ♦D-val próbálkozz: Nyugat a ♦A-val üt.",
            "Vesztők: ♥A, ♥D, ♦A, ♣A, ♣K. Minden más a miénk.",
            "Húzd ki az adukat: a ♥A és a ♥D elvész, a többi 4 kör ütés a miénk.",
            "Ütések: 4 kör + ♠A + ♦K, ♦D (a ♦A után) + a harmadik körben a ♣D. Eredmény: 8 ütés.",
        ],
        lesson="A gyenge kettes után a válaszadó először azt nézi: van-e fit? Fit nélkül még 11–14 fp-tal is általában passz a helyes licit.",
    ),
    dict(
        title="2. leosztás – Gyenge 2♠ és egyenes gém",
        dealer="Észak",
        N="AQJ964 73 T85 62", S="K83 AK5 64 AQ975",
        W="72 8642 A732 KT3", E="T5 QJT9 KQJ9 J84",
        auction=["2♠", "passz", "4♠", "passz", "passz", "passz"],
        explain=[
            ("2♠", "Gyenge kettes: 6 pikk, 7 fp."),
            ("4♠", "Dél 3 lapos fittel és 16 fp-tal tudja, hogy van 9 adu és elég ütés: ♥A, ♥K, ♣A és a pikk szín. Nem kell kérdezni, egyenesen gémet licitál."),
        ],
        lead="♥D (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♥A-val, majd két körben (♠K, ♠A) húzd ki az adukat. Az ellenfeleknél 2-2 az elosztás.",
            "Az asztalon maradjon egy adu! Játssz kárót kétszer: az ellenfelek elviszik, a harmadik kárót az asztalon lopod.",
            "A ♣D-ra nincs impassz: a ♣K Nyugatnál van, a ♣D mögött. A ♣A után a második treffed elvész.",
            "Ütések: 6 pikk + ♥A, ♥K + ♣A + káró lopás = 10. Vesztők: két káró és egy treff.",
        ],
        lesson="Gyenge kettes után a 4♠ (vagy 4♥) lezáró licit: a nyitó passzol. Ha fittel és elég ütéssel látod a gémet, ne kérdezz, licitáld.",
    ),
    dict(
        title="3. leosztás – Gyenge 2♦ és 3SZ: a blokkolás veszélye",
        dealer="Észak",
        N="84 62 KQT973 J96", S="AK5 QJ3 A2 K8742",
        W="QJT97 T94 85 AQT", E="632 AK875 J64 53",
        auction=["2♦", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("2♦", "Gyenge kettes: 6 káró, 6 fp."),
            ("3SZ", "Dél 17 fp, ♦A a partner színében, és minden színben van fogása. Ha Észak kárói futnak, megvan a 9 ütés. Főszín fit nincs, és a 3SZ-hez kevesebb ütés kell, mint az 5♦-hoz."),
        ],
        lead="♠D (Nyugat)",
        play=[
            "Felvevő: Dél. Ütsz a ♠A-val. Északnak a káró szíven kívül nincs bemenete!",
            "A LEGFONTOSABB: először a ♦A-t játszd le, utána kis kárót az asztal ♦K-jához. Ha a ♦2-t játszanád először, a ♦A a kezedben maradna, és elzárná a szín útját.",
            "A kárók 3-2-es elosztásban futnak: 6 ütés. Dobj treffet a kezedből, de tartsd meg a ♠K-t, a ♥DB-t és a ♣K-t.",
            "6 káró + ♠A, ♠K = 8 ütés. A kilencedik jön a ♥D-ból vagy a ♣B-ből, amikor az ellenfelek ütnek. Eredmény: 9 ütés.",
        ],
        lesson="A 3SZ gyenge kettes után is jó gém, ha a partner színe fut. Rövid színben a magas lapot játszd le először, hogy ne zárd el a hosszú színt: ez a blokkolás elkerülése.",
    ),
    dict(
        title="4. leosztás – 2SZ kérdés: a nyitó minimális",
        dealer="Észak",
        N="QJT975 84 Q63 J5", S="K83 AK5 AJ4 T962",
        W="A4 7632 KT98 743", E="62 QJT9 752 AKQ8",
        auction=["2♠", "passz", "2SZ", "passz", "3♠", "passz", "passz", "passz"],
        explain=[
            ("2♠", "Gyenge kettes: 6 pikk, 6 fp."),
            ("2SZ", "Kényszerítő kérdés: »Milyen erős a nyitásod?« Dél 15 fp-ja és 3 lapos fitje van, gém csak akkor lesz, ha Észak a maximum közelében van."),
            ("3♠", "A nyitó színének ismétlése = minimális kéz (5–7 fp)."),
            ("passz", "Dél 15 + Észak legfeljebb 7 = 22 fp. Megállunk."),
        ],
        lead="♣K (Kelet)",
        play=[
            "Felvevő: Észak. Kelet leadja a ♣K-t és a ♣A-t, a harmadik treffet Észak lopja.",
            "Játssz adut: a ♠A elvész, utána minden pikk a miénk (2-2 elosztás).",
            "Káró impassz: Észak ♦3-at indít Dél ♦AB felé. A ♦K Nyugatnál van, így a ♦B veszít, de utána a ♦A és a ♦D üt.",
            "Vesztők: két treff, ♠A, ♦K. Eredmény: pontosan 9 ütés. A 4♠ egy ütéssel bukott volna.",
        ],
        lesson="Gyenge kettes után a 2SZ az egyetlen kényszerítő kérdés (új szín is kényszerítő, de természetes). A nyitó színének ismétlése nemet mond: nincs gém.",
    ),
    dict(
        title="5. leosztás – 2SZ kérdés: maximum, kiegészítő értékkel",
        dealer="Észak",
        N="63 KJT985 84 A72", S="AK5 Q73 KJ52 Q63",
        W="742 62 AT73 JT98", E="QJT98 A4 Q96 K54",
        auction=["2♥", "passz", "2SZ", "passz", "3♣", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("2♥", "Gyenge kettes: 6 kör, 8 fp, tehát a maximum közelében."),
            ("2SZ", "Kérdés: Dél 15 fp-ja és 3 lapos fitje van."),
            ("3♣", "Maximális kéz (8–10 fp), és treffben van ász vagy király. (Új szín a 2SZ után = kiegészítő érték, feature.)"),
            ("4♥", "Dél ♣D-ja most sokat ér: Észak ♣A-ja vagy ♣K-ja mellett ütést hoz. 15 + legalább 8 fp és jó illeszkedés → gém."),
        ],
        lead="♠D (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♠A-val az asztalon, és játssz adut: Kelet a ♥A-val üt, és folytatja a pikket a ♠K-ra.",
            "Húzd ki a maradék adut, majd Észak felől kárót az asztal ♦KB felé, és tedd a ♦B-t: Nyugat a ♦A-val üt, de utána a ♦K magas. Ez egy vesztő.",
            "Treff: a ♣K Keletnél van. Észak felől indíts a ♣D felé: így a ♣D ütést hoz, ha Kelet kicsit tesz.",
            "Vesztők: ♥A, ♦A és a harmadik treff. Eredmény: 10 ütés.",
        ],
        lesson="A 2SZ-re adott válasz: színismétlés = minimum, új szín = maximum ott értékkel, 3SZ = zárt szín (AKD-s 6 lap). A válaszadó így pontosan tudja, illeszkednek-e a lapjai.",
    ),
    dict(
        title="6. leosztás – 2♣ nyitás, 2SZ és Stayman",
        dealer="Észak",
        N="AK5 KQ63 AQ9 AQ7", S="9642 JT84 K5 T85",
        W="73 52 76432 KJ32", E="QJT8 A97 JT8 964",
        auction=["2♣", "passz", "2♦", "passz", "2SZ", "passz", "3♣", "passz", "3♥", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("2♣", "Erős, mesterséges nyitás: 22+ fp vagy nagyon sok ütés. Semmit sem mond a treffről! Észak: 24 fp."),
            ("2♦", "Várakozó licit: »Mondd tovább!« Ez nem mutat kárót és nem mutat erőt. Dél 4 fp-tal is köteles válaszolni, mert a 2♣ kényszerítő."),
            ("2SZ", "22–24 fp, egyenletes elosztás. Ez az egyetlen második licit, amit Dél passzolhat, ha teljesen üres a keze."),
            ("3♣", "Stayman, ugyanúgy, mint 1SZ után, csak egy szinttel feljebb. Dél 4 fp-ja elég: 22 + 4 = 26 fp."),
            ("3♥", "4 lapos kör."),
            ("4♥", "Megvan a 4-4 kör fit és a gém."),
        ],
        lead="♠D (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♠A-val, és játssz adut: a ♥A kiütése után a ♥K, ♥D húzza ki a többit (3-2 elosztás).",
            "Káró: ♦K, majd ♦A és ♦D: három ütés, Dél a ♦D-ra eldobhat egy lapot.",
            "Treff impassz: a ♦K bemenettel Dél kezéből ♣10-et indíts Észak ♣AD felé. A ♣K Nyugatnál van, a ♣D nyer.",
            "Vesztők: ♥A, a harmadik pikk és a harmadik treff. Eredmény: 10 ütés.",
        ],
        lesson="2♣–2♦–2SZ után minden úgy működik, mint 1SZ után: 3♣ = Stayman, 3♦ és 3♥ = transzfer. Néhány pont a válaszadónál már elég a gémhez.",
    ),
    dict(
        title="7. leosztás – 2♣ nyitás és gyenge emelés: 4♥",
        dealer="Észak",
        N="AQ5 AKQ974 AK3 6", S="9742 J63 Q85 874",
        W="K83 52 742 QJT93", E="JT6 T8 JT96 AK52",
        auction=["2♣", "passz", "2♦", "passz", "2♥", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("2♣", "22 fp és 6 jó kör: nagyon erős kéz."),
            ("2♦", "Várakozó licit, Dél 3 fp-ja ellenére."),
            ("2♥", "Természetes, legalább 5 lap, gémig kényszerítő: gém előtt senki sem passzolhat."),
            ("4♥", "A gyors érkezés elve (1. lecke): 3 adu, de semmi más érték. A 3♥ több értéket mutatna, és szlem felé vezetne."),
            ("passz", "Észak tudja, hogy Dél gyenge: a 6♥-hez nem lesz meg a 12 ütés."),
        ],
        lead="♣A (Kelet)",
        play=[
            "Felvevő: Észak. Kelet viszi a ♣A-t, a második treffet lopod.",
            "♥A, ♥K (2-2 elosztás). Az asztalon a ♥B megmarad bemenetnek, de a ♦D is az.",
            "♦3 az asztal ♦D-jához, majd pikk Dél kezéből a ♠AD felé: ha Nyugatnál van a ♠K, a ♠D nyer (impassz).",
            "Vesztők: egy treff és egy pikk. Eredmény: 11 ütés. A 6♥ egy ütéssel bukott volna.",
        ],
        lesson="2♣ után is érvényes a gyors érkezés: az ugrás a gémbe a leggyengébb válasz. Az erős kéz így megáll, nem megy szlembe a semmire.",
    ),
    dict(
        title="8. leosztás – 2♣ nyitás, emelés és szlem",
        dealer="Észak",
        N="AKQJ76 A5 KQ3 A2", S="T95 K63 J84 K853",
        W="42 872 T952 QJ74", E="83 QJT94 A76 T96",
        auction=["2♣", "passz", "2♦", "passz", "2♠", "passz", "3♠", "passz", "4SZ", "passz", "5♦", "passz", "6♠", "passz", "passz", "passz"],
        explain=[
            ("2♣", "23 fp, 6 zárt pikk."),
            ("2♦", "Várakozó licit. Dél 7 fp-ja 8 fp alatt van, ezért nem mutat saját színt."),
            ("2♠", "Természetes, gémig kényszerítő."),
            ("3♠", "Pikk fit, és némi érték. (A 4♠ azt jelentené: fit, de semmi más, ahogy az előző leosztásban.)"),
            ("4SZ", "RKCB: Észak a lassú emelés után a szlemet keresi."),
            ("5♦", "0 vagy 3 kulcslap: itt nyilván 0."),
            ("6♠", "Északnak 4 kulcslapja van, tehát csak a ♦A hiányzik → kis szlem. A nagy szlem nem lehet jó."),
        ],
        lead="♥D (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♥A-val, és húzd ki az adukat. A pikk zárt, 6 ütés.",
            "Üsd ki a ♦A-t a ♦K-val: Kelet viszi, de utána a ♦D már magas.",
            "Ütések: 6 pikk + ♥A, ♥K + ♣A, ♣K + ♦K, ♦D. Dél két királya pont a jó helyen van.",
            "Eredmény: 12 ütés. Csak a ♦A veszít.",
        ],
        lesson="2♣ után a 3♠ és a 4♠ különbsége dönti el a szlemet: 3♠ = van valami, 4♠ = nincs semmi. Utána jön a már ismert RKCB.",
    ),
]

BASICS_3 = [
    ("Gyenge kettes nyitás (2♦, 2♥, 2♠): ", "6 lap, 5–10 fp. A célja az ellenfelek zavarása és a lapunk pontos leírása."),
    ("Válaszok gyenge kettesre: ", "fit nélkül általában passz. Egyszerű emelés (2♠–3♠) = zavarás, nem meghívás. 4♥/4♠ = lezárás. Új szín = 5+ lap, egy körig kényszerítő."),
    ("2SZ válasz: ", "kényszerítő kérdés, kb. 15+ fp és legalább 2–3 lapos fit vagy erős kéz."),
    ("A nyitó válaszai a 2SZ-re: ", "színismétlés = minimum (5–7 fp); új szín = maximum (8–10 fp), ott ász vagy király; 3SZ = zárt szín (AKD)."),
    ("2♣ nyitás: ", "erős, mesterséges, kb. 22+ fp vagy nagyon sok ütés. A partner nem passzolhat."),
    ("2♦ válasz: ", "várakozó licit, gyenge kézzel is kötelező. Saját színt (2♥, 2♠, 3♣, 3♦) csak jó 5 lappal és 8+ fp-tal mondunk."),
    ("A nyitó második licitje: ", "2SZ = 22–24 fp, egyenletes elosztás. Új szín = természetes, gémig kényszerítő; utána 3♠ = fit és érték, 4♠ = fit, de semmi más."),
    ("2♣–2♦–2SZ után: ", "ugyanúgy licitálunk, mint 1SZ után: 3♣ = Stayman, 3♦ = transzfer körre, 3♥ = transzfer pikkre."),
]

GLOSS_3 = [
    ("gyenge kettes", "weak two"),
    ("várakozó licit", "waiting bid"),
    ("kiegészítő érték", "feature"),
]

if __name__ == "__main__":
    validate(DEALS)
    build(DEALS, sys.argv[1], "A 2/1 licitrendszer (Two over One Game Force) – 3. lecke: 8 gyakorló leosztás",
          "A 3. lecke témái", BASICS_3, GLOSS_3)
