# Projekt-PM – Kursprojekt i Projektmetodik inom IT (ÅK1)

## 1. Bakgrund och syfte
I kursprojektet ska ni planera och genomföra ett mindre IT-projekt enligt **agila arbetssätt** och med stöd av
**tekniska verktyg** som versionshantering, issue-hantering och CI/test.

Projektet tränar särskilt kursens lärandemål:
- **(3)** praktisera agil utvecklingsmetodik/projektmetodik och använda tekniska hjälpmedel i systemutvecklingsprojekt
- **(4)** planera och genomföra IT-projekt (tidsplan, resurser, risk, kvalitet) och reflektera över resultat och arbetsprocess
- **(5)** redovisa projekt muntligt och skriftligt

## 2. Projektuppgift: “Hållbarhetskollen”
Ni utvecklar ett system som hjälper användare att förstå och minska sin miljöpåverkan genom att:
- registrera aktiviteter (t.ex. resor, måltider, elförbrukning),
- beräkna ett CO₂e-estimat baserat på emissionsfaktorer,
- visa sammanställningar över tid,
- exportera data.

**Viktigt:** Fokuset i kursen är **process, kvalitet och spårbarhet**, inte perfekta klimatdata eller ett avancerat UI.

### 2.1 Målgrupp och hållbarhet
Systemet ska ha en tydlig hållbarhetsnytta: t.ex. synliggöra beteenden, skapa underlag för åtgärder,
eller stödja reflektion kring klimatpåverkan.

Ni ska i rapporten beskriva:
- vilken hållbarhetsnytta systemet har,
- vilka antaganden som gjorts i beräkningarna,
- vilka risker som finns (t.ex. feltolkning av data).

## 3. Krav

### 3.1 MVP (måste)
Ni ska leverera en körbar MVP som innehåller:

1) **Användare**
- Skapa/lista användare (miniminivå).
- (Valfritt/extra) inloggning och autentisering.

2) **Aktivitetslogg**
- Registrera aktivitet (kategori, typ/nyckel, mängd, datum).
- Lista aktiviteter (filtrera per användare).

3) **Beräkning**
- CO₂e-estimat för aktiviteter baserat på emissionsfaktorer i systemet.
- Minst en rapportvy: t.ex. total CO₂e per vecka.

4) **Data**
- Emissionsfaktorer ska kunna importeras från en fil (CSV/JSON) eller hämtas från extern källa.

5) **Kvalitet**
- Tester (enhet + minst ett integrationstest).
- CI som kör tester (och gärna lint) vid PR.

### 3.2 Valbara förbättringar (stretch)
Välj 1–3 beroende på tid:
- Export (CSV/JSON)
- Visualisering (enkel graf)
- Admin-funktion för att uppdatera emissionsfaktorer
- Enkel autentisering (t.ex. token)
- Åtgärdsförslag: “topp-3 sätt att minska utsläpp” baserat på användarens data
- Grundläggande roll/behörighet

### 3.3 Icke-funktionella krav (måste)
- **Tydlig DoD:** “klart” betyder kodgranskat + tester gröna + dokumenterat.
- **Grundsäkerhet:** inga hemligheter i repo, inputvalidering, rimlig felhantering.
- **Spårbarhet:** user stories → issues → PR → leverans.

## 4. Teknik och begränsningar
Rekommenderad stack:
- Python + FastAPI
- SQLite lokalt (ok att byta till Postgres)
- Pytest
- Git + PR + code review
- CI (GitHub Actions/GitLab CI)

Begränsning: håll det **lagom**. En stabil MVP är bättre än många halvklara features.

## 5. Arbetssätt (agilt)
Ni arbetar i sprintar:

- **Sprint 0 (setup/planering)**: backlog, risker, arkitektur, CI, körbar “hello world”
- **Sprint 1**: MVP end-to-end (“tunn vertikal slice”)
- **Sprint 2**: förbättringar + kvalitet + rapport + demo

Ceremonier (rekommenderat):
- planering (30–60 min/sprint)
- kort standup 2–3 ggr/vecka (10 min)
- demo/review (15–20 min/sprint)
- retro (20–30 min/sprint)

## 6. Roller och ansvar (rotera)
- **PO (Product Owner):** backlog, prioritering, kravtolkning
- **SM (Scrum Master):** möten, hinder, följer upp arbetsflöde
- **QA/Release:** test, CI, DoD, release-tag
- **Arkitekturansvar:** struktur, gränser mellan moduler, tekniska beslut

Alla kodar. Roller ska hjälpa processen – inte skapa hierarki.

## 7. Obligatoriska artefakter (ska finnas i repo)
- Product backlog (user stories + acceptanskriterier)
- Sprint backlog (issues)
- Risklogg (minst 5 risker + ägare + åtgärd)
- Definition of Done
- Enkel arkitekturbeskrivning (komponentbild + dataflöde)
- Retroanteckningar (kort)

Mallarna finns i `docs/templates/`.

## 8. Leveranser (inlämning)
1) **Källkod (repo)**: körbar, dokumenterad, CI grön
2) **Rapport** enligt rapportmallen
3) **Muntlig redovisning** (demo + metod + kvalitet + reflektion)
4) **Individuell reflektion** (1–2 sidor)

## 9. Bedömning (U/G/VG)
Bedömning sker enligt kursens betygskriterier/rubric (se `docs/rubric.md`).
VG baseras främst på **kvalitet, metod och spårbarhet** – inte flest funktioner.