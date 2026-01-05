# Bitrix24 → Properstar XML Feed Integration

Automatyczna synchronizacja nieruchomości z Bitrix24 do Properstar w formacie XML.

## 📋 Spis treści

1. [Wymagania](#wymagania)
2. [Konfiguracja Bitrix24](#konfiguracja-bitrix24)
3. [Konfiguracja GitHub](#konfiguracja-github)
4. [Import nieruchomości z Excel](#import-nieruchomości-z-excel)
5. [Testowanie](#testowanie)
6. [Link do Properstar](#link-do-properstar)
7. [Rozwiązywanie problemów](#rozwiązywanie-problemów)

---

## 🔧 Wymagania

- Konto Bitrix24 z uprawnieniami administratora
- Konto GitHub
- Python 3.9+ (tylko do lokalnego testowania)

---

## 📦 Konfiguracja Bitrix24

### Krok 1: Utworzenie Webhooka

1. Zaloguj się do Bitrix24
2. Przejdź do: **Aplikacje** → **Webhooki** → **Webhook wychodzący**
3. Kliknij **Dodaj webhook**
4. Nadaj nazwę: `Properstar Sync`
5. Zaznacz uprawnienia:
   - ✅ **CRM** → **crm.deal.list** (odczyt)
   - ✅ **CRM** → **crm.deal.add** (zapis - jeśli będziesz importować)
   - ✅ **CRM** → **crm.deal.get** (odczyt)
6. Kliknij **Zapisz**
7. **SKOPIUJ URL WEBHOOKA** - będzie wyglądał tak:
   ```
   https://twoja-domena.bitrix24.pl/rest/123/abcdef123456/
   ```

### Krok 2: Weryfikacja pól niestandardowych

Twoje pola custom (UF_CRM_201-290) powinny być już utworzone zgodnie z plikiem `bitrix24_pole_dodatkowe.txt`.

**Najważniejsze pola:**
- `UF_CRM_201` - AdvertId (String)
- `UF_CRM_204` - AdvertType (Lista: Sale/Rent)
- `UF_CRM_205` - SubType (Lista: Apartment/House/Villa/etc)
- `UF_CRM_232` - Price (Liczba)
- `UF_CRM_233` - PriceCurrency (String: USD/EUR/etc)
- `UF_CRM_240` - Address (String)
- `UF_CRM_242` - City (String)
- `UF_CRM_243` - Country (String: DO = Dominican Republic)

**Jak sprawdzić ID pól:**
1. Przejdź do: **CRM** → **Ustawienia** → **Ustawienia pól**
2. Znajdź pole (np. "AdvertId")
3. Kliknij edycję - w URL zobaczysz ID pola

---

## 🔐 Konfiguracja GitHub

### Krok 1: Utworzenie repozytorium

1. Zaloguj się do GitHub
2. Utwórz nowe repozytorium:
   - Nazwa: `properstar-bitrix-sync` (lub dowolna)
   - Typ: **Public** (aby GitHub Pages działał)
   - ✅ Zaznacz "Initialize with README"

### Krok 2: Upload plików

Skopiuj wszystkie pliki z tego projektu do repozytorium:

```
properstar-bitrix-sync/
├── .github/
│   └── workflows/
│       └── sync_properstar.yml
├── bitrix24_properstar_sync.py
├── import_excel_to_bitrix.py
├── requirements.txt
└── README.md
```

### Krok 3: Konfiguracja GitHub Secrets

1. W repozytorium przejdź do: **Settings** → **Secrets and variables** → **Actions**
2. Kliknij **New repository secret**
3. Dodaj sekret:
   - **Name:** `BITRIX24_WEBHOOK_URL`
   - **Value:** `https://twoja-domena.bitrix24.pl/rest/123/abcdef123456/`
   - Kliknij **Add secret**

### Krok 4: Włączenie GitHub Pages

1. W repozytorium przejdź do: **Settings** → **Pages**
2. W sekcji **Source** wybierz:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
3. Kliknij **Save**

Po kilku minutach Twój feed XML będzie dostępny pod adresem:
```
https://twoj-login.github.io/properstar-bitrix-sync/export.xml
```

### Krok 5: Włączenie uprawnień do zapisu

1. Przejdź do: **Settings** → **Actions** → **General**
2. Przewiń do sekcji **Workflow permissions**
3. Wybierz: ✅ **Read and write permissions**
4. Kliknij **Save**

---

## 📊 Import nieruchomości z Excel

Jeśli chcesz zaimportować swoje 217 nieruchomości z pliku Excel do Bitrix24:

### Przygotowanie środowiska lokalnego

```bash
# Sklonuj repozytorium
git clone https://github.com/twoj-login/properstar-bitrix-sync.git
cd properstar-bitrix-sync

# Zainstaluj zależności
pip install -r requirements.txt

# Skopiuj plik Excel do folderu
# Plik powinien nazywać się: Dominican_Republic_Estate_listings_data_export__3_.xlsx
```

### Uruchomienie importu

```bash
# Ustaw zmienną środowiskową z webhookiem
export BITRIX24_WEBHOOK_URL="https://twoja-domena.bitrix24.pl/rest/123/abcdef123456/"

# Uruchom import
python import_excel_to_bitrix.py
```

**Import będzie:**
- ✅ Sprawdzać czy nieruchomość już istnieje (po AdvertId)
- ✅ Pomijać duplikaty
- ✅ Tworzyć nowe oferty
- ✅ Mapować wszystkie pola z Excel do Bitrix24

**Przykładowy output:**
```
================================================================================
Starting import from Excel to Bitrix24
================================================================================
Loaded 217 properties from Excel
Row 1: Creating property 107359978...
Row 1: ✓ Created deal ID: 12345
Row 2: Creating property 107386393...
Row 2: ✓ Created deal ID: 12346
...
================================================================================
Import completed!
Created: 217
Skipped: 0
Errors: 0
================================================================================
```

---

## 🧪 Testowanie

### Test 1: Ręczne uruchomienie workflow

1. Przejdź do zakładki **Actions** w repozytorium
2. Wybierz workflow **Properstar XML Sync**
3. Kliknij **Run workflow** → **Run workflow**
4. Poczekaj ~2 minuty
5. Sprawdź czy workflow zakończył się sukcesem (zielony ✓)

### Test 2: Sprawdzenie wygenerowanego XML

Otwórz w przeglądarce:
```
https://twoj-login.github.io/properstar-bitrix-sync/export.xml
```

Powinieneś zobaczyć XML zaczynający się od:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<Adverts>
  <Advert>
    <AdvertId>107359978</AdvertId>
    <AdvertType>Sale</AdvertType>
    <SubType>Apartment</SubType>
    ...
  </Advert>
</Adverts>
```

### Test 3: Walidacja XML

Możesz sprawdzić poprawność XML na:
- https://www.xmlvalidation.com/
- https://codebeautify.org/xmlvalidator

---

## 📮 Link do Properstar

### Odpowiedź dla Michaela Shvedova

Wyślij mailem do: **support@properstar.com** oraz **info@bitrix24.com**

```
Subject: Data Feed Link - Dominican Republic Estate

Dear Michael,

Thank you for your message. I have successfully set up the XML data feed integration between Bitrix24 and Properstar.

Here is the link to our XML data feed:
https://YOUR-GITHUB-USERNAME.github.io/properstar-bitrix-sync/export.xml

Feed details:
- Format: XML (compliant with Properstar/ListGlobally schema)
- Update frequency: Daily (automated via GitHub Actions at 4:00 AM UTC)
- Feed type: Full export (all active listings included in each update)
- Total properties: 217 (Dominican Republic luxury real estate)
- Fields included: All mandatory and optional fields as per your documentation

The feed is automatically updated daily and contains complete property information including:
- Property details (type, rooms, areas)
- Pricing in USD
- Location data (address, coordinates)
- Descriptions in multiple languages (EN, PL, ES)
- Contact information (office and agent details)

Please review the feed and let me know if any adjustments are needed.

Best regards,
[Your Name]
[Your Company]
```

**WAŻNE:** Zastąp `YOUR-GITHUB-USERNAME` swoją prawdziwą nazwą użytkownika GitHub!

---

## 🔄 Harmonogram automatyzacji

Workflow GitHub Actions uruchamia się:

1. **Automatycznie:** Codziennie o 4:00 UTC (6:00 czasu polskiego zimą, 5:00 latem)
2. **Ręcznie:** Możesz uruchomić z zakładki Actions w dowolnym momencie

Każde uruchomienie:
1. Pobiera aktualne dane z Bitrix24
2. Generuje plik `export.xml`
3. Publikuje na GitHub Pages
4. Commituje kopię do głównej gałęzi (backup)

---

## 🐛 Rozwiązywanie problemów

### Problem: Workflow kończy się błędem

**Sprawdź:**
1. Czy `BITRIX24_WEBHOOK_URL` jest poprawnie ustawiony w Secrets
2. Czy webhook w Bitrix24 ma odpowiednie uprawnienia
3. Logi w zakładce Actions → kliknij na konkretny workflow → sprawdź szczegóły błędu

### Problem: XML jest pusty lub ma mało ofert

**Możliwe przyczyny:**
1. Oferty w Bitrix24 nie mają wypełnionego pola `UF_CRM_201` (AdvertId)
2. Oferty są w złym statusie/kategorii
3. Webhook nie ma dostępu do wszystkich ofert

**Rozwiązanie:**
- Sprawdź w Bitrix24 czy oferty mają wypełnione AdvertId
- Możesz zmodyfikować filtr w `bitrix24_properstar_sync.py` (linia ~337)

### Problem: GitHub Pages nie działa

**Sprawdź:**
1. Czy repozytorium jest **Public**
2. Czy w Settings → Pages jest ustawiony branch `gh-pages`
3. Czy workflow zakończył się sukcesem (sekcja "Deploy XML to GitHub Pages")

### Problem: Zdjęcia nie są pobierane

Obecnie skrypt nie pobiera zdjęć automatycznie z Bitrix24, ponieważ wymaga to dodatkowych wywołań API.

**Aby dodać zdjęcia:**
1. Zdjęcia w Bitrix24 muszą być przechowywane w konkretnym polu (np. `UF_CRM_XXX`)
2. Trzeba pobrać URL-e zdjęć przez API
3. Usunąć parametry `?mode=max` z URL-i (funkcja `clean_url` to robi)
4. Dodać do sekcji `<Photos>` w XML

Jeśli potrzebujesz pomocy z implementacją zdjęć, daj znać!

---

## 📞 Wsparcie

Jeśli masz pytania lub problemy:
1. Sprawdź logi w GitHub Actions (zakładka Actions)
2. Sprawdź czy wszystkie kroki w tym README zostały wykonane
3. Zweryfikuj konfigurację webhooków w Bitrix24

---

## 📄 Licencja

Ten projekt jest open source. Możesz go modyfikować według własnych potrzeb.

---

**Powodzenia z integracją! 🚀**
