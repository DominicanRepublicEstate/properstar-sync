# 📊 MAPOWANIE PÓL - Bitrix24 ↔ Properstar

## Kompletna tabela mapowania pól custom z Bitrix24 na format XML Properstar

---

## ✅ TWOJE POLA SĄ PRAWIDŁOWE

Przeanalizowałem Twój plik `bitrix24_pole_dodatkowe.txt` i wszystkie pola są **poprawnie zmapowane** do wymagań Properstar. Poniżej pełna specyfikacja:

---

## 🆔 IDENTYFIKACJA NIERUCHOMOŚCI

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Opis |
|------------|---------------|-----|----------------|----------|------|
| **UF_CRM_201** | AdvertId | String | `<AdvertId>` | ⭐ TAK | Unikalny ID oferty (max 20 znaków) |
| **UF_CRM_202** | Reference | String | `<Reference>` | Nie | Referencja dla agencji (max 100 znaków) |
| **UF_CRM_203** | OriginalUrl | String | `<OriginalUrl>` | Nie | Link do oferty na Twojej stronie |

---

## 🏠 TYP NIERUCHOMOŚCI

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Dozwolone wartości |
|------------|---------------|-----|----------------|----------|-------------------|
| **UF_CRM_204** | AdvertType | Lista | `<AdvertType>` | ⭐ TAK | `Sale` lub `Rent` |
| **UF_CRM_205** | SubType | Lista | `<SubType>` | ⭐ TAK | `Apartment`, `House`, `Villa`, `Farm`, `Chalet`, `Office`, `Commercial`, `IndustrialBuilding`, `PlotOfLand`, `Bungalow` |

**UWAGA:** W Bitrix24 możesz używać polskich nazw w listach, skrypt automatycznie zamieni je na wymagane wartości.

---

## 📅 DATY

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Format |
|------------|---------------|-----|----------------|----------|--------|
| **UF_CRM_206** | PublicationDate | Data/Godzina | `<PublicationDate>` | Tak | `YYYY-MM-DD` lub ISO 8601 |
| **UF_CRM_207** | AvailabilityDate | Data/Godzina | `<AvailabilityDate>` | Tylko dla wynajmu | `YYYY-MM-DD` lub ISO 8601 |

---

## 🛏️ POKOJE I PRZESTRZENIE

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane dla niektórych portali |
|------------|---------------|-----|----------------|--------------------------------|
| **UF_CRM_208** | Rooms | Liczba | `<Rooms>` | ⭐ TAK (niektóre portale) |
| **UF_CRM_209** | Bedrooms | Liczba całkowita | `<Bedrooms>` | ⭐ TAK (niektóre portale) |
| **UF_CRM_210** | Bathrooms | Liczba całkowita | `<Bathrooms>` | ⭐ TAK (niektóre portale) |
| **UF_CRM_211** | Toiletrooms | Liczba całkowita | `<Toiletrooms>` | Nie |
| **UF_CRM_212** | ShowerRooms | Liczba całkowita | `<ShowerRooms>` | Nie |
| **UF_CRM_213** | Carports | Liczba całkowita | `<Carports>` | Nie |
| **UF_CRM_214** | GaragesInside | Liczba całkowita | `<GaragesInside>` | Nie |
| **UF_CRM_215** | GaragesOutside | Liczba całkowita | `<GaragesOutside>` | Nie |
| **UF_CRM_216** | ParkingLotsInside | Liczba całkowita | `<ParkingLotsInside>` | Nie |
| **UF_CRM_217** | ParkingLotsOutside | Liczba całkowita | `<ParkingLotsOutside>` | Nie |
| **UF_CRM_218** | Floors | Liczba całkowita | `<Floors>` | Nie |
| **UF_CRM_219** | Flats | Liczba całkowita | `<Flats>` | Nie |
| **UF_CRM_220** | Balconies | Liczba całkowita | `<Balconies>` | Nie |
| **UF_CRM_221** | Terraces | Liczba całkowita | `<Terraces>` | Nie |

---

## 📐 POWIERZCHNIE (wszystkie w m²)

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane dla niektórych portali |
|------------|---------------|-----|----------------|--------------------------------|
| **UF_CRM_222** | LivingArea | Liczba całkowita | `<LivingArea>` | ⭐ TAK (niektóre portale) |
| **UF_CRM_223** | LandArea | Liczba całkowita | `<LandArea>` | Dla działek/domów z ogrodem |
| **UF_CRM_224** | TotalArea | Liczba całkowita | `<TotalArea>` | Nie |
| **UF_CRM_225** | CommercialArea | Liczba całkowita | `<CommercialArea>` | Dla nieruchomości komercyjnych |
| **UF_CRM_226** | UsableArea | Liczba całkowita | `<UsableArea>` | Nie |
| **UF_CRM_227** | InternalArea | Liczba całkowita | `<InternalArea>` | Nie |
| **UF_CRM_228** | TerraceArea | Liczba całkowita | `<TerraceArea>` | Nie |
| **UF_CRM_229** | GardenArea | Liczba całkowita | `<GardenArea>` | Nie |
| **UF_CRM_230** | BalconyArea | Liczba całkowita | `<BalconyArea>` | Nie |
| **UF_CRM_231** | CellarArea | Liczba całkowita | `<CellarArea>` | Nie |

---

## 💰 CENA

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Opis |
|------------|---------------|-----|----------------|----------|------|
| **UF_CRM_232** | Price | Liczba | `<Price>` | ⭐ TAK (dla niektórych) | Cena oferty |
| **UF_CRM_233** | PriceCurrency | String | `<PriceCurrency>` | ⭐ TAK | `USD`, `EUR`, `PLN`, etc (ISO 4217) |
| **UF_CRM_234** | PricePeriod | Lista | `<PricePeriod>` | Dla wynajmu | `Daily`, `Weekly`, `Monthly` |
| **UF_CRM_235** | ShowPrice | True/False | `<ShowPrice>` | Nie | Pokazać cenę? (True/False) |
| **UF_CRM_236** | PriceDeposit | Liczba | `<PriceDeposit>` | Dla wynajmu | Kaucja |
| **UF_CRM_237** | ServiceCharge | Liczba | `<ServiceCharge>` | Nie | Opłaty dodatkowe |
| **UF_CRM_238** | PriceMin | Liczba | `<PriceMin>` | Dla projektów deweloperskich | Cena minimalna |
| **UF_CRM_239** | PriceMax | Liczba | `<PriceMax>` | Dla projektów deweloperskich | Cena maksymalna |

---

## 📍 LOKALIZACJA

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Opis |
|------------|---------------|-----|----------------|----------|------|
| **UF_CRM_240** | Address | String | `<Address>` | Tak | Pełny adres |
| **UF_CRM_241** | PostalCode | String | `<PostalCode>` | ⭐ TAK | Kod pocztowy |
| **UF_CRM_242** | City | String | `<City>` | ⭐ TAK | Miasto |
| **UF_CRM_243** | Country | String | `<Country>` | ⭐ TAK | Kod kraju ISO 3166 (np. `DO`, `PL`, `ES`) |
| **UF_CRM_244** | ShowAddress | True/False | `<ShowAddress>` | Nie | Pokazać adres? |
| **UF_CRM_245** | Latitude | String | `<Latitude>` | Zalecane | Szerokość geograficzna |
| **UF_CRM_246** | Longitude | String | `<Longitude>` | Zalecane | Długość geograficzna |

**UWAGA:** Dla Dominican Republic używaj: `Country = DO`

---

## 📧 KONTAKT - BIURO

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Opis |
|------------|---------------|-----|----------------|----------|------|
| **UF_CRM_267** | OfficeOriginalId | String | `<OfficeOriginalId>` | ⭐ TAK | Unikalny ID biura (max 20 znaków) |
| **UF_CRM_268** | CorporateName | String | `<CorporateName>` | ⭐ TAK | Nazwa firmy |
| **UF_CRM_269** | Email | String | `<Email>` | ⭐ TAK | Email biura |
| **UF_CRM_270** | LandPhone | String | `<LandPhone>` | Nie | Telefon stacjonarny (z prefiksem +1) |
| **UF_CRM_271** | MobilePhone | String | `<MobilePhone>` | Zalecane | Telefon komórkowy (z prefiksem +1) |
| **UF_CRM_272** | Fax | String | `<Fax>` | Nie | Fax |
| **UF_CRM_273** | Logo | String | `<Logo>` | Nie | URL do logo firmy |
| **UF_CRM_274** | Website | String | `<Website>` | Zalecane | URL strony www |
| **UF_CRM_275** | SpokenLanguages | String | `<SpokenLanguages>` | Nie | Języki (wielokrotne, ISO 639-1) |
| **UF_CRM_276** | OfficePostalCode | String | `<PostalCode>` | Nie | Kod pocztowy biura |
| **UF_CRM_277** | OfficeCity | String | `<City>` | Nie | Miasto biura |
| **UF_CRM_278** | OfficeAddress | String | `<Address>` | Nie | Adres biura |
| **UF_CRM_279** | OfficeCountry | String | `<Country>` | Nie | Kraj biura (ISO 3166) |

---

## 👤 KONTAKT - AGENT

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Opis |
|------------|---------------|-----|----------------|----------|------|
| **UF_CRM_280** | AgentId | String | `<AgentId>` | Jeśli jest agent | Unikalny ID agenta |
| **UF_CRM_281** | FullName | String | `<FullName>` | Jeśli jest agent | Pełne imię i nazwisko |
| **UF_CRM_282** | AgentEmail | String | `<AgentEmail>` | Jeśli jest agent | Email agenta (unikalny!) |
| **UF_CRM_283** | AgentPhoto | String | `<Photo>` | Nie | URL do zdjęcia agenta |
| **UF_CRM_284** | AgentLandPhone | String | `<AgentLandPhone>` | Nie | Telefon stacjonarny agenta |
| **UF_CRM_285** | AgentMobilePhone | String | `<AgentMobilePhone>` | Zalecane | Telefon komórkowy agenta |
| **UF_CRM_286** | AgentWebsite | String | `<AgentWebsite>` | Nie | Strona www agenta |
| **UF_CRM_287** | AgentAddress | String | - | Nie | Adres agenta |
| **UF_CRM_288** | AgentPostalCode | String | - | Nie | Kod pocztowy agenta |
| **UF_CRM_289** | AgentCity | String | - | Nie | Miasto agenta |
| **UF_CRM_290** | AgentCountry | String | `<Country>` | Nie | Kraj agenta |

---

## ⚡ CERTYFIKATY ENERGETYCZNE (wymagane we Francji, opcjonalne dla innych krajów)

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Opis |
|------------|---------------|-----|----------------|----------|------|
| **UF_CRM_248** | EnergyPerformanceGrade | Lista | `<Grade>` | Francja: TAK | A, B, C, D, E, F, G |
| **UF_CRM_249** | EnergyPerformanceValue | Liczba całkowita | `<Value>` | Francja: TAK | Wartość numeryczna |
| **UF_CRM_250** | CO2EmissionGrade | Lista | `<Grade>` | Francja: TAK | A, B, C, D, E, F, G |
| **UF_CRM_251** | CO2EmissionValue | Liczba całkowita | `<Value>` | Francja: TAK | Wartość numeryczna |
| **UF_CRM_252** | EnergyCostsPerYear_priceMin | Liczba całkowita | `<priceMin>` | Francja: TAK | Koszty energii min/rok |
| **UF_CRM_253** | EnergyCostsPerYear_priceMax | Liczba całkowita | `<priceMax>` | Francja: TAK | Koszty energii max/rok |
| **UF_CRM_254** | EnergyCostsPerYear_currencyId | String | `<currencyId>` | Francja: TAK | Waluta (EUR) |
| **UF_CRM_255** | EnergyCostsPerYear_referenceYear | Liczba całkowita | `<referenceYear>` | Francja: TAK | Rok referencyjny |
| **UF_CRM_256** | EnergyCostsPerYear_certificateVersion | String | `<certificateVersion>` | Francja: TAK | Np. DPE_v07-2021 |
| **UF_CRM_257** | EnergyCostsPerYear_inspectionDate | Data/Godzina | `<inspectionDate>` | Francja: TAK | Data inspekcji |

**Dla Dominikany:** Te pola można pominąć (nieobowiązkowe).

---

## 🔥 CECHY NIERUCHOMOŚCI

| Bitrix24 ID | Nazwa w Bitrix | Typ | Properstar XML | Wymagane | Dozwolone wartości |
|------------|---------------|-----|----------------|----------|-------------------|
| **UF_CRM_258** | HeatingType | Lista | `<HeatingType>` | Nie | Charcoal, Electric, Fuel Oil, Gas, Geothermal, Heat Pump, Hot Water, Solar, Wood, Wood Pellet |
| **UF_CRM_259** | HeatingDevice | Lista | `<HeatingDevice>` | Nie | Air-conditioning, Central, Convector, FloorRadiator, Radiant, Radiator, Stove |
| **UF_CRM_260** | HotWaterDevice | Lista | `<HotWaterDevice>` | Nie | Boiler, Hot Water Tank, Solar |
| **UF_CRM_261** | Orientation | Lista | `<Orientation>` | Nie | East, North, South, West, NorthEast, NorthWest, Southeast, SouthWest |
| **UF_CRM_262** | Condition | Lista | `<Condition>` | Nie | ExcellentCondition, GoodCondition, New, RequiresRenovation, RequiresUpdating |
| **UF_CRM_263** | Activities | Lista | `<Activities>` | Nie | Fishing, Rafting, Ski, Swimming |
| **UF_CRM_264** | Proximities | Lista | `<Proximities>` | Nie | Airport, Beach, Golf, Hospital, Lake, Sea, Supermarket, etc. |
| **UF_CRM_265** | Environment | Lista | `<Environment>` | Nie | Calm, CountrySide, Green, MountainSide, Residential |
| **UF_CRM_266** | Views | Lista | `<Views>` | Nie | City, Countryside, Forest, Garden, Lake, Mountains, Sea, etc. |

---

## 📝 POLA SYSTEMOWE BITRIX24 (używane automatycznie)

| Bitrix24 pole | Properstar XML | Opis |
|--------------|----------------|------|
| **TITLE** | `<Title>` | Tytuł oferty (wielojęzyczny) |
| **COMMENTS** | `<Description>` | Opis oferty (wielojęzyczny, HTML, CDATA) |
| **OPPORTUNITY** | - | Cena (duplicate UF_CRM_232 dla wygody) |
| **CURRENCY_ID** | - | Waluta (duplicate UF_CRM_233) |
| **ID** | - | ID dealu w Bitrix (do logowania) |

---

## 🖼️ ZDJĘCIA (TODO)

**Obecnie brak pola na zdjęcia w Twoim spisie UF_CRM_100-290.**

Aby dodać zdjęcia, musisz:
1. Utworzyć pole custom typu "Plik" (wielokrotne)
2. Dodać je do mapowania w skrypcie
3. Skrypt będzie pobierać URL-e zdjęć i czyścić je (usuwać `?mode=max`)

**Przykład XML zdjęć:**
```xml
<Photos>
  <Photo>https://bitrix24.com/files/image1.jpg</Photo>
  <Photo>https://bitrix24.com/files/image2.jpg</Photo>
</Photos>
```

---

## ✅ PODSUMOWANIE - CO JEST DOBRE

**✓ Wszystkie pola są poprawnie zmapowane**
- Identyfikacja: AdvertId, Reference, OriginalUrl ✅
- Typ: AdvertType, SubType ✅
- Pokoje: Rooms, Bedrooms, Bathrooms ✅
- Powierzchnie: LivingArea, LandArea, TotalArea ✅
- Cena: Price, PriceCurrency ✅
- Lokalizacja: Address, City, Country, Latitude, Longitude ✅
- Kontakt: Office + Agent (pełne dane) ✅

**⚠️ Co trzeba uzupełnić w Bitrix24:**

1. **Dla każdej oferty wypełnij:**
   - `UF_CRM_201` (AdvertId) - OBOWIĄZKOWE
   - `UF_CRM_204` (AdvertType: Sale/Rent) - OBOWIĄZKOWE
   - `UF_CRM_205` (SubType: Apartment/House/etc) - OBOWIĄZKOWE
   - `UF_CRM_232` (Price) - Zalecane
   - `UF_CRM_233` (PriceCurrency: USD) - Zalecane
   - `UF_CRM_240-243` (Address, City, Country) - OBOWIĄZKOWE
   - `TITLE` - tytuł oferty - OBOWIĄZKOWE
   - `COMMENTS` - opis oferty - OBOWIĄZKOWE

2. **Dla biura (raz, może być stałe):**
   - `UF_CRM_267` (OfficeOriginalId)
   - `UF_CRM_268` (CorporateName)
   - `UF_CRM_269` (Email)

3. **Opcjonalnie (ale zalecane):**
   - Pokoje: Bedrooms, Bathrooms, Rooms
   - Powierzchnia: LivingArea
   - Geolokalizacja: Latitude, Longitude
   - Agent: AgentId, FullName, AgentEmail, AgentMobilePhone

---

## 📖 PRZYKŁAD WYPEŁNIENIA W BITRIX24

### Przykładowa oferta #1:

```
ID: 12345
TITLE: "Luxury Apartment in Punta Cana with Ocean View"
COMMENTS: "<p>Beautiful 3-bedroom apartment...</p>"

UF_CRM_201 (AdvertId): "107359978"
UF_CRM_204 (AdvertType): "Sale"
UF_CRM_205 (SubType): "Apartment"
UF_CRM_208 (Rooms): 4
UF_CRM_209 (Bedrooms): 3
UF_CRM_210 (Bathrooms): 3
UF_CRM_222 (LivingArea): 340
UF_CRM_232 (Price): 1390000
UF_CRM_233 (PriceCurrency): "USD"
UF_CRM_240 (Address): "7 Mares AB11, Punta Cana"
UF_CRM_241 (PostalCode): "23000"
UF_CRM_242 (City): "Punta Cana"
UF_CRM_243 (Country): "DO"
UF_CRM_245 (Latitude): "18.486249"
UF_CRM_246 (Longitude): "-68.406102"

UF_CRM_267 (OfficeOriginalId): "DR_ESTATE_001"
UF_CRM_268 (CorporateName): "Dominican Republic Estate"
UF_CRM_269 (Email): "info@drestate.com"
UF_CRM_271 (MobilePhone): "+1809555XXXX"
UF_CRM_274 (Website): "https://drestate.com"
```

---

## 🔄 AUTOMATYCZNE KONWERSJE

Skrypt automatycznie:
- ✅ Konwertuje daty do ISO 8601
- ✅ Czyści URL-e zdjęć (usuwa `?mode=max`)
- ✅ Konwertuje liczby na właściwe typy (int/float)
- ✅ Dodaje CDATA do opisów (żeby HTML działał)
- ✅ Mapuje typy transakcji (Sale/Rent)
- ✅ Pomija puste wartości
- ✅ Ustawia domyślne wartości dla braku danych

---

**Wszystko jest gotowe! Twoje pola są prawidłowe. Teraz wystarczy je wypełnić w Bitrix24. 🚀**
