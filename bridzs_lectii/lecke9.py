import sys
from bridzs_doc import validate, build

# Lesson 9: competitive bidding after a 1♣ / 1♦ opening (East interferes).
DEALS = [
    dict(
        title="1. leosztás – Negatív kontra: 4 lapos kör",
        dealer="Észak",
        N="K5 AQ74 KJ963 Q4", S="862 K985 Q4 KJ73",
        W="T73 T62 T85 A962", E="AQJ94 J3 A72 T85",
        auction=["1♦", "1♠", "kontra", "passz", "2♥", "passz", "passz", "passz"],
        explain=[
            ("1♦", "15 fp, 5 káró, 4 kör. Főszínt csak 5 lappal nyitunk."),
            ("1♠ (Kelet)", "Közbeszólás: 5+ pikk, kb. 8–16 fp."),
            ("kontra", "NEGATÍV KONTRA, nem büntető! Dél 9 fp-ja és 4 köre van. Az 1♥ licitet Kelet elvette, a 2♥ pedig 5 lapot és több erőt ígérne. A kontra azt mondja: »8+ fp, 4 lap a nem licitált főszínben (itt a körben).«"),
            ("2♥", "Északnak 4 köre van, megvan a 4-4 fit. Minimális nyitás (12–15 fp), ezért nem ugrik."),
            ("passz", "Dél 9 fp + Észak 12–15 fp = legfeljebb 24 fp. Gémhez kevés."),
        ],
        lead="♠A (Kelet)",
        play=[
            "Felvevő: Észak. Kelet elviszi a ♠A-t. Utána a ♠K már jó: Kelet a ♠D-t nem viheti el.",
            "Húzd ki az adukat (a kör 3-2 elosztású), majd növeld fel a kárót: a ♦A kiütése után négy káró ütés jön.",
            "A ♣A Nyugatnál van. Dél felől indíts treffet Észak ♣D-ja felé: így a ♣D is ütést visz.",
            "Reális eredmény: 9–10 ütés, a 2♥ teljesül.",
        ],
        lesson="A közbeszólás után a válaszadó kontrája negatív kontra: 4 lapot mutat a nem licitált főszínben. Így a 4-4 kör fit nem vész el.",
    ),
    dict(
        title="2. leosztás – Új szín közbeszólás után: 5 lap",
        dealer="Észak",
        N="K74 Q5 AJ6 KJ932", S="AQ862 763 T85 Q4",
        W="T53 T82 Q943 A76", E="J9 AKJ94 K72 T85",
        auction=["1♣", "1♥", "1♠", "2♥", "2♠", "passz", "passz", "passz"],
        explain=[
            ("1♣", "14 fp, 5 treff."),
            ("1♥ (Kelet)", "Közbeszólás: 5+ kör."),
            ("1♠", "Dél nem kontrázik, hanem licitál: közbeszólás után az új szín 1-es szinten 5+ lapot mutat (6+ fp). 4 lapos pikkel negatív kontrát mondana."),
            ("2♥ (Nyugat)", "Nyugat emeli partnere színét: 3 lapos kör támogatás, gyenge kéz."),
            ("2♠", "Észak tudja, hogy Délnek 5 pikkje van. 3 lapos támogatással nyugodtan emel: 5 + 3 = 8 adu. A licitet nem adjuk át az ellenfélnek!"),
            ("passz", "Dél 8 fp-ja kevés gémhez."),
        ],
        lead="♥8 (Nyugat)",
        play=[
            "Felvevő: Dél. Kelet elviszi a ♥B-t és a ♥A-t (az asztal ♥D-ja leesik). A harmadik kört az asztalon lopod.",
            "Három körben húzd ki az adukat (3-2 elosztás).",
            "Növeld fel a treffet: a ♣A Nyugatnál van. Utána Észak hosszú treffjeire Dél eldobhatja a vesztő kárókat (indítás az asztalra: ♦A).",
            "Reális eredmény: 8–9 ütés, a 2♠ teljesül.",
        ],
        lesson="Közbeszólás után: kontra = 4 lapos főszín, új szín licit = 5+ lap. A nyitó ezért 3 lapos támogatással is emelheti a partner színét.",
    ),
    dict(
        title="3. leosztás – 1SZ válasz közbeszólás után: fogás az ellenfél színében",
        dealer="Észak",
        N="KJ5 82 AQ974 K63", S="Q83 KT6 J5 QJ984",
        W="T7642 753 K82 T7", E="A9 AQJ94 T63 A52",
        auction=["1♦", "1♥", "1SZ", "passz", "passz", "passz"],
        explain=[
            ("1♦", "13 fp, 5 káró."),
            ("1♥ (Kelet)", "Közbeszólás: 5+ kör."),
            ("1SZ", "8–10 fp, egyenletes elosztás, és FOGÁS a körben (♥K 10 x). Nincs 4 lapos pikk (azzal negatív kontrát mondana)."),
            ("passz", "Észak minimális: 13 + legfeljebb 10 = 23 fp, ez nem gém."),
        ],
        lead="♥7 (Nyugat, a partnere színe)",
        play=[
            "Felvevő: Dél. Kelet a ♥B-t teszi, Dél a ♥K-val üt. A ♥K 10 x fogás Kelet ♥A D B mögött ül, ezért ér sokat.",
            "Számold meg az ütéseket: ♥K + négy treff (a ♣A kiütése után) + ♦A, ♦D + egy pikk = 7 ütés. Az ellenfelek: ♣A, ♠A és néhány kör.",
            "Ezért ne kapkodj: először a treffet növeld fel. Káró impassz: Dél felől indíts kárót Észak ♦A D felé – a ♦K Nyugatnál van.",
            "Reális eredmény: 7 ütés, az 1SZ teljesül.",
        ],
        lesson="Közbeszólás után az 1SZ válasz 8–10 fp-t és fogást ígér az ellenfél színében. Fogás nélkül ne licitálj szanzadut!",
    ),
    dict(
        title="4. leosztás – Emelés és versenylicit a 3-as szintig",
        dealer="Észak",
        N="54 AJ5 KQ873 AJ6", S="82 Q63 AJ964 T74",
        W="KT73 T982 T2 Q52", E="AQJ96 K74 5 K983",
        auction=["1♦", "1♠", "2♦", "2♠", "passz", "passz", "3♦", "passz", "passz", "passz"],
        explain=[
            ("1♦", "15 fp, 5 káró."),
            ("1♠ (Kelet)", "Közbeszólás: 5+ pikk."),
            ("2♦", "Egyszerű emelés: 6–10 fp, káró támogatás. Dél gyenge, de a támogatást azonnal mutatja."),
            ("2♠ (Nyugat)", "Nyugat emeli a pikket (4 lapos támogatás)."),
            ("passz (Észak)", "Minimális nyitás, nincs mit hozzátenni. (Észak passza itt nem kényszerítő.)"),
            ("3♦", "Dél számol: 5 káró nála + legalább 4 Északnál = legalább 9 adu. A 9 adu szabálya: 9 aduval 9 ütésre, azaz a 3-as szintig licitálhatunk. Nem hagyjuk az ellenfelet 2♠-ben játszani!"),
        ],
        lead="♠A (Kelet)",
        play=[
            "Felvevő: Észak. Két pikket elvesztesz, a harmadik pikket lopod.",
            "Kör: Észak felől indíts kört Dél ♥D-ja felé. A ♥K Keletnél van, így a ♥D ütést visz.",
            "Treff: Dél felől kétszer indíts treffet Észak ♣A B felé (dupla impassz). A ♣K Keletnél, a ♣D Nyugatnál van: csak egy treffet vesztesz.",
            "Reális eredmény: 8–9 ütés. Ha 9, a 3♦ teljesül. Ha egyszer bukik (−50/−100), az is jobb, mint az ellenfél teljesített 2♠-je (−110).",
        ],
        lesson="Versenylicitben az adu hosszát számold. 8 aduval a 2-es, 9 aduval a 3-as szintig licitálhatsz – akkor is, ha gyenge a kezed.",
    ),
    dict(
        title="5. leosztás – Az ellenfél színének licitje (cue bid)",
        dealer="Észak",
        N="AQ5 K82 J74 KJ63", S="73 AJ5 K96 AT952",
        W="T62 T964 QT32 Q7", E="KJ984 Q73 A85 84",
        auction=["1♣", "1♠", "2♠", "passz", "2SZ", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("1♣", "14 fp, egyenletes elosztás (1SZ-hez gyenge)."),
            ("1♠ (Kelet)", "Közbeszólás: 5+ pikk."),
            ("2♠", "Az ellenfél színének licitje (cue bid): »Treff támogatásom van, és legalább limitemelés ereje (10+ fp).« Kényszerítő. Dél 12 fp, 5 treff, nincs 4 lapos főszíne."),
            ("2SZ", "Minimális nyitás (12–14 fp) és FOGÁS pikkben (♠A D x). Erősebb kézzel (15+) 3SZ-t mondana, fogás nélkül 3♣-t."),
            ("3SZ", "Dél 12 + Észak 12–14 = 24–26 fp, a treff szín hosszú: gém."),
        ],
        lead="♠8 (Kelet)",
        play=[
            "Felvevő: Észak. A ♠A D Kelet ♠K-ja után ül: az első ütést a ♠D viszi, a ♠A pedig megmarad második fogásnak.",
            "Treff: ♣K, majd ♣A. Nyugat ♣D 7-je kettesben leesik: öt treff ütés.",
            "Számolj: 2 pikk + 5 treff + ♥A, ♥K = 9 ütés, a lead elvesztése nélkül. A ♥D Keletnél van, a kör impassz (Észak felől Dél ♥A B felé) a 10. ütés.",
            "Reális eredmény: 9–10 ütés, a 3SZ teljesül.",
        ],
        lesson="Az ellenfél színének licitje (1♣–(1♠)–2♠) erős emelést mutat a partner színében. Ha a nyitónak fogása van, szanzadu felé mehetünk.",
    ),
    dict(
        title="6. leosztás – Rekontra felvételi kontra után",
        dealer="Észak",
        N="Q96 7 J83 AKQT53", S="K7 KQT98 AT74 92",
        W="T532 J542 96 J76", E="AJ84 A63 KQ52 84",
        auction=["1♣", "kontra", "rekontra", "1♥", "passz", "passz", "kontra", "passz", "passz", "passz"],
        explain=[
            ("1♣", "12 fp, 6 treff."),
            ("kontra (Kelet)", "Felvételi kontra: rövid treff, támogatás a többi színhez, nyitóerő."),
            ("rekontra", "Dél: 10+ fp. »Miénk a leosztás!« Utána a kontráink büntetők."),
            ("1♥ (Nyugat)", "Nyugat menekül: 2 fp-ja van, az 1♣ rekontrával sokba kerülne nekik."),
            ("passz (Észak)", "A rekontra után Észak passza kényszerítő: Dél még szól. Észak várja, hogy Dél büntet-e."),
            ("kontra", "BÜNTETŐ kontra: Délnek ♥K D 10 9 8-ja van Nyugat kör színe mögött."),
        ],
        lead="♥7 (Észak – partner büntető kontrája után adut hívunk)",
        play=[
            "Felvevő: Nyugat (1♥ kontrázva). Az adu indítás elveszi az asztal lopásait.",
            "Dél ♥K D 10 9 8-ja négy adu ütést visz. Észak ♣A K-ja, Dél ♦A-ja és ♠K-ja is ütés.",
            "Reális eredmény: Nyugat 4–5 ütést visz, 2–3 bukás kontrázva: 300–500 pont (beliben 500–800).",
        ],
        lesson="Felvételi kontra után a rekontra 10+ fp-t mutat. Ha az ellenfél menekül, büntető kontrával sok pontot szerezhetünk.",
    ),
    dict(
        title="7. leosztás – Az 1SZ közbeszólás büntető kontrája",
        dealer="Észak",
        N="AJ4 Q73 KQT85 93", S="T95 KT984 J2 AQ5",
        W="8632 62 973 J864", E="KQ7 AJ5 A64 KT72",
        auction=["1♦", "1SZ", "kontra", "passz", "passz", "passz"],
        explain=[
            ("1♦", "12 fp, 5 káró."),
            ("1SZ (Kelet)", "15–18 fp, egyenletes elosztás, káró fogással – mint egy 1SZ nyitás."),
            ("kontra", "BÜNTETŐ kontra: 9+ fp. Dél 10 fp + Észak 12+ fp = legalább 22 fp, Keletnél legfeljebb 18. Az erő a miénk!"),
            ("passz (Észak)", "Észak örömmel passzol. Gyenge, hosszú kézzel futna (2♦), de itt jó a kártyája."),
        ],
        lead="♦B (Dél – a partner színe)",
        play=[
            "Felvevő: Kelet (1SZ kontrázva). A ♦A kiütése után Észak négy káró ütést visz (indítás: ♠A).",
            "Dél ♣A D-ja Kelet ♣K-ja mögött ül, Dél ♥K-ja Kelet ♥A B-je mögött: ezek is ütések.",
            "Reális eredmény: Kelet 4–5 ütést visz: 2–3 bukás kontrázva, 300–500 pont (beliben 500–800).",
        ],
        lesson="Ha az ellenfél 1SZ-tel szól közbe a nyitásunk után, a kontra büntető: 9+ fp. A két kéz együtt erősebb, a felvevő rosszul fog járni.",
    ),
    dict(
        title="8. leosztás – Csapdapassz és újranyitó kontra",
        dealer="Észak",
        N="AQ84 KJ6 AJ752 4", S="J73 Q85 K6 KQT98",
        W="T962 T742 T983 2", E="K5 A93 Q4 AJ7653",
        auction=["1♦", "2♣", "passz", "passz", "kontra", "passz", "passz", "passz"],
        explain=[
            ("1♦", "15 fp, 5 káró."),
            ("2♣ (Kelet)", "Közbeszólás 2-es szinten: jó 6 lapos treff."),
            ("passz (Dél)", "CSAPDAPASSZ! Dél ♣K D 10 9 8-ja Kelet treffje mögött ül. Szívesen büntetne, de a kontrája negatív kontra lenne (főszínt mutatna). Ezért passzol és vár."),
            ("passz (Nyugat)", "Nyugatnak nincs pontja."),
            ("kontra", "Újranyitó kontra: Északnak rövid a treffje (szingli). Ha a partner csendben van, a rövid lappal rendelkező nyitó újranyit, hátha Dél csapdapasszt mondott."),
            ("passz (Dél)", "Dél passza a kontrát büntetővé teszi. Ezt várta!"),
        ],
        lead="♣K (Dél – adu indítás)",
        play=[
            "Felvevő: Kelet (2♣ kontrázva). Dél ♣K D 10 9 8-ja négy adu ütést visz.",
            "Mellé: ♠A, ♦A, ♦K és két kör ütés (Kelet ♥A-ja után).",
            "Reális eredmény: Kelet 4–5 ütést visz: 3–4 bukás kontrázva, 500–800 pont (beliben 800–1100). Ez több, mint a 3SZ (400/600).",
        ],
        lesson="Ha a válaszadónak erős lapja van az ellenfél színében, passzol (csapdapassz). Rövid lappal a nyitó kontrával újranyit, és a partner passzal büntet.",
    ),
]

BASICS_9 = [
    ("Negatív kontra: ", "1♦–(1♠)–kontra = 8+ fp, 4 lap a nem licitált főszínben. 1♣–(1♦)–kontra = mindkét főszín. Nem büntető!"),
    ("Új szín, 1SZ: ", "1♣–(1♥)–1♠ = 5+ lap (4 lappal negatív kontra). 1♦–(1♥)–1SZ = 8–10 fp és fogás az ellenfél színében."),
    ("Emelés: ", "1♦–(1♠)–2♦ = 6–10 fp, támogatás. 1♣–(1♠)–2♠ (az ellenfél színének licitje) = 10+ fp és fit."),
    ("A 9 adu szabálya: ", "8 adu = 2-es szint, 9 adu = 3-as szint. Gyenge kézzel is versenyzünk."),
    ("Rekontra és büntető kontra: ", "1♣–(felvételi kontra)–rekontra = 10+ fp, utána a kontráink büntetők. 1♦–(1SZ)–kontra = 9+ fp, büntető."),
    ("Csapdapassz és újranyitó kontra: ", "erős lappal az ellenfél színében a válaszadó passzol. A nyitó rövid lappal kontrával újranyit, a válaszadó passzal büntet."),
    ("Bukás kontrázva: ", "nem beliben 100, 300, 500, 800…; beliben 200, 500, 800, 1100…"),
]

GLOSS_9 = [
    ("csapdapassz", "trap pass"),
    ("újranyitó kontra", "reopening (balancing) double"),
    ("bukás / beliben", "undertrick / vulnerable"),
]

OPP_NOTE = ("A 4. lecke folytatása: Észak 1♣-t vagy 1♦-t nyit, Kelet szól közbe, és Dél (te) válaszol. "
            "A mi licitjeink félkövérek, az ellenfélé mellett zárójelben áll a neve.")

if __name__ == "__main__":
    validate(DEALS)
    build(DEALS, sys.argv[1], "A 2/1 licitrendszer (Two over One Game Force) – 9. lecke: versenylicit 1♣/1♦ nyitás után, 8 gyakorló leosztás",
          "A 9. lecke témái", BASICS_9, GLOSS_9, opp_note=OPP_NOTE)
