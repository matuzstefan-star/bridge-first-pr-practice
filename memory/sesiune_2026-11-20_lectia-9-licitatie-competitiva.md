# [A1 - Agent Lecții Bridge] Sesiunea din 2026-11-20: Lecția 9, licitație competitivă după 1♣/1♦

## Cererea
Steffy: 8 done cu licitație competitivă, intervențiile adversarilor după deschiderea de 1♣ sau 1♦.

## Ce s-a făcut
1. **Lecția 9** (`bridzs_lectii/lecke9.py`, `Bridzs_2-1_Lecke_9.docx`, `Lapok_Lecke_9/`): Nord deschide 1♣/1♦, Est intervine, Sud (prietenul) răspunde.
   - D1 contră negativă (1♦–1♠–X), D2 culoare nouă = 5 cărți (1♣–1♥–1♠), D3 1SZ cu oprire (1♦–1♥–1SZ),
   - D4 ridicare simplă + competiție la 3♦ (regula celor 9 atuuri), D5 cue-bid 1♣–1♠–2♠, apoi 2SZ–3SZ,
   - D6 recontră după contra de informație + contră de penalizare la 1♥, D7 contră de penalizare pe 1SZ în intervenție,
   - D8 pas capcană + contră de redeschidere pe 2♣.
2. Export pe Desktop: `Bridzs lectii\Lectia 9`. Introducerea pe o pagină, fiecare donă pe o pagină (verificat Word → PDF).
3. `cards.py` primește acum lista lecțiilor: `cards.py <OUT> 9` regenerează doar Lecția 9.

## Incident (rezolvat)
La început am lucrat pe `main`, unde există doar Lecțiile 1–2. Am numit lecția „3” și am exportat-o pe Desktop, suprascriind vechea `Lectia 3` (slabe de 2 / 2♣ forte, făcută pe 2026-11-06). Am restaurat-o imediat din commit-ul `d6bab80` (documentul e identic, JPG-urile regenerate din aceleași PNG). Apoi am mutat branch-ul peste `d6bab80` și am numit lecția 9.
- Lecțiile 3–8 sunt pe branch-ul `claude/lectii-3-4-date-09d926`, care NU e încă în `main`.

## Decizii
- Terminologie maghiară aliniată cu Lecția 4: közbelicit, felvételi kontra, negatív kontra (8+ fp), büntető kontra, „az ellenfél színének licitje”, „a 9 adu szabálya”. Termeni noi: csapdapassz, újranyitó kontra, bukás / beliben.
- Lecția 9 se suprapune parțial cu Lecția 4 (contră negativă, cue-bid, recontră). Diferența: aici doar după 1♣/1♦, cu Sud ca răspunzător.

## Corecturi de la Steffy (aplicate în Lecțiile 1, 2, 4, 5, 6, 9)
- közbeszólás, NU közbelicit (deci și Lecția 4 a fost corectată).
- növeld fel (felnövel), NU állítsd fel (felállít).
- indítás, NU belépő.
- Lecția 4: tema „Közbeszólás” a fost scurtată, ca introducerea să încapă din nou pe o pagină.
- Documentele au fost regenerate și copiate pe Desktop. Artefact cu Lecția 9: https://claude.ai/artifact/FmTdtVqRDxPQxaobus6jDk

## Artefact, commit, PR
- Pagina web a Lecției 9 (privată, generată din `lecke9.py`): https://claude.ai/artifact/FmTdtVqRDxPQxaobus6jDk, cu butonul „Csak Dél lapjai”, care ascunde celelalte mâini. Generatorul paginii a fost un script temporar (scratchpad), nu e în proiect.
- Commit `ab24e25` pe `claude/lectii-licitatie-competitiva-a284b6`, peste `d6bab80` (Lecțiile 3–8).
- PR [matuzstefan-star/bridge-first-pr-practice#5](https://github.com/matuzstefan-star/bridge-first-pr-practice/pull/5) către main, deschis, fără conflicte, fără CI. Merge-ul îl face Steffy după ce verifică lecțiile.

## Pași următori
- Steffy verifică planurile de joc și termenii, apoi face merge la PR #5.
- Următoarea lecție nouă primește numărul 10.

## De verificat de Steffy
- Planurile de joc (manual, fără solver), mai ales D3 (1SZ face exact 7 dacă se numără), D6–D8 (numărul de căderi estimat).
- Termenii noi: csapdapassz, újranyitó kontra.
