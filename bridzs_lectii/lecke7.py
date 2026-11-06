import sys
from bridzs_doc import validate, build

DEALS = [
    dict(
        title="1. leosztás – 2SZ nyitás: nagyon gyenge kézzel passz",
        dealer="Észak",
        N="AQ5 KQ4 AJ92 KJ3", S="973 8652 T74 Q82",
        W="642 JT7 KQ3 AT65", E="KJT8 A93 865 974",
        auction=["2SZ", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, egyenletes elosztás. Az 1SZ (15–17 fp) és a 2♣ (22+ fp) között ez a pontos licit."),
            ("passz", "Dél 2 fp: 20 + 2 = 22, a gémhez kevés. 0–3 fp-tal, hosszú főszín nélkül passzolunk."),
        ],
        lead="♠B (Kelet)",
        play=[
            "Felvevő: Észak. A ♠D üt, a ♠A pedig megmarad: két pikk ütés.",
            "Üsd ki a ♥A-t: a ♥K, ♥D után két kör ütésed van.",
            "Treff: az asztal ♣D-ja és Észak ♣K, ♣B lapjai a ♣A kiütése után két ütést hoznak.",
            "Káró: ♦A, majd a ♦B és a ♦9 elvész Nyugat ♦K-ja és ♦D-ja ellen. A kárók 3-3-ban vannak, ezért a ♦2 a végén magas: két káró ütés.",
            "Eredmény: 8 ütés, a 2SZ teljesül.",
        ],
        lesson="2SZ nyitás után a válaszadó 0–3 fp-tal passzolhat. A nyitó erős, de egyedül nem tud gémet teljesíteni.",
    ),
    dict(
        title="2. leosztás – 2SZ–3SZ",
        dealer="Észak",
        N="KQ4 AQ7 AJ5 KJ63", S="T85 J93 K842 Q52",
        W="AJ2 6542 763 A74", E="9763 KT8 QT9 T98",
        auction=["2SZ", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, egyenletes elosztás."),
            ("3SZ", "Dél 6 fp: 20 + 6 = 26 → gém. 4 lapos vagy hosszú főszíne nincs, ezért nincs mit keresni: egyenesen 3SZ. (4–10 fp-tal ez a válasz.)"),
        ],
        lead="♦D (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♦A-val. A ♦K és a ♦B után a kárók 3-3-ban vannak, így Dél negyedik kárója is magas: 4 káró ütés.",
            "Üsd ki a ♣A-t: ♣K, ♣D, ♣B = 3 treff ütés.",
            "Üsd ki a ♠A-t: a ♠K, ♠D = 2 pikk ütés. A ♥A a tizedik ütés.",
            "Vesztők: ♣A, ♠A, ♥K. Eredmény: 10 ütés.",
        ],
        lesson="2SZ-re 4–10 fp-tal gém a válasz. Először nézd meg, van-e 4 lapos vagy hosszú főszíned; ha nincs, 3SZ.",
    ),
    dict(
        title="3. leosztás – 3♣ Stayman: megvan a 4-4 fit",
        dealer="Észak",
        N="AJ5 KQ82 AQ6 KJ4", S="92 J973 K87 Q532",
        W="7643 A54 5432 A6", E="KQT8 T6 JT9 T987",
        auction=["2SZ", "passz", "3♣", "passz", "3♥", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, egyenletes elosztás."),
            ("3♣", "Stayman, ugyanúgy, mint 1SZ után, csak egy szinttel feljebb: »Van 4 lapos főszíned?« Dél 6 fp-ja elég a gémhez."),
            ("3♥", "4 lapos kör. (3♦ = nincs 4 lapos főszín; 3♠ = 4 pikk, nincs 4 kör.)"),
            ("4♥", "Megvan a 4-4 kör fit és a gém erő."),
        ],
        lead="♠K (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♠A-val. Üsd ki a ♥A-t, és három körben húzd ki az adukat. Délnél marad egy adu.",
            "♠B: Kelet ♠D-ja üt, de a harmadik pikket az asztalon lopod. Ezért jobb a 4♥, mint a 3SZ.",
            "Káró: ♦K, ♦A, ♦D = 3 ütés.",
            "Treff: üsd ki a ♣A-t, utána a ♣K, ♣B, ♣D magas.",
            "Vesztők: ♥A, ♠D, ♣A. Eredmény: 10 ütés.",
        ],
        lesson="2SZ után a 3♣ Stayman: 4 lapos főszínnel és legalább 4 fp-tal keressük a 4-4 fitet. A rövid szín a kezünkben lopást ad, ezért a fit gyakran többet ér, mint a 3SZ.",
    ),
    dict(
        title="4. leosztás – 3♣ Stayman: nincs fit, 3SZ",
        dealer="Észak",
        N="K93 AQ5 AQ82 KQ6", S="QJ64 T82 J93 842",
        W="752 J643 K54 AJ5", E="AT8 K97 T76 T973",
        auction=["2SZ", "passz", "3♣", "passz", "3♦", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, egyenletes elosztás."),
            ("3♣", "Stayman: Dél 4 lapos pikket keres, 4 fp-tal: 20 + 4 = 24, a gém felé megyünk."),
            ("3♦", "Nincs 4 lapos főszín."),
            ("3SZ", "Nincs fit, tehát 3SZ."),
        ],
        lead="♣3 (Kelet, negyedik a legjobb lapjától)",
        play=[
            "Felvevő: Észak. Nyugat a ♣A-val üt, a ♣K és a ♣D után két treff ütésed van.",
            "Üsd ki a ♠A-t a ♠K-val: a ♠D, ♠B és a negyedik pikk magas lesz (3-3 elosztás), és bemenet az asztalra.",
            "Káró impassz az asztalról: ♦B, Nyugat kicsit tesz, a ♦B nyer. ♦9 szintén, majd a ♦A leejti a ♦K-t. 4 káró ütés.",
            "2 treff + 3 pikk + 4 káró = 9 ütés, és a ♥A a tizedik. Eredmény: 10 ütés.",
        ],
        lesson="A Stayman nem kockázatos: ha a nyitónak nincs 4 lapos főszíne, 3♦-t mond, és a válaszadó 3SZ-t licitál. Ehhez legalább 4 fp kell, hogy a gém meglegyen.",
    ),
    dict(
        title="5. leosztás – Transzfer nagyon gyenge kézzel",
        dealer="Észak",
        N="AQ7 K6 AJ4 AQ842", S="83 T97532 962 J5",
        W="6542 Q4 KQT7 K63", E="KJT9 AJ8 853 T97",
        auction=["2SZ", "passz", "3♦", "passz", "3♥", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, 5 treff, egyenletes elosztás."),
            ("3♦", "Transzfer körre: legalább 5 kört ígér, a nyitónak 3♥-t kell mondania. Mindegy, milyen gyenge a kéz!"),
            ("3♥", "Kötelező válasz."),
            ("passz", "Dél 1 fp-tal megáll. A 6 lapos kör itt több ütést hoz, mint a 2SZ: Dél lapjaiból szanzaduban semmi sem lenne."),
        ],
        lead="♠B (Kelet)",
        play=[
            "Felvevő: Észak. A ♠D üt, ♠A, a harmadik pikket az asztalon lopod.",
            "Adu: ♥K, és két adu vesztő jön (♥A, ♥D). Dél maradék körei magasak.",
            "Treff impassz az asztalról: ♣B, Nyugat kicsit tesz, a ♣B nyer. Ha Nyugat a ♣K-t teszi, a ♣A üt, és a ♣D magas.",
            "Vesztők: ♥A, ♥D, két káró. Eredmény: 9–10 ütés.",
        ],
        lesson="Hosszú főszínnel transzfert mondunk, még 0–3 fp-tal is, és utána passzolunk. Így a gyenge kéz aduként hasznos, és az erős kéz a felvevő.",
    ),
    dict(
        title="6. leosztás – Transzfer, majd 3SZ: pontosan 5 lap",
        dealer="Észak",
        N="AK6 K85 KQ3 AJ84", S="QT753 J63 J8 Q52",
        W="842 QT4 A6542 K3", E="J9 A972 T97 T976",
        auction=["2SZ", "passz", "3♥", "passz", "3♠", "passz", "3SZ", "passz", "4♠", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, egyenletes elosztás."),
            ("3♥", "Transzfer pikkre: legalább 5 pikk."),
            ("3♠", "Kötelező válasz."),
            ("3SZ", "»Pontosan 5 pikkem van és gém erőm (6 fp). Válassz: 3SZ vagy 4♠.«"),
            ("4♠", "Északnak 3 pikkje van: megvan az 5-3 fit."),
        ],
        lead="♣10 (Kelet)",
        play=[
            "Felvevő: Észak. Nyugat a ♣K-val üt, te a ♣A-val.",
            "Három körben húzd ki az adukat: ♠A, ♠K, majd az asztal ♠D-ja.",
            "Üsd ki a ♦A-t: a ♦K, ♦D után a harmadik kárót az asztalon lopod.",
            "Treff: ♣B, ♣D, és a negyedik treffet is lophatod az asztalon.",
            "Vesztők: ♥A, egy kör és a ♦A. Eredmény: 10 ütés.",
        ],
        lesson="1SZ-hez hasonlóan: transzfer, majd 3SZ = 5 lap és gém erő. A nyitó dönt: 3 lappal 4-es szintű főszín, 2 lappal passz.",
    ),
    dict(
        title="7. leosztás – 4SZ: mennyiségi meghívás",
        dealer="Észak",
        N="AQ5 KQ4 K63 AQ82", S="KJ4 A76 QJ92 T53",
        W="632 8532 A54 K64", E="T987 JT9 T87 J97",
        auction=["2SZ", "passz", "4SZ", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, a nyitó minimuma."),
            ("4SZ", "Mennyiségi meghívás: 11–12 fp, egyenletes elosztás. Nem kulcslapot kér, mert nincs adu! Jelentése: »Ha a maximumon vagy, licitálj 6SZ-t.«"),
            ("passz", "Észak 20 fp-ja minimum: 20 + 11 = 31 fp, a kis szlemhez (33 fp) kevés. 21 fp-tal 6SZ-t mondana."),
        ],
        lead="♠10 (Kelet)",
        play=[
            "Felvevő: Észak. 3 pikk és 3 kör ütés biztos.",
            "Káró: a ♦K-t Nyugat a ♦A-val üti, utána a ♦D, ♦B, ♦9 magas.",
            "Treff impassz az asztalról: kis treff a ♣AD felé, Nyugat kicsit tesz, a ♣D nyer. A ♣K a harmadik körben elvész.",
            "Vesztők: ♦A, ♣K. Eredmény: 11 ütés. A 6SZ egy ütéssel bukna.",
        ],
        lesson="Fit nélkül a 4SZ nem RKCB, hanem mennyiségi meghívás. A nyitó a saját pontjai szerint dönt: minimum = passz, maximum = 6SZ.",
    ),
    dict(
        title="8. leosztás – 2SZ–6SZ: egyenesen szlem",
        dealer="Észak",
        N="AQ6 KT5 AK94 KJ3", S="K87 AQ9 Q83 Q542",
        W="432 6432 652 A76", E="JT95 J87 JT7 T98",
        auction=["2SZ", "passz", "6SZ", "passz", "passz", "passz"],
        explain=[
            ("2SZ", "20 fp, egyenletes elosztás."),
            ("6SZ", "Dél 13 fp: 20 + 13 = 33 fp, megvan a kis szlem, még a nyitó minimuma mellett is. Főszín fit nincs, ezért nem kell kérdezni. (A 7SZ-hez 37 fp kellene.)"),
        ],
        lead="♠B (Kelet)",
        play=[
            "Felvevő: Észak. Csak a ♣A hiányzik. 3 pikk és 3 kör ütés biztos.",
            "Káró: ♦D, ♦A, ♦K, és a kárók 3-3-ban vannak: Észak negyedik kárója is magas. 4 káró ütés.",
            "Treff: üsd ki a ♣A-t. Utána a ♣K és a ♣B vagy a ♣D két ütést hoz.",
            "3 + 3 + 4 + 2 = 12 ütés. Eredmény: 12 ütés.",
        ],
        lesson="Egyenletes kezekkel a szlem egyszerű számolás: 33 fp = 6SZ, 37 fp = 7SZ. 2SZ-re 13–15 fp-tal közvetlenül 6SZ-t mondunk.",
    ),
]

