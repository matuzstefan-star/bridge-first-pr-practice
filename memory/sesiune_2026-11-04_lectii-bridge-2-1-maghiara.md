# [A1 - Agent Lecții Bridge] Sesiunea din 2026-11-04: dedicație și lecții de bridge 2/1 în maghiară

## Context
Un prieten al lui Steffy a cumpărat „Horoscope for Bridge Players”. Au învățat bridge împreună acum 50 de ani, în armată, apoi au fost colegi de facultate la Cluj. Prietenul s-a mutat în Ungaria, nu a mai jucat de atunci și au reluat legătura în 2026. Acum vrea să reînvețe jocul, iar sistemul 2/1 e complet nou pentru el.

## Ce s-a făcut
1. **Dedicația**: variante în română, apoi în maghiară (ce a ales Steffy). Patru tonuri: nostalgic, invitație înapoi la masă, cu umor („passz” de 50 de ani), scurt.
2. **Lecția 1** (8 done): răspuns la nivel 1, 1NT forcing, ridicare limită, 2/1 GF + fast arrival, 1♠–2♥, 1♦–2♣, Stayman, transfer Jacoby.
3. **Lecția 2** (8 done): răspunsuri la 1♣/1♦ (întâi majoră, up the line, rebid 1NT 12–14), Jacoby 2NT (minim / singleton / forță în plus), cue-bid, RKCB 1430 (inclusiv oprirea la 5 când lipsesc 2 carte cheie).
4. **Corecturi de terminologie maghiară** cerute de Steffy (aplicate peste tot): gémig kényszerítő (nu játszmáig), fogás (nu megállító), egyenletes elosztás (nu kiegyensúlyozott kéz), gém forsz (nu játszmakényszer), gém (nu játszma).
5. **Format pentru WhatsApp**: lecțiile se țin pe WhatsApp, iar prietenul nu trebuie să vadă distribuția. Pentru fiecare donă sunt două imagini: `_barat` = doar mâna lui (Sud), `_Steffy` = toate cele 4 mâini. Copiate ca JPG pe Desktop, în `Bridzs lectii\Lectia N\{Pentru prieten, Pentru mine}`, plus documentul Word cu explicații în „Pentru mine”. PNG-ul trimis ca document apărea la prieten ca link. Soluția: JPG plus copiere/lipire (Ctrl+C/Ctrl+V) sau „Fotografii și videoclipuri”.

## Mod de lucru stabilit
- Material în maghiară; termenii englezi în dicționar. Onoruri: A K D B 10; NT = SZ; puncte = fp.
- Format document Word: o pagină de introducere (teme + dicționar), apoi câte o pagină pe donă (diagramă, licitație, explicații, plan de joc, concluzie).
- Câte 8 done pe lecție, cu licitație + plan de joc. Adversarii pasează mereu. Nord deschide (dealer), prietenul e Sud.
- Verificare: scriptul validează 13 cărți/mână, 52 distincte și punctele. Documentul se randează prin Word → PDF → pymupdf, ca să verifici că fiecare donă încape pe o pagină. Nu există solver double dummy (endplay nu se instalează pe Python 3.14), deci planurile de joc sunt analizate manual și Steffy le verifică.
- Scripturile sunt în `bridzs_lectii/` (vezi README-ul de acolo).

## Pași următori posibili
- Lecția 3: licitație competitivă (contră, intervenții) sau 2♣ forte și deschideri slabe de 2.
