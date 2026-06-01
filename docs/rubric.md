# Betygskriterier / Rubric – Projekt (U/G/VG)

> Denna rubric är ett stöd för bedömning av projektet och kopplar främst till lärandemål **3–5**.
> För betyg **G** ska samtliga “måste”-kriterier vara uppfyllda. För **VG** krävs dessutom en helhet som visar
> hög kvalitet i metod, spårbarhet och reflektion – inte nödvändigtvis fler funktioner.

---

## Översikt per område

### 1) Planering och genomförande (mål 4)
**U**
- Ingen realistisk plan / sprintmål saknas, eller projektet blir i praktiken “ad hoc”.
- Leverans saknar tydlig prioritering (MVP ej uppnådd).

**G**
- Tydlig plan (Sprint 0 + sprintar) med prioriterad backlog.
- MVP levereras och är körbar enligt instruktioner.
- Rimlig arbetsfördelning och uppföljning (synlig i issues/PR).

**VG**
- Planering och prioritering är konsekvent och datadriven (t.ex. justering efter risker/retro).
- Scope hanteras professionellt (medvetna avgränsningar + leveransfokus).
- Tydlig spårbarhet från krav → plan → leverans.

---

### 2) Agilt arbetssätt och tekniska hjälpmedel (mål 3)
**U**
- Arbetssättet syns inte i repo (få/inga issues/PR) eller arbetet sker mest direkt på main.
- Brist på code review eller otydligt versionshanteringsflöde.

**G**
- Arbetet sker via issues + branch/PR + minst en review per större förändring.
- Grundläggande ceremonier (planering, review, retro) är dokumenterade kort.

**VG**
- Mycket god disciplin: små PRs, tydliga commits, bra review-kommentarer.
- DoD används aktivt och syns i arbetssättet (inte bara “finns”).
- CI används som kvalitetsspärr (inte ignorerad).

---

### 3) Arkitektur, struktur och kodkvalitet (mål 3–4)
**U**
- Kod är svår att förstå/underhålla: monolitisk fil, duplicerad logik, otydliga gränser.
- Saknar rimlig modulstruktur eller konsekvent stil.

**G**
- Rimlig struktur (t.ex. separerar API/DB/beräkning).
- Namngivning och modulindelning är begriplig.
- Grundläggande dokumentation: README med körinstruktion.

**VG**
- Väl motiverade arkitekturval, tydliga gränser mellan lager/moduler.
- God praxis: tydliga felmeddelanden, loggning där relevant, konsekventa typer/validering.
- Arkitekturbeskrivningen stämmer med implementationen.

---

### 4) Kvalitetssäkring (test, CI, felhantering) (mål 4)
**U**
- Tester saknas eller är triviala; CI saknas eller är trasig vid inlämning.
- Beräkningar/funktioner är inte verifierade.

**G**
- Minst enhetstester för central logik + minst ett integrationstest för API.
- CI kör tester (och gärna lint) och är grön vid inlämning.
- Rimlig felhantering och inputvalidering.

**VG**
- Tester täcker kritiska scenarion och felvägar (inte bara “happy path”).
- Kvalitet är integrerad: tydlig teststrategi + konsekvent körning.
- Få regressioner, stabil demo och robusthet vid oväntad input.

---

### 5) Riskhantering (mål 4)
**U**
- Risklogg saknas eller är symbolisk (inga åtgärder/ägare).

**G**
- Risklogg med minst 5 risker, åtgärder och ansvariga.
- Minst någon risk har aktivt hanterats under projektet.

**VG**
- Riskarbetet påverkar planering och prioritering (synligt i sprintplan/retro).
- Kvalitets- och tidsrisker identifieras tidigt och hanteras proaktivt.

---

### 6) Informationssäkerhet (grundnivå) (mål 4)
**U**
- Hemligheter i repo, eller uppenbara sårbarheter (t.ex. ingen validering, hårdkodade lösenord).

**G**
- Inga hemligheter i repo (använder t.ex. `.env` lokalt + `.gitignore`).
- Inputvalidering och rimliga felmeddelanden.
- Grundläggande resonemang om säkerhet i rapporten.

**VG**
- Tydlig hot-/riskbild på grundnivå (vad kan gå fel och hur minimeras det?).
- Säkerhetsåtgärder är implementerade där relevant (t.ex. bättre access-kontroll, säkra defaults).

---

### 7) Skriftlig rapport (mål 5)
**U**
- Rapport saknar viktiga delar eller är för otydlig för att bedöma metod/arbete.

**G**
- Rapporten följer mallen: krav, metod, arkitektur, kvalitet, resultat, reflektion.
- Innehåller hållbarhetskoppling med rimliga antaganden och begränsningar.

**VG**
- Mycket tydlig och välstrukturerad rapport med konkreta exempel (från repo/process).
- Starka motiveringar av val, tydliga begränsningar och förbättringsförslag.

---

### 8) Muntlig redovisning (mål 5)
**U**
- Otydlig demo eller saknar centrala delar (metod/kvalitet/reflektion).

**G**
- Demo fungerar, och gruppen kan förklara systemet, arbetssättet och kvalitet.
- Alla i gruppen deltar meningsfullt.

**VG**
- Mycket tydlig berättelse: problem → lösning → design → kvalitet → lärdomar.
- Kan svara på frågor med hänvisning till spårbarhet (issues/PR/test).

---

### 9) Reflektion (mål 4)
**U**
- Reflektion är ytlig (“allt gick bra”) eller saknas.

**G**
- Reflekterar över grupprocess, planering, kvalitet och vad som kan förbättras.

**VG**
- Konkret och självkritisk reflektion med exempel (beslut, misstag, åtgärder, lärdomar).
- Tydliga förbättringar som är realistiska och prioriterade.

---

## Minimikrav (sammanfattning)
För **G** ska följande alltid vara uppfyllt:
- Körbar MVP + README med instruktioner
- Git-flöde med branch/PR + code review
- CI som kör tester och är grön
- Tester för central logik + minst ett integrationstest
- Risklogg + DoD + kort arkitekturbeskrivning
- Rapport + muntlig redovisning + individuell reflektion