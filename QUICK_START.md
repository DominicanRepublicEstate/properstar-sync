# 🚀 QUICK START GUIDE - Bitrix24 → Properstar

## ⚡ Szybka konfiguracja (30 minut)

---

## KROK 1: Pobierz klucz API z Bitrix24 (5 min)

### A. Wejdź do Bitrix24
```
1. Zaloguj się: https://twoja-nazwa.bitrix24.pl
2. Kliknij: Aplikacje (menu po lewej)
3. Wybierz: Webhooki
4. Kliknij: "Webhook wychodzący"
5. Kliknij: "+ Dodaj webhook"
```

### B. Skonfiguruj webhook
```
Nazwa: Properstar Sync
Uprawnienia:
  ☑ CRM → crm.deal.list
  ☑ CRM → crm.deal.get
  ☑ CRM → crm.deal.add (jeśli będziesz importować z Excel)

Kliknij: ZAPISZ
```

### C. Skopiuj URL
```
URL będzie wyglądał tak:
https://twoja-nazwa.bitrix24.pl/rest/12345/abcdef987654/

📋 SKOPIUJ GO - będzie potrzebny w kroku 3!
```

---

## KROK 2: Przygotuj repozytorium GitHub (10 min)

### A. Utwórz nowe repozytorium
```
1. Wejdź na: https://github.com
2. Kliknij: "+" (góra po prawej) → "New repository"
3. Wypełnij:
   - Repository name: properstar-sync
   - Description: "Bitrix24 to Properstar XML feed"
   - ☑ Public (WAŻNE!)
   - ☑ Add a README file
4. Kliknij: "Create repository"
```

### B. Upload plików
```
1. W repozytorium kliknij: "Add file" → "Upload files"
2. Przeciągnij wszystkie pliki z tego projektu:
   - .github/workflows/sync_properstar.yml
   - bitrix24_properstar_sync.py
   - import_excel_to_bitrix.py
   - requirements.txt
   - README.md
   - .gitignore
3. Kliknij: "Commit changes"
```

**UWAGA:** Musisz utworzyć folder `.github/workflows/` i wrzucić tam plik `sync_properstar.yml`

---

## KROK 3: Konfiguracja Secrets (5 min)

### Dodaj webhook URL do GitHub
```
1. W repozytorium: Settings (góra)
2. Po lewej: Secrets and variables → Actions
3. Kliknij: "New repository secret"
4. Wypełnij:
   - Name: BITRIX24_WEBHOOK_URL
   - Secret: https://twoja-nazwa.bitrix24.pl/rest/12345/abcdef987654/
     (wklej URL z KROKU 1)
5. Kliknij: "Add secret"
```

---

## KROK 4: Włącz GitHub Pages (5 min)

### Konfiguracja hostingu XML
```
1. W repozytorium: Settings
2. Po lewej: Pages
3. W sekcji "Source":
   - Branch: gh-pages
   - Folder: / (root)
4. Kliknij: Save

⏳ Poczekaj 2-3 minuty
```

Twój link będzie:
```
https://twoja-nazwa-github.github.io/properstar-sync/export.xml
```

---

## KROK 5: Włącz uprawnienia (2 min)

### Pozwól GitHub Actions zapisywać pliki
```
1. W repozytorium: Settings
2. Po lewej: Actions → General
3. Przewiń do: "Workflow permissions"
4. Wybierz: ☑ Read and write permissions
5. Kliknij: Save
```

---

## KROK 6: Test! (3 min)

### Uruchom synchronizację ręcznie
```
1. W repozytorium: Actions (górny pasek)
2. Wybierz: "Properstar XML Sync" (po lewej)
3. Kliknij: "Run workflow" (po prawej)
4. Wybierz: Branch: main
5. Kliknij: "Run workflow"

⏳ Poczekaj ~2 minuty

✅ Jeśli jest zielony znaczek - sukces!
❌ Jeśli jest czerwony - sprawdź logi (kliknij na workflow)
```

