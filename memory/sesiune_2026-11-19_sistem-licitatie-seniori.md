# [A2 - Agent Sistem Licitație Seniori] Sesiunea din 2026-11-19: sistemul „Easy Bidding” pentru seniori

## Context
Steffy a pornit un proiect nou: un sistem de licitație foarte simplu pentru oameni în vârstă (pensionari). Din experiența lui de trainer, ei rețin greu sistemele clasice (2/1, trefla tare, trefla poloneză). S-a creat agentul nou A2, trecut în CLAUDE.md-ul proiectului, cu folderul `easy_bidding/`.

## Deciziile lui Steffy
- Publicul: **începători** care joacă pe **BBO** și nu au învățat 2/1.
- **Majore din 5**, **deschideri slabe de 2**, totul **în engleză**.
- În a doua etapă a cerut **transferuri după 1FA și 2FA**.

## Ce s-a făcut
1. **Sistemul (numele provizoriu „Easy Bidding”)**, construit pe 3 idei: „licitezi ce ai”, aceleași cifre peste tot (6 – 12 – 25 – 33) și „Scara” (0–5 pas, 6–9 PAS MIC, 10–12 SALT = invitație, 13+ MANȘĂ).
   - Deschideri: 1♣/1♦ 12–21, fără majoră de 5 (3-3 → 1♣, 4-4 → 1♦); 1♥/1♠ 5+; 1FA 15–17; 2♣ 22+ (singura deschidere artificială); 2♦/2♥/2♠ slabe (6 cărți, 6–10); 2FA 20–21; la nivel de 3 = 7 cărți, slab.
   - Răspunsuri la majoră: întâi sprijinul (2 / 3 / 4 = 6–9 / 10–12 / 13+); 1FA 6–9; culoare nouă la nivel de 2 = 10+; 2FA / 3FA = 10–12 / 13–15.
   - După 1FA: 2♣ Stayman; 2♦/2♥ transferuri; 2♠ = slab cu minoră lungă (partenerul spune 3♣); 2FA 8–9; 3FA 10–15; 6FA 18–19. După 2FA (și după 2♣–2♦–2FA) totul merge la fel, un nivel mai sus.
   - După 2♣ răspunsul e mereu 2♦.
   - Competiție: intervenții 8–16 / 10–16; 1FA în intervenție 15–18. Regula unică a contrei: e de informație doar când adversarii au deschis o culoare și partenerul n-a licitat; orice altă contră e de pedeapsă.
   - Blackwood simplu (5♣ = 0/4 ași, 5♦ = 1, 5♥ = 2, 5♠ = 3). Atac de sus din secvență, al 4-lea din cea mai lungă culoare la FA. Semnal: carte mare = îmi place.
2. **Fișa de sistem** (`Easy_Bidding_Card.docx`): 4 pagini A4 (2 foi față-verso), litere de 12, ♥♦ roșii. Ultima pagină cuprinde lista de alerte pentru BBO.
3. **Broșura** (`Easy_Bidding_Booklet.docx`): 8 pagini, copertă cu numele lui Steffy, 10 capitole cu casete „Remember” și exemple, plus un chestionar cu 16 mâini și răspunsurile pe pagină separată.

## Abateri de la SAYC (sunt alertate pe BBO)
1♥–4♥ / 1♠–4♠ = 13+ (nu e o mână slabă); fără contră negativă; 2FA ca răspuns la 1 în culoare = 10–12; fără Jacoby 2FA; 2♠ după 1FA = minor slab. Roboții BBO joacă sistemul lor, deci sistemul e pentru parteneri umani.

## Mod de lucru stabilit
- Scripturile sunt în `easy_bidding/`: `docbuild.py` (funcții comune și verificarea mâinilor: 13 cărți, punctele din text), `card.py` și `booklet.py`. Documentele se generează în `easy_bidding/out/`.
- Verificarea vizuală: Word COM → PDF → pymupdf → PNG. Exemplele țin mâna lipită de explicație (keep_with_next).

## Pași următori posibili
- Numele final al sistemului.
- Done întregi (4 mâini) cu joc, ca la lecțiile din maghiară.
- Lecții pe capitole sau imagini pentru WhatsApp.
