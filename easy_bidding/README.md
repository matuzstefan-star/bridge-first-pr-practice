# Easy Bidding – sistem de licitație simplu pentru seniori (agentul A2)

Sistem natural, în engleză, pentru începători în vârstă care joacă pe BBO și nu au învățat 2/1.
Bază: majore din 5, 1FA 15–17, 2♣ forte, deschideri slabe de 2, Stayman, transferuri după 1FA și 2FA (2♠ = minor slab), Blackwood.

## Fișiere

| Fișier | Ce face |
|---|---|
| `docbuild.py` | Funcții comune Word (litere mari, ♥♦ roșii, tabele, casete) + verificarea mâinilor (13 cărți, puncte). |
| `card.py` | Fișa de sistem: 4 pagini A4, de ținut pe masă. |
| `booklet.py` | Broșura: explicații pe capitole, exemple, chestionar cu 16 mâini și răspunsuri. |
| `out/` | Documentele Word generate. |

## Cum se generează (din acest folder)

```bash
python -X utf8 card.py out/Easy_Bidding_Card.docx
python -X utf8 booklet.py out/Easy_Bidding_Booklet.docx
```

Dacă punctele scrise în text nu se potrivesc cu mâna, scriptul se oprește cu eroare.