BASICS_7 = [
    ("2SZ nyitás: ", "20–21 fp, egyenletes elosztás. Az 5 lapos mellékszín vagy főszín is belefér."),
    ("Az SZ erőlépcsői: ", "1SZ második licit 12–14 fp; 1SZ nyitás 15–17 fp; 2SZ második licit 18–19 fp; 2SZ nyitás 20–21 fp; 2♣, majd 2SZ 22–24 fp."),
    ("0–3 fp: ", "passz, de hosszú főszínnel transzfert mondunk, és utána passzolunk."),
    ("4–10 fp: ", "3SZ, ha nincs 4 lapos vagy hosszú főszín."),
    ("3♣ = Stayman: ", "4 lapos főszínt keres, 4+ fp-tal. Válaszok: 3♦ = nincs 4 lapos főszín, 3♥ = 4 kör, 3♠ = 4 pikk."),
    ("Transzfer: ", "3♦ = legalább 5 kör, 3♥ = legalább 5 pikk. A nyitó kötelezően mondja a jelzett színt. Utána 3SZ = 5 lap és gém erő, 4 az adott színben = 6 lap."),
    ("4SZ: ", "fit nélkül mennyiségi meghívás, 11–12 fp. A nyitó 20 fp-tal passzol, 21 fp-tal 6SZ-t mond."),
    ("6SZ: ", "13–15 fp, közvetlen licit. 33 fp a kis szlemhez, 37 fp a nagy szlemhez."),
]

GLOSS_7 = [
    ("mennyiségi meghívás", "quantitative invitation"),
]

if __name__ == "__main__":
    validate(DEALS)
    build(DEALS, sys.argv[1], "A 2/1 licitrendszer (Two over One Game Force) – 7. lecke: 8 gyakorló leosztás",
          "A 7. lecke témái", BASICS_7, GLOSS_7)
