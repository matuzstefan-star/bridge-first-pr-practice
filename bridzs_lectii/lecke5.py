import sys
from bridzs_doc import validate, build

DEALS = [
    dict(
        title="1. leosztás – 1♦ nyitás 5-4 elosztással: 2♣ második licit",
        dealer="Észak",
        N="K7 Q5 AQT84 K652", S="Q94 KJ963 J72 83",
        W="T632 T72 K3 AQJ4", E="AJ85 A84 965 T97",
        auction=["1♦", "passz", "1♥", "passz", "2♣", "passz", "2♦", "passz", "passz", "passz"],
        explain=[
            ("1♦", "14 fp, 5 káró és 4 treff. Mindig a hosszabb mellékszínt nyitjuk."),
            ("1♥", "7 fp, 5 kör: új szín 1-es szinten."),
            ("2♣", "Új szín 2-es szinten: 12–16 fp, legalább 4 treff, és a káró hosszabb. Nem kényszerítő."),
            ("2♦", "Preferencia: Dél 3 kárót és 2 treffet tart, ezért a kárót választja. Nem mutat erőt, 7 fp-tal nincs több mondanivalója."),
            ("passz", "Észak nem tud többet: nincs kör fit, és a 21 fp kevés a gémhez."),
        ],
        lead="♣10 (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♣K-val, Nyugat ♣B-je felett.",
            "♥5 az asztal ♥K-ja felé: Kelet a ♥A-val üt. Így az asztal körei felállnak.",
            "Adu impassz az asztalról: ♦B, Nyugat kicsit tesz, a ♦B nyer. Utána a ♦A leejti a ♦K-t.",
            "A ♠K-t Kelet ♠A-ja üti, de a ♠D már magas. Az asztal hosszú köreire Észak eldobja a vesztő treffjeit.",
            "Vesztők: ♠A, ♥A, egy-két treff. Eredmény: 9–10 ütés.",
        ],
        lesson="5-4 elosztással a hosszabb színt nyitjuk, és a rövidebbet mondjuk második licitként. A partner ilyenkor csak választ a két szín közül: ez a preferencia.",
    ),
    dict(
        title="2. leosztás – 3-3 mellékszínekkel 1♣; válasz 1♦",
        dealer="Észak",
        N="KJ52 A74 Q83 K62", S="96 Q53 KJT74 Q97",
        W="QT73 JT98 96 AJ5", E="A84 K62 A52 T843",
        auction=["1♣", "passz", "1♦", "passz", "1♠", "passz", "1SZ", "passz", "passz", "passz"],
        explain=[
            ("1♣", "13 fp. 3-3 mellékszínekkel mindig 1♣-t nyitunk. (4-4 mellékszínekkel 1♦ a nyitás.)"),
            ("1♦", "8 fp, 5 káró, nincs 4 lapos főszín."),
            ("1♠", "A nyitó 4 lapos pikkjét 1-es szinten mutatja meg. Így nem marad el a 4-4 fit. Ez nem mutat extra erőt."),
            ("1SZ", "Dél nem emel pikket, és a kárót sem ismétli. 6–10 fp, kör fogása van (♥D)."),
            ("passz", "Észak 13 fp + Dél legfeljebb 10 fp: a gém nincs meg."),
        ],
        lead="♥B (Nyugat)",
        play=[
            "Felvevő: Dél. Az asztal kicsit tesz. Ha Kelet a ♥K-val üt, Dél kicsit dob, így a ♥D és a ♥A is ütés marad.",
            "Először a kárót növeld fel: Kelet a ♦A-val üt, utána négy káró ütésed van.",
            "Számolás: 4 káró + ♥A, ♥D + ♠K + ♣K = 8 ütés.",
            "Vesztők: ♦A, ♥K, ♠A, ♣A és még egy. Eredmény: 7–8 ütés.",
        ],
        lesson="3-3 mellékszínnel 1♣, 4-4-gyel 1♦. Az 1♦ válasz után a nyitó 1-es szinten megmutatja 4 lapos főszínét. A főszín fit a legfontosabb.",
    ),
    dict(
        title="3. leosztás – 1SZ válasz mellékszínre: nem kényszerítő",
        dealer="Észak",
        N="K72 Q85 A4 AJ964", S="Q84 K73 J96 T852",
        W="AJ53 964 QT8 K73", E="T96 AJT2 K7532 Q",
        auction=["1♣", "passz", "1SZ", "passz", "passz", "passz"],
        explain=[
            ("1♣", "14 fp, 5 treff, egyenletes elosztás."),
            ("1SZ", "6–10 fp, nincs 4 lapos főszín. Ez NEM az a kényszerítő 1SZ, amit az 1. leckében tanultál: az csak főszín nyitás után érvényes!"),
            ("passz", "Észak passzolhat. 14 + legfeljebb 10 = 24 fp: nincs gém."),
        ],
        lead="♠3 (Nyugat, negyedik a legjobb lapjától)",
        play=[
            "Felvevő: Dél. Az asztal kicsit tesz, Kelet a ♠10-et, a ♠D üt.",
            "Treff: az asztal ♣A-ja leejti Kelet szingli ♣D-ját. Utána a ♣B-t Nyugat ♣K-ja üti.",
            "A ♣K után a többi treff már magas, és a ♦A bemenet az asztalra. Összesen 4 treff ütés.",
            "4 treff + ♦A + ♠D, ♠K = 7 ütés. Eredmény: az 1SZ teljesül.",
        ],
        lesson="Főszín nyitás után az 1SZ kényszerítő (6–12 fp), mellékszín nyitás után nem (6–10 fp). Ne keverd össze a kettőt!",
    ),
    dict(
        title="4. leosztás – Egyszerű emelés mellékszínben",
        dealer="Észak",
        N="64 K5 AQT84 KJ72", S="Q83 742 K962 Q85",
        W="J752 AJT83 3 AT4", E="AKT9 Q96 J75 963",
        auction=["1♦", "passz", "2♦", "passz", "passz", "passz"],
        explain=[
            ("1♦", "13 fp, 5 káró, 4 treff."),
            ("2♦", "Egyszerű emelés: 6–9 fp, legalább 4 káró, nincs 4 lapos főszín. Ha lenne 4 lapos főszíne, azt mondaná először."),
            ("passz", "13 + legfeljebb 9 = 22 fp. Észak minimális, passzol. A 3SZ-hez nincs elég erő."),
        ],
        lead="♠A (Kelet)",
        play=[
            "Felvevő: Észak. Kelet leadja a ♠A-t és a ♠K-t, utána az asztal ♠D-ja magas.",
            "Adu: ♦K, ♦A, ♦D. Kelet három kárója (a ♦B is) leesik, nincs káró vesztő.",
            "Kör: Délről indíts a ♥K felé. Ha Nyugat kicsit tesz, a ♥K nyer. A második kört elveszted, a harmadikat lopod.",
            "Treff: üsd ki a ♣A-t a ♣D-val, utána a ♣K, ♣B és a negyedik treff is magas.",
            "Vesztők: ♠A, ♠K, ♥A, ♣A. Eredmény: 9 ütés.",
        ],
        lesson="Mellékszín emelés előtt mindig nézd meg a főszíneket: az emelés azt is jelenti, hogy nincs 4 lapos főszínünk.",
    ),
    dict(
        title="5. leosztás – Limitemelés mellékszínben, majd 3SZ",
        dealer="Észak",
        N="AJ7 QJ5 K84 K942", S="95 K63 Q72 AJ863",
        W="432 T984 AT95 QT", E="KQT86 A72 J63 75",
        auction=["1♣", "passz", "3♣", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("1♣", "14 fp, 4 treff, egyenletes elosztás."),
            ("3♣", "Limitemelés: 10–11 fp, legalább 5 treff, nincs 4 lapos főszín. Meghívás."),
            ("3SZ", "Észak elfogadja: 14 + 10 = 24 fp, jó treffekkel. Minden színben van fogása. A 3SZ 9 ütés, az 5♣ 11 ütés: ezért a mellékszín fit után is gyakran a 3SZ a cél."),
        ],
        lead="♠K (Kelet)",
        play=[
            "Felvevő: Észak. Engedd át a ♠K-t! Ha Kelet folytatja, a ♠A üt, és a ♠B lesz a következő fogásod.",
            "Treff: ♣K, ♣A: Nyugat ♣D-ja és ♣10-e leesik, öt treff ütésed van.",
            "Üsd ki a ♥A-t: a ♥K, ♥D megmarad. A ♦K is ütést hoz, ha a ♦A már elment.",
            "Vesztők: ♠K, ♥A, ♦A. Eredmény: 9–10 ütés.",
        ],
        lesson="Mellékszín fit és gém erő: először a 3SZ-re gondolj, mert ahhoz kevesebb ütés kell, mint az 5♣-hoz vagy az 5♦-hoz.",
    ),
    dict(
        title="6. leosztás – 2SZ válasz: meghívás",
        dealer="Észak",
        N="K82 K73 AQ864 Q9", S="A74 QJ5 K3 J8642",
        W="QJT93 A82 T97 75", E="65 T964 J52 AKT3",
        auction=["1♦", "passz", "2SZ", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("1♦", "14 fp, 5 káró. 1SZ-hez (15–17) gyenge."),
            ("2SZ", "11–12 fp, egyenletes elosztás, nincs 4 lapos főszín. Meghívás: »Ha nem vagy minimális, menj gémbe.« (A 2♣ gém forsz lenne, ahhoz 12–13+ fp kell.)"),
            ("3SZ", "Észak 14 fp + Dél 11–12 fp = 25–26 fp, és jó kárói vannak: elfogadja."),
        ],
        lead="♠D (Nyugat)",
        play=[
            "Felvevő: Dél. Üss a ♠A-val a kezedben: a ♠K bemenet marad az asztalra.",
            "Káró: ♦K, majd kis káró a ♦A-hoz és a ♦D-hoz. A kárók 3-3-ban vannak, mind az öt ütés.",
            "A ♥K után a ♥D, ♥B-t is felnöveled: Nyugat a ♥A-val üthet.",
            "5 káró + ♠A, ♠K + 2 kör = 9 ütés. Eredmény: 9–10 ütés.",
        ],
        lesson="1♣/1♦ után a 2SZ válasz 11–12 fp meghívás, a 3SZ válasz 13–15 fp lezárás. Mindkettő nemet mond a 4 lapos főszínre.",
    ),
    dict(
        title="7. leosztás – 3SZ válasz: egyenesen gém",
        dealer="Észak",
        N="QJ2 K85 A4 AT972", S="K94 AJ3 KT5 Q864",
        W="876 T972 QJ98 K3", E="AT53 Q64 7632 J5",
        auction=["1♣", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("1♣", "14 fp, 5 treff."),
            ("3SZ", "13–15 fp, egyenletes elosztás, nincs 4 lapos főszín, és mindenhol van fogás. Dél tudja, hogy van gém, és azt is, hogy nincs főszín fit."),
            ("passz", "14 + legfeljebb 15 = 29 fp: szlemhez kevés."),
        ],
        lead="♦D (Nyugat)",
        play=[
            "Felvevő: Dél. Üss a ♦K-val.",
            "Treff: ♣D, Nyugat kicsit tesz, az asztal ♣A-ja üt, majd a következő treffre leesik a ♣K. Öt treff ütés.",
            "5 treff + ♦A, ♦K + ♥A, ♥K = 9 ütés, a pikkhez hozzá sem kell nyúlni.",
            "Ha a ♠A-t is kiütöd, további két pikk ütés jön. Eredmény: 10–11 ütés.",
        ],
        lesson="Ha tudod a célt, ne csinálj sok licitet: a 3SZ a legrövidebb út, és az ellenfelek nem kapnak információt.",
    ),
    dict(
        title="8. leosztás – A válaszadó második licitje: ugrás a saját színben",
        dealer="Észak",
        N="K84 J6 AJ93 KQ52", S="73 KQT984 Q5 A86",
        W="QJT65 75 T86 T97", E="A92 A32 K742 J43",
        auction=["1♦", "passz", "1♥", "passz", "1SZ", "passz", "3♥", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("1♦", "14 fp, 4-4 mellékszínekkel: 1♦."),
            ("1♥", "6 lapos kör, 11 fp."),
            ("1SZ", "12–14 fp, egyenletes elosztás, nincs 4 lapos kör."),
            ("3♥", "Ugrás a saját színben: 6 jó kör és 10–12 fp, meghívás. (A 2♥ gyengébb lenne, 6–9 fp. A 4♥ már gém erő.)"),
            ("4♥", "Észak a maximumon van (14 fp), a ♥B is hasznos: elfogadja."),
        ],
        lead="♠D (Nyugat)",
        play=[
            "Felvevő: Dél. Kelet a ♠A-val üt. A ♠K már magas lesz az asztalon.",
            "Üsd ki a ♥A-t, és három körben húzd ki az adukat.",
            "Káró: az asztalról indíts a ♦D felé: Kelet ♦K-ja egy vesztő, a harmadik kárót lopod.",
            "Treff: ♣A, ♣K, ♣D, és a negyedik treff is magas (3-3 elosztás).",
            "Vesztők: ♠A, ♥A, ♦K. Eredmény: 10–11 ütés.",
        ],
        lesson="A válaszadó második licitje is erőt mutat: színismétlés 2-es szinten = gyenge, ugrás = meghívás, gém = elég erő. A nyitó ebből dönt.",
    ),
]

