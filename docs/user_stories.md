# Exempelbacklog – Hållbarhetskollen (15 user stories)

> Använd detta som start. Anpassa och prioritera för er MVP.  
> Tänk “vertikala slices”: en story ska ge **synligt värde** och vara demo-bar.

## MVP (rekommenderad bas)

### US-01 Skapa användare
Som användare vill jag kunna skapa en profil så att jag kan logga min data.
**Acceptanskriterier**
- [ ] Det går att skapa användare med namn.
- [ ] Svaret innehåller användar-id.
- [ ] Tomt namn ger 4xx + tydligt fel.

### US-02 Lista användare
Som användare vill jag se vilka användare som finns så att jag kan välja rätt profil.
**Acceptanskriterier**
- [ ] API returnerar en lista med (id, namn).
- [ ] Tom lista hanteras utan fel.

### US-03 Registrera aktivitet (generell)
Som användare vill jag registrera en aktivitet (kategori, typ, mängd, datum) så att jag kan spåra min påverkan.
**Acceptanskriterier**
- [ ] Aktivitet skapas med user_id, category, key, amount, date.
- [ ] amount måste vara > 0.
- [ ] Okänd user_id ger 404.

### US-04 Lista aktiviteter (filter)
Som användare vill jag kunna lista mina aktiviteter så att jag kan se historik.
**Acceptanskriterier**
- [ ] Det går att lista alla aktiviteter.
- [ ] Det går att filtrera på user_id.

### US-05 Visa CO₂e per aktivitet
Som användare vill jag se CO₂e-estimat för en aktivitet så att jag förstår påverkan.
**Acceptanskriterier**
- [ ] När emissionsfaktor finns: co2e = amount * co2e_per_unit.
- [ ] När emissionsfaktor saknas: API svarar tydligt (t.ex. co2e=null och/eller 4xx enligt ert beslut).
- [ ] Beräkningen är enhetstestad.

### US-06 Importera emissionsfaktorer
Som systemadministratör vill jag kunna importera emissionsfaktorer från fil så att beräkningar kan göras.
**Acceptanskriterier**
- [ ] Importscript kan köras lokalt och lägger in faktorer i DB.
- [ ] Felaktig fil/kolumn ger begripligt fel.
- [ ] Import är idempotent (körbar flera gånger utan dubbletter).

### US-07 Lista emissionsfaktorer
Som utvecklare vill jag kunna se vilka emissionsfaktorer som finns så att jag kan felsöka och verifiera data.
**Acceptanskriterier**
- [ ] Endpoint listar faktorer (category, key, unit, co2e_per_unit).
- [ ] Rimlig sortering eller stabil ordning.

### US-08 Veckorapport per användare
Som användare vill jag se min totala CO₂e för en vecka så att jag kan följa trender.
**Acceptanskriterier**
- [ ] Givet user_id och week_start (måndag) returneras total CO₂e för veckan.
- [ ] Endpoints hanterar vecka utan aktiviteter (total=0).
- [ ] Minst ett integrationstest för rapportendpoint.

### US-09 Förklara beräkningen (transparens)
Som användare vill jag kunna se vilka faktorer som användes så att jag kan förstå resultatet.
**Acceptanskriterier**
- [ ] Rapport eller aktivitet visar “grund”: category, key, co2e_per_unit, unit (i någon form).
- [ ] Rapporten beskriver antaganden (i text/README/rapport).

### US-10 Kvalitet: CI + lint + tester
Som team vill vi ha automatiska kontroller så att vi undviker regressioner.
**Acceptanskriterier**
- [ ] CI kör ruff + pytest på PR.
- [ ] PR mergeas inte när CI är röd (enligt er överenskommelse).
- [ ] Testerna täcker åtminstone central beräkningslogik.

---

## Stretch (välj 1–3)

### US-11 Exportera data (CSV/JSON)
Som användare vill jag exportera mina aktiviteter så att jag kan analysera dem vidare.
**Acceptanskriterier**
- [ ] Export kan filtreras per användare.
- [ ] Exportformat dokumenteras.

### US-12 Åtgärdsförslag (“topp-3”)
Som användare vill jag få förslag på åtgärder som minskar min CO₂e så att jag kan förbättra mitt beteende.
**Acceptanskriterier**
- [ ] Systemet kan identifiera största källorna (enkel heuristik ok).
- [ ] Förslagen är begripliga och kopplade till data.

### US-13 Månadsrapport
Som användare vill jag se en månadsrapport så att jag kan jämföra över tid.
**Acceptanskriterier**
- [ ] Totalsumma per månad eller per vecka inom månad.
- [ ] Testad beräkning.

### US-14 Enkel autentisering
Som användare vill jag logga in så att mina data skyddas från andra.
**Acceptanskriterier**
- [ ] Miniminivå: token/session eller enkel auth-lösning (beskriv i rapport).
- [ ] Grundläggande säkerhet: inga plain-text lösenord.

### US-15 Admin: uppdatera emissionsfaktorer via API
Som admin vill jag kunna uppdatera faktorer utan att köra script så att systemet blir enklare att underhålla.
**Acceptanskriterier**
- [ ] CRUD för emissionsfaktorer (kan vara begränsat).
- [ ] Behörighet (även enkel) finns så att inte alla kan ändra.