# [A1 - Agent Lecții Bridge] Sesiunea din 2026-11-06: donele Lecțiilor 3–8

## Ce s-a făcut
1. **Lecția 3** (8 done, `bridzs_lectii/lecke3.py`): deschideri slabe de 2 (pas la misfit, 4♠ direct, 3SZ cu deblocarea ♦A, 2SZ cu răspuns minim și cu feature), 2♣ forte (2♦ de așteptare, 2SZ + Stayman, fast arrival 4♥, ridicare 3♠ + RKCB + 6♠).
2. **Lecția 4** (8 done, `bridzs_lectii/lecke4.py`): licitație competitivă: 2/1 nu mai e GF după intervenție, contră negativă, cue-bid ca ridicare forte, ridicare slabă cu sărit (regula celor 9 atuuri), recontră și contră de penalizare, intervenția lui Sud, contră de informație, 1SZ în intervenție cu transfer.
3. Imagini `Lapok_Lecke_3`, `Lapok_Lecke_4` și export pe Desktop (`Bridzs lectii\Lectia 3`, `Lectia 4`).
4. `bridzs_doc.build` are parametrul `opp_note` (textul despre adversari din introducere), iar `cards.py` include Lecțiile 3–4.

5. **Lecția 5** (`lecke5.py`): deschiderile 1♣/1♦ și răspunsurile (2♣ în 5-4, 3-3 minore → 1♣, 1SZ neforcing, ridicare simplă, limită, 2SZ 11–12, 3SZ 13–15, rebid sărit al răspunzătorului).
6. **Lecția 6** (`lecke6.py`): al doilea anunț al deschizătorului (ridicări pe trepte, 3♣ sărit, 2SZ 18–19, reverz 17+, jump shift 19+, NMF).

7. **Lecția 7** (`lecke7.py`): deschiderea de 2SZ, 20–21 (pas, 3SZ, Stayman 3♣, transfer 3♦/3♥, 4SZ cantitativ, 6SZ direct).
8. **Lecția 8** (`lecke8.py`): deschiderea de 1SZ, 15–17 (pas, 2SZ invit, 3SZ, Stayman cu invit, corecția 2♥–3SZ–4♠, transfer + pas/2SZ, 4SZ cantitativ).

## Decizii
- Ridicările la minoră sunt naturale (1♣–2♣ = 6–9, 1♣–3♣ = 10–11), nu inverted. De confirmat de Steffy.
- Planul dat de Steffy: Lecțiile 5–6 = deschiderile de 1♣ și 1♦; Lecțiile 7–8 = deschiderile de 2NT și 1NT.
- Lecția 4 e excepție de la „adversarii pasează”. La donele 6–8 Nord pasează, Est deschide, Sud intervine. Steffy îi spune prietenului licitația adversarilor pe WhatsApp.
- Introducerea trebuie să încapă pe o pagină: maximum ~8 teme și 3–4 termeni noi în dicționar.

## Lecție pentru agent
Steffy a întrebat de ce caut alte căi când metoda e salvată: am încercat, neîntrebat, un solver double dummy. Metoda rămâne cea din cronica din 2026-11-04: done manuale, validare cu scriptul, Word → PDF, iar Steffy verifică planurile de joc. Solverul a fost scos, nu a rămas nimic din el în proiect.

## De verificat de Steffy
- Planurile de joc (analizate manual, fără solver).
- Termenii maghiari noi: közbelicit, felvételi kontra, negatív kontra, büntető kontra, gyenge kettes, várakozó licit, kiegészítő érték (feature), preferencia, meghívás, reverz, ugrás új színben, új mellékszín kényszerítő (NMF), mennyiségi meghívás, részfelvétel. Căutarea pe web nu a găsit un dicționar care să îi confirme.
