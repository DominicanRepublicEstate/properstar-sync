# 🔑 GDZIE WKLEIĆ KLUCZ Z BITRIX24 I JAK TO DZIAŁA

## ✅ ODPOWIEDZI NA TWOJE PYTANIA

---

## 1️⃣ GDZIE WKLEIĆ KLUCZ Z BITRIX24?

### Klucz webhook NIE idzie do pliku .py!
Klucz wklejasz w **GitHub Secrets** (bezpieczne miejsce).

### Krok po kroku:

**A. Pobierz klucz z Bitrix24:**
```
1. Zaloguj się do Bitrix24
2. Kliknij: Aplikacje → Webhooki → Webhook wychodzący
3. Kliknij: "+ Dodaj webhook"
4. Nadaj nazwę: "Properstar Sync"
5. Zaznacz uprawnienia:
   ☑ CRM → crm.deal.list
   ☑ CRM → crm.deal.get
   ☑ CRM → crm.deal.add
6. Kliknij: ZAPISZ
7. SKOPIUJ URL, który wygląda tak:

https://twoja-nazwa.bitrix24.pl/rest/12345/abc123def456/
                                      └─ USER_ID  └─ WEBHOOK_CODE
```

**B. Wklej do GitHub Secrets:**
```
1. Przejdź do swojego repozytorium na GitHub
2. Kliknij: Settings (górny pasek)
3. Po lewej stronie: Secrets and variables → Actions
4. Kliknij: "New repository secret"
5. Wypełnij:
   Name: BITRIX24_WEBHOOK_URL
   Secret: https://twoja-nazwa.bitrix24.pl/rest/12345/abc123def456/
6. Kliknij: "Add secret"
```

**GOTOWE!** Klucz jest bezpiecznie przechowywany i workflow go automatycznie użyje.

---

## 2️⃣ JAK TO POTEM MA DZIAŁAĆ?

### Automatyczny proces (bez Twojego udziału):

```
🕐 CODZIENNIE O 4:00 RANO (UTC):
└─→ 1. GitHub Actions automatycznie uruchamia workflow
    └─→ 2. Workflow pobiera Twój klucz z Secrets
        └─→ 3. Uruchamia skrypt Python (bitrix24_properstar_sync.py)
            └─→ 4. Skrypt łączy się z Bitrix24 (używając klucza)
                └─→ 5. Pobiera wszystkie oferty z CRM
                    └─→ 6. Generuje plik export.xml
                        └─→ 7. Publikuje na GitHub Pages
                            └─→ 8. Twój XML jest dostępny pod:
                                https://twoj-login.github.io/repo-name/export.xml
```

### Możesz też uruchomić ręcznie:
```
1. Wejdź na GitHub → Twoje repozytorium
2. Zakładka: Actions
3. Wybierz: "Properstar XML Sync"
4. Kliknij: "Run workflow" → "Run workflow"
5. Poczekaj ~2 minuty
6. ✅ Gotowe - XML zaktualizowany!
```

---

## 3️⃣ JAKI LINK WYSŁAĆ DO PROPERSTAR?

Po uruchomieniu workflow (automatycznym lub ręcznym), Twój plik XML będzie dostępny pod adresem:

```
https://TWOJA-NAZWA-GITHUB.github.io/NAZWA-REPO/export.xml
```

**Przykład:**
- Jeśli Twoja nazwa GitHub to: `kowalski`
- I nazwałeś repo: `properstar-sync`
- To link będzie: `https://kowalski.github.io/properstar-sync/export.xml`

**Ten link wysyłasz do Michaela Shvedova z Properstar.**

---

## 4️⃣ CZY TO DODA MOJE OFERTY Z PLIKU EXCEL?

### NIE automatycznie, ale masz skrypt do tego!

Masz dwa skrypty:

**SKRYPT 1: `import_excel_to_bitrix.py`**
- Import 217 ofert z Excel → Bitrix24
- Uruchamiasz **raz** (lokalnie na swoim komputerze)
- Tworzy oferty w Bitrix24 CRM

**SKRYPT 2: `bitrix24_properstar_sync.py`**
- Synchronizacja Bitrix24 → XML dla Properstar
- Uruchamia się **automatycznie** przez GitHub Actions
- Pobiera oferty z Bitrix24 i generuje XML

---

## 5️⃣ KOMPLETNY PRZEPŁYW DANYCH

```
┌─────────────────────────────────────────────────────────────────┐
│                         ETAP 1 (RAZ)                            │
│                      Import z Excel                              │
└─────────────────────────────────────────────────────────────────┘

📊 Excel (217 ofert)
    │
    │ [uruchamiasz lokalnie: import_excel_to_bitrix.py]
    ↓
🏢 Bitrix24 CRM (217 ofert w systemie)


┌─────────────────────────────────────────────────────────────────┐
│                 ETAP 2 (AUTOMATYCZNIE CODZIENNIE)               │
│              Synchronizacja do Properstar                        │
└─────────────────────────────────────────────────────────────────┘

🏢 Bitrix24 CRM (oferty)
    │
    │ [GitHub Actions uruchamia: bitrix24_properstar_sync.py]
    ↓
📄 export.xml (plik XML zgodny z Properstar)
    │
    │ [GitHub Pages publikuje]
    ↓
🌐 https://twoj-login.github.io/repo/export.xml
    │
    │ [Properstar pobiera codziennie]
    ↓
🏠 Properstar (Twoje oferty widoczne na portalu)
```

---

## 6️⃣ INSTRUKCJA KROK PO KROKU

### KROK A: Importuj oferty z Excel do Bitrix24 (raz)

```bash
# 1. Sklonuj repozytorium na swój komputer
git clone https://github.com/twoj-login/properstar-sync.git
cd properstar-sync

# 2. Zainstaluj Python dependencies
pip install -r requirements.txt

# 3. Skopiuj plik Excel do tego folderu
# Nazwa: Dominican_Republic_Estate_listings_data_export__3_.xlsx

# 4. Ustaw zmienną środowiskową z webhookiem
# Windows (CMD):
set BITRIX24_WEBHOOK_URL=https://twoja-nazwa.bitrix24.pl/rest/12345/abc/

# Windows (PowerShell):
$env:BITRIX24_WEBHOOK_URL="https://twoja-nazwa.bitrix24.pl/rest/12345/abc/"

# Mac/Linux:
export BITRIX24_WEBHOOK_URL="https://twoja-nazwa.bitrix24.pl/rest/12345/abc/"

# 5. Uruchom import
python import_excel_to_bitrix.py

# 6. Poczekaj ~5-10 minut
# Zobaczysz logi:
# Created: 217
# Skipped: 0
# Errors: 0
```

**GOTOWE!** Teraz masz 217 ofert w Bitrix24.

### KROK B: Skonfiguruj GitHub (raz)

**Wszystkie pliki wgraj do repozytorium:**
```
properstar-sync/
├── .github/
│   └── workflows/
│       └── sync_properstar.yml    ← Ten plik!
├── bitrix24_properstar_sync.py
├── requirements.txt
├── README.md
└── .gitignore
```

**WAŻNE:** Folder `.github/workflows/` musi istnieć! GitHub Actions czyta stamtąd.

**Dodaj webhook URL do Secrets** (patrz punkt 1 powyżej).

**Włącz GitHub Pages** (Settings → Pages → Branch: gh-pages).

**Włącz uprawnienia** (Settings → Actions → General → Read and write permissions).

### KROK C: Testuj (raz)

```
1. Actions → "Properstar XML Sync" → "Run workflow"
2. Poczekaj 2 minuty
3. Sprawdź: https://twoj-login.github.io/repo/export.xml
```

### KROK D: Wyślij link do Properstar

```
To: support@properstar.com
CC: info@bitrix24.com

Subject: Data Feed Link - [Your Company]

Dear Michael,

Please find our Properstar XML data feed:

https://twoj-login.github.io/properstar-sync/export.xml

- Update frequency: Daily (4:00 AM UTC)
- Feed type: Full export
- Total properties: 217

Best regards,
[Your Name]
```

---

## 7️⃣ FAQ

**Q: Czy muszę mieć Python zainstalowany?**
A: Tylko jeśli chcesz importować oferty z Excel (KROK A). Do synchronizacji Bitrix24→XML wystarczy GitHub Actions (nie potrzebujesz Pythona).

**Q: Czy muszę płacić za GitHub?**
A: Nie! GitHub jest darmowy dla publicznych repozytoriów, a GitHub Actions ma 2000 minut/miesiąc za darmo (Twój workflow zajmuje ~2 minuty dziennie = 60 minut/miesiąc).

**Q: Co jeśli zmienię ofertę w Bitrix24?**
A: Przy następnej synchronizacji (o 4:00 rano lub gdy uruchomisz ręcznie) zaktualizowany XML będzie zawierał nowe dane.

**Q: Czy mogę uruchomić częściej niż raz dziennie?**
A: Tak! W pliku `sync_properstar.yml` zmień:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Co 6 godzin
  # lub
  - cron: '0 * * * *'     # Co godzinę
```

**Q: Gdzie są zdjęcia?**
A: Obecnie skrypt nie pobiera zdjęć. Aby dodać zdjęcia:
1. Musisz mieć pole na zdjęcia w Bitrix24 (np. UF_CRM_XXX)
2. Dodaj mapowanie w skrypcie
3. Skrypt pobierze URL-e i wyczyści je (usunie `?mode=max`)

**Q: Co jeśli mam błąd "BITRIX24_WEBHOOK_URL not set"?**
A: Upewnij się, że dodałeś secret w GitHub (Settings → Secrets → Actions).

---

## 8️⃣ SCHEMAT BEZPIECZEŃSTWA

```
❌ NIGDY NIE WKLEJAJ KLUCZA DO PLIKU .py
❌ NIGDY NIE COMMITUJ KLUCZA DO GITHUB
✅ ZAWSZE UŻYWAJ GITHUB SECRETS

Klucz jest BEZPIECZNIE przechowywany w GitHub Secrets.
Nikt nie może go zobaczyć (nawet Ty po dodaniu).
Tylko workflow ma do niego dostęp podczas wykonywania.
```

---

**Masz wszystko gotowe! Powodzenia z integracją! 🚀**

Jeśli coś nie działa - sprawdź logi w zakładce Actions na GitHub.