### Sprawdź XML
```
Otwórz w przeglądarce:
https://twoja-nazwa-github.github.io/properstar-sync/export.xml

Powinieneś zobaczyć:
<?xml version='1.0' encoding='UTF-8'?>
<Adverts>
  <Advert>
    <AdvertId>...</AdvertId>
    ...
  </Advert>
</Adverts>
```

---

## KROK 7: Wyślij link do Properstar

### Treść maila dla Michaela Shvedova
```
To: support@properstar.com
CC: info@bitrix24.com
Subject: Data Feed Link - [Twoja Firma]

Dear Michael,

Please find our Properstar XML data feed link below:

https://twoja-nazwa-github.github.io/properstar-sync/export.xml

Feed details:
- Update frequency: Daily at 4:00 AM UTC
- Feed type: Full export
- Total properties: [liczba]
- Format: XML (Properstar/ListGlobally compliant)

Best regards,
[Twoje Imię]
```

---

## 📋 CHECKLIST - Czy wszystko działa?

✅ **Bitrix24**
- [ ] Webhook utworzony
- [ ] URL skopiowany
- [ ] Uprawnienia: crm.deal.list, crm.deal.get

✅ **GitHub**
- [ ] Repozytorium utworzone (Public!)
- [ ] Wszystkie pliki wgrane
- [ ] Secret BITRIX24_WEBHOOK_URL dodany
- [ ] GitHub Pages włączony (branch: gh-pages)
- [ ] Workflow permissions: Read and write

✅ **Test**
- [ ] Workflow uruchomiony ręcznie
- [ ] Workflow zakończony sukcesem (zielony ✓)
- [ ] XML dostępny pod linkiem
- [ ] XML zawiera oferty

✅ **Properstar**
- [ ] Link wysłany do support@properstar.com
- [ ] Link działa (sprawdzony w przeglądarce)

---

## 🆘 POMOC - Co jeśli nie działa?

### Workflow kończy się błędem (czerwony X)

**SPRAWDŹ:**
```
1. Actions → kliknij na czerwony workflow → sprawdź logi
2. Czy BITRIX24_WEBHOOK_URL jest poprawnie wpisany w Secrets?
3. Czy webhook w Bitrix24 ma uprawnienia do CRM?
```

### XML jest pusty

**PRZYCZYNY:**
```
1. Oferty w Bitrix24 nie mają wypełnionego UF_CRM_201 (AdvertId)
2. Webhook nie ma dostępu do ofert
3. Oferty są w złym statusie
```

**ROZWIĄZANIE:**
```
Sprawdź w Bitrix24:
- Czy masz jakieś oferty w CRM (Deals)?
- Czy mają wypełnione pole AdvertId?
- Czy są aktywne?
```

### GitHub Pages nie działa

**SPRAWDŹ:**
```
1. Czy repozytorium jest PUBLIC?
2. Czy w Settings → Pages wybrałeś branch: gh-pages?
3. Czy workflow się wykonał poprawnie?
4. Poczekaj 5 minut - czasem GitHub potrzebuje czasu
```

---

## 🔄 Import z Excel (OPCJONALNIE)

Jeśli chcesz zaimportować 217 nieruchomości z Excel do Bitrix24:

```bash
# 1. Sklonuj repozytorium lokalnie
git clone https://github.com/twoja-nazwa/properstar-sync.git
cd properstar-sync

# 2. Zainstaluj Python dependencies
pip install -r requirements.txt

# 3. Skopiuj plik Excel do tego folderu
# Nazwa: Dominican_Republic_Estate_listings_data_export__3_.xlsx

# 4. Ustaw webhook
export BITRIX24_WEBHOOK_URL="https://twoja-nazwa.bitrix24.pl/rest/12345/abc/"

# 5. Uruchom import
python import_excel_to_bitrix.py

# ⏳ Poczekaj ~5-10 minut (217 ofert)
```

---

## 📞 KONTAKT

Jeśli potrzebujesz pomocy:
1. Sprawdź README.md (pełna dokumentacja)
2. Sprawdź logi w GitHub Actions
3. Napisz co dokładnie nie działa

---

**POWODZENIA! 🎉**

Cała integracja będzie działać automatycznie - każdego dnia o 4:00 UTC.