BASICS_5 = [
    ("Melyik mellékszín? ", "A hosszabb. 3-3 esetén 1♣, 4-4 esetén 1♦, 5-5 esetén 1♦."),
    ("Válasz 1-es szinten: ", "6+ fp, 4+ lap. A 4 lapos főszín az első (2. lecke). 1♣–1♦ = 4+ káró, nincs 4 lapos főszín."),
    ("1SZ válasz: ", "6–10 fp, nincs 4 lapos főszín. Mellékszín nyitás után NEM kényszerítő."),
    ("Egyszerű emelés: ", "1♦–2♦ = 6–9 fp, 4+ lap; 1♣–2♣ = 6–9 fp, 5+ lap. Nincs 4 lapos főszín."),
    ("Limitemelés: ", "1♣–3♣, 1♦–3♦ = 10–11 fp, 5+ lap, nincs 4 lapos főszín. Meghívás."),
    ("SZ válaszok: ", "2SZ = 11–12 fp (meghívás), 3SZ = 13–15 fp. Egyenletes elosztás, nincs 4 lapos főszín."),
    ("A nyitó új színe 2-es szinten: ", "1♦–1♥–2♣ = 12–16 fp, a káró hosszabb. Nem kényszerítő; a partner választ."),
    ("A válaszadó második licitje: ", "színismétlés 2-es szinten = 6–9 fp, ugrás = 10–12 fp (meghívás)."),
]

GLOSS_5 = [
    ("preferencia", "preference (choosing between partner's suits)"),
    ("meghívás", "invitation"),
    ("limitemelés", "limit raise"),
]

if __name__ == "__main__":
    validate(DEALS)
    build(DEALS, sys.argv[1], "A 2/1 licitrendszer (Two over One Game Force) – 5. lecke: 8 gyakorló leosztás",
          "Az 5. lecke témái", BASICS_5, GLOSS_5)
