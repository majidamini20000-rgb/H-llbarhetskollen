# IT-Projektmetodik – Starter Kit (ÅK1)

Det här repot är en **startmall** för kursprojektet *Hållbarhetskollen* (eller liknande CRUD + beräkningslogik).
Målet är att ni snabbt ska kunna komma igång med **projektmetodik** (Git-flöde, issues/PR, CI, test, kvalitet)
utan att fastna i tomt “setup-arbete”.

## Snabbstart

### 1) Skapa virtuell miljö och installera beroenden
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2) Starta API-servern
```bash
uvicorn app.main:app --reload
```

Öppna Swagger UI:
- http://127.0.0.1:8000/docs

### 3) Skapa databas + importera emissionsfaktorer
```bash
python -m app.bootstrap_db
python -m app.import_emission_factors
```

### 4) Kör tester + lint
```bash
pytest -q
ruff check .
```

> Tips: Håll er CI grön. När CI går rött: åtgärda direkt.

---

## Rekommenderat arbetsflöde (kort)

- Planera i **issues** (en issue per user story eller task).
- Skapa **branch per feature**: `feature/<kort-namn>` eller `fix/<kort-namn>`.
- Leverera via **Pull Request** + minst en code review.
- Merge när: CI grön + acceptanskriterier uppfyllda.

---

## Projektidé i korthet (Hållbarhetskollen)

Ni bygger ett system där en användare kan:
- registrera aktiviteter (t.ex. resa, måltid, elförbrukning),
- få ett CO₂e-estimat baserat på emissionsfaktorer,
- se en sammanställning per vecka/månad,
- exportera data.

**Viktigt:** Exakta klimatdata är inte huvudpoängen i kursen – *spårbarhet, kvalitet och process* är det.

---

## Katalogstruktur

```
app/
  main.py              # FastAPI endpoints
  db.py                # databas-session (SQLAlchemy)
  models.py            # ORM-modeller
  schemas.py           # API-scheman (Pydantic)
  services/
    emissions.py       # beräkningslogik (enhetstestas)
  bootstrap_db.py      # skapar tabeller (enkel start)
  import_emission_factors.py
data/
  emission_factors.csv # exempeldata
tests/
  test_emissions.py
  test_api.py
docs/
  project_pm.md
  rubric.md
  templates/
    backlog_template.md
    definition_of_done.md
    risklogg_template.md
    sprint_plan_template.md
    retro_template.md
    rapportmall.md
    presentation_checklist.md
```

---

## Vad ni bör lägga till i projektet

Minimikrav (för att uppfylla projektbeskrivningen):
- fler user stories (MVP + några förbättringar)
- bättre validering och felhantering
- fler tester (enhet + integration)
- enkel säkerhet: inputvalidering, hantering av hemligheter, grundläggande access-kontroll
- tydlig dokumentation (README + rapport)

---

## Vanliga fallgropar

- För mycket UI tidigt → bygg hellre ett stabilt API + demo.
- För stora user stories → bryt ner till små vertikala slices.
- “Vi testar sen” → tester från dag 1.
- Otydliga acceptanskriterier → skriv dem innan ni kodar.

Lycka till!