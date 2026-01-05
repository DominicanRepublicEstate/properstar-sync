#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bitrix24 → Properstar XML Feed Generator
Synchronizes property listings from Bitrix24 CRM to Properstar-compatible XML format
"""

import os
import sys
import requests
import time
from datetime import datetime
from lxml import etree
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

BITRIX24_WEBHOOK_URL = os.environ.get('BITRIX24_WEBHOOK_URL')
if not BITRIX24_WEBHOOK_URL:
    print("ERROR: BITRIX24_WEBHOOK_URL environment variable is not set!")
    print("Please set it to: https://your-domain.bitrix24.com/rest/USER_ID/WEBHOOK_CODE/")
    sys.exit(1)

OUTPUT_FILE_TEMP = 'export.tmp.xml'
OUTPUT_FILE_FINAL = 'export.xml'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# BITRIX24 FIELD MAPPING
# Based on your bitrix24_pole_dodatkowe.txt file
# ============================================================================

FIELD_MAPPING = {
    # Property Identity
    'AdvertId': 'UF_CRM_201',
    'Reference': 'UF_CRM_202',
    'OriginalUrl': 'UF_CRM_203',
    
    # Property Type & Dates
    'AdvertType': 'UF_CRM_204',      # Lista: Sale/Rent
    'SubType': 'UF_CRM_205',         # Lista: Apartment/House/Villa/etc
    'PublicationDate': 'UF_CRM_206',
    'AvailabilityDate': 'UF_CRM_207',
    
    # Rooms & Spaces
    'Rooms': 'UF_CRM_208',
    'Bedrooms': 'UF_CRM_209',
    'Bathrooms': 'UF_CRM_210',
    'Toiletrooms': 'UF_CRM_211',
    'ShowerRooms': 'UF_CRM_212',
    'Carports': 'UF_CRM_213',
    'GaragesInside': 'UF_CRM_214',
    'GaragesOutside': 'UF_CRM_215',
    'ParkingLotsInside': 'UF_CRM_216',
    'ParkingLotsOutside': 'UF_CRM_217',
    'Floors': 'UF_CRM_218',
    'Flats': 'UF_CRM_219',
    'Balconies': 'UF_CRM_220',
    'Terraces': 'UF_CRM_221',
    
    # Areas (all in m²)
    'LivingArea': 'UF_CRM_222',
    'LandArea': 'UF_CRM_223',
    'TotalArea': 'UF_CRM_224',
    'CommercialArea': 'UF_CRM_225',
    'UsableArea': 'UF_CRM_226',
    'InternalArea': 'UF_CRM_227',
    'TerraceArea': 'UF_CRM_228',
    'GardenArea': 'UF_CRM_229',
    'BalconyArea': 'UF_CRM_230',
    'CellarArea': 'UF_CRM_231',
    
    # Price
    'Price': 'UF_CRM_232',
    'PriceCurrency': 'UF_CRM_233',
    'PricePeriod': 'UF_CRM_234',
    'ShowPrice': 'UF_CRM_235',
    'PriceDeposit': 'UF_CRM_236',
    'ServiceCharge': 'UF_CRM_237',
    'PriceMin': 'UF_CRM_238',
    'PriceMax': 'UF_CRM_239',
    
    # Location
    'Address': 'UF_CRM_240',
    'PostalCode': 'UF_CRM_241',
    'City': 'UF_CRM_242',
    'Country': 'UF_CRM_243',
    'ShowAddress': 'UF_CRM_244',
    'Latitude': 'UF_CRM_245',
    'Longitude': 'UF_CRM_246',
    
    # Energy Performance (for France, optional for other countries)
    'EnergyPerformanceGrade': 'UF_CRM_248',
    'EnergyPerformanceValue': 'UF_CRM_249',
    'CO2EmissionGrade': 'UF_CRM_250',
    'CO2EmissionValue': 'UF_CRM_251',
    'EnergyCostsPerYear_priceMin': 'UF_CRM_252',
    'EnergyCostsPerYear_priceMax': 'UF_CRM_253',
    'EnergyCostsPerYear_currencyId': 'UF_CRM_254',
    'EnergyCostsPerYear_referenceYear': 'UF_CRM_255',
    'EnergyCostsPerYear_certificateVersion': 'UF_CRM_256',
    'EnergyCostsPerYear_inspectionDate': 'UF_CRM_257',
    
    # Features
    'HeatingType': 'UF_CRM_258',
    'HeatingDevice': 'UF_CRM_259',
    'HotWaterDevice': 'UF_CRM_260',
    'Orientation': 'UF_CRM_261',
    'Condition': 'UF_CRM_262',
    'Activities': 'UF_CRM_263',
    'Proximities': 'UF_CRM_264',
    'Environment': 'UF_CRM_265',
    'Views': 'UF_CRM_266',
    
    # Contact - Office
    'OfficeOriginalId': 'UF_CRM_267',
    'CorporateName': 'UF_CRM_268',
    'Email': 'UF_CRM_269',
    'LandPhone': 'UF_CRM_270',
    'MobilePhone': 'UF_CRM_271',
    'Fax': 'UF_CRM_272',
    'Logo': 'UF_CRM_273',
    'Website': 'UF_CRM_274',
    'SpokenLanguages': 'UF_CRM_275',
    'OfficePostalCode': 'UF_CRM_276',
    'OfficeCity': 'UF_CRM_277',
    'OfficeAddress': 'UF_CRM_278',
    'OfficeCountry': 'UF_CRM_279',
    
    # Contact - Agent
    'AgentId': 'UF_CRM_280',
    'FullName': 'UF_CRM_281',
    'AgentEmail': 'UF_CRM_282',
    'AgentPhoto': 'UF_CRM_283',
    'AgentLandPhone': 'UF_CRM_284',
    'AgentMobilePhone': 'UF_CRM_285',
    'AgentWebsite': 'UF_CRM_286',
    'AgentAddress': 'UF_CRM_287',
    'AgentPostalCode': 'UF_CRM_288',
    'AgentCity': 'UF_CRM_289',
    'AgentCountry': 'UF_CRM_290',
}

# Standard Bitrix fields to fetch
STANDARD_FIELDS = ['ID', 'TITLE', 'COMMENTS', 'OPPORTUNITY']

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_url(url):
    """Remove query parameters like ?mode=max to get original quality images"""
    if not url:
        return None
    if isinstance(url, list):
        url = url[0]
    url_str = str(url)
    # Remove everything after '?' to get original file
    return url_str.split('?')[0]


def safe_get(data, field_id, default=None):
    """Safely get value from Bitrix deal data"""
    value = data.get(field_id, default)
    # Handle empty strings
    if value == '' or value == 'null':
        return default
    return value


def safe_int(value, default=None):
    """Safely convert to integer"""
    try:
        if value is None or value == '':
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default


def safe_float(value, default=None):
    """Safely convert to float"""
    try:
        if value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def format_iso_date(date_str):
    """Convert Bitrix date to ISO 8601 format"""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    
    # Bitrix usually returns dates like "2024-01-15T10:30:00+00:00"
    # We need just "2024-01-15"
    try:
        if 'T' in str(date_str):
            return str(date_str).split('T')[0]
        return str(date_str)[:10]
    except:
        return datetime.now().strftime('%Y-%m-%d')


# ============================================================================
# BITRIX24 API FUNCTIONS
# ============================================================================

def fetch_all_deals():
    """Fetch all deals from Bitrix24 with pagination"""
    logger.info("Starting to fetch deals from Bitrix24...")
    
    all_deals = []
    start = 0
    batch_size = 50
    
    # Prepare fields to fetch
    select_fields = list(FIELD_MAPPING.values()) + STANDARD_FIELDS
    
    while True:
        try:
            url = f"{BITRIX24_WEBHOOK_URL}crm.deal.list.json"
            payload = {
                'start': start,
                'select': select_fields,
                'filter': {
                    # Optional: Filter only active deals
                    # 'STAGE_ID': 'C1:NEW'  # Adjust to your pipeline stages
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'result' in data and data['result']:
                deals = data['result']
                all_deals.extend(deals)
                logger.info(f"Fetched {len(deals)} deals (total: {len(all_deals)})")
                
                # Check if there are more results
                if 'next' in data:
                    start = data['next']
                    time.sleep(0.5)  # Be nice to the API
                else:
                    break
            else:
                logger.info("No more deals to fetch")
                break
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching deals from Bitrix24: {e}")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break
    
    logger.info(f"Finished fetching. Total deals: {len(all_deals)}")
    return all_deals


# ============================================================================
# XML GENERATION
# ============================================================================

def create_properstar_xml(deals):
    """Generate Properstar-compatible XML from Bitrix24 deals"""
    logger.info("Generating Properstar XML...")
    
    # Create root element
    root = etree.Element("Adverts")
    
    properties_added = 0
    
    for deal in deals:
        # Get AdvertId - skip if missing
        advert_id = safe_get(deal, FIELD_MAPPING['AdvertId'])
        if not advert_id:
            logger.warning(f"Skipping deal without AdvertId: {deal.get('ID')}")
            continue
        
        # Create <Advert> element
        advert = etree.SubElement(root, "Advert")
        
        # ---- MANDATORY FIELDS ----
        
        # AdvertId (mandatory)
        etree.SubElement(advert, "AdvertId").text = str(advert_id)
        
        # Reference (optional but recommended)
        reference = safe_get(deal, FIELD_MAPPING['Reference'])
        if reference:
            etree.SubElement(advert, "Reference").text = str(reference)
        
        # OriginalUrl (optional)
        original_url = safe_get(deal, FIELD_MAPPING['OriginalUrl'])
        if original_url:
            etree.SubElement(advert, "OriginalUrl").text = str(original_url)
        
        # AdvertType (mandatory: Sale or Rent)
        advert_type = safe_get(deal, FIELD_MAPPING['AdvertType'], 'Sale')
        # Handle if Bitrix returns list ID instead of value
        if str(advert_type).isdigit():
            advert_type = 'Sale'  # Default fallback
        etree.SubElement(advert, "AdvertType").text = str(advert_type)
        
        # SubType (mandatory: Apartment, House, Villa, etc)
        sub_type = safe_get(deal, FIELD_MAPPING['SubType'], 'Apartment')
        etree.SubElement(advert, "SubType").text = str(sub_type)
        
        # PublicationDate
        pub_date = safe_get(deal, FIELD_MAPPING['PublicationDate'])
        etree.SubElement(advert, "PublicationDate").text = format_iso_date(pub_date)
        
        # AvailabilityDate (for rentals)
        avail_date = safe_get(deal, FIELD_MAPPING['AvailabilityDate'])
        if avail_date:
            etree.SubElement(advert, "AvailabilityDate").text = format_iso_date(avail_date)
        
        # ---- ROOMS & SPACES ----
        
        rooms = safe_float(safe_get(deal, FIELD_MAPPING['Rooms']))
        if rooms:
            etree.SubElement(advert, "Rooms").text = str(rooms)
        
        bedrooms = safe_int(safe_get(deal, FIELD_MAPPING['Bedrooms']))
        if bedrooms:
            etree.SubElement(advert, "Bedrooms").text = str(bedrooms)
        
        bathrooms = safe_int(safe_get(deal, FIELD_MAPPING['Bathrooms']))
        if bathrooms:
            etree.SubElement(advert, "Bathrooms").text = str(bathrooms)
        
        toiletrooms = safe_int(safe_get(deal, FIELD_MAPPING['Toiletrooms']))
        if toiletrooms:
            etree.SubElement(advert, "Toiletrooms").text = str(toiletrooms)
        
        showerrooms = safe_int(safe_get(deal, FIELD_MAPPING['ShowerRooms']))
        if showerrooms:
            etree.SubElement(advert, "ShowerRooms").text = str(showerrooms)
        
        carports = safe_int(safe_get(deal, FIELD_MAPPING['Carports']))
        if carports:
            etree.SubElement(advert, "Carports").text = str(carports)
        
        garages_inside = safe_int(safe_get(deal, FIELD_MAPPING['GaragesInside']))
        if garages_inside:
            etree.SubElement(advert, "GaragesInside").text = str(garages_inside)
        
        garages_outside = safe_int(safe_get(deal, FIELD_MAPPING['GaragesOutside']))
        if garages_outside:
            etree.SubElement(advert, "GaragesOutside").text = str(garages_outside)
        
        parking_inside = safe_int(safe_get(deal, FIELD_MAPPING['ParkingLotsInside']))
        if parking_inside:
            etree.SubElement(advert, "ParkingLotsInside").text = str(parking_inside)
        
        parking_outside = safe_int(safe_get(deal, FIELD_MAPPING['ParkingLotsOutside']))
        if parking_outside:
            etree.SubElement(advert, "ParkingLotsOutside").text = str(parking_outside)
        
        floors = safe_int(safe_get(deal, FIELD_MAPPING['Floors']))
        if floors:
            etree.SubElement(advert, "Floors").text = str(floors)
        
        flats = safe_int(safe_get(deal, FIELD_MAPPING['Flats']))
        if flats:
            etree.SubElement(advert, "Flats").text = str(flats)
        
        balconies = safe_int(safe_get(deal, FIELD_MAPPING['Balconies']))
        if balconies:
            etree.SubElement(advert, "Balconies").text = str(balconies)
        
        terraces = safe_int(safe_get(deal, FIELD_MAPPING['Terraces']))
        if terraces:
            etree.SubElement(advert, "Terraces").text = str(terraces)
        
        # ---- AREAS (all in m²) ----
        
        living_area = safe_int(safe_get(deal, FIELD_MAPPING['LivingArea']))
        if living_area:
            etree.SubElement(advert, "LivingArea").text = str(living_area)
        
        land_area = safe_int(safe_get(deal, FIELD_MAPPING['LandArea']))
        if land_area:
            etree.SubElement(advert, "LandArea").text = str(land_area)
        
        total_area = safe_int(safe_get(deal, FIELD_MAPPING['TotalArea']))
        if total_area:
            etree.SubElement(advert, "TotalArea").text = str(total_area)
        
        commercial_area = safe_int(safe_get(deal, FIELD_MAPPING['CommercialArea']))
        if commercial_area:
            etree.SubElement(advert, "CommercialArea").text = str(commercial_area)
        
        usable_area = safe_int(safe_get(deal, FIELD_MAPPING['UsableArea']))
        if usable_area:
            etree.SubElement(advert, "UsableArea").text = str(usable_area)
        
        internal_area = safe_int(safe_get(deal, FIELD_MAPPING['InternalArea']))
        if internal_area:
            etree.SubElement(advert, "InternalArea").text = str(internal_area)
        
        terrace_area = safe_int(safe_get(deal, FIELD_MAPPING['TerraceArea']))
        if terrace_area:
            etree.SubElement(advert, "TerraceArea").text = str(terrace_area)
        
        garden_area = safe_int(safe_get(deal, FIELD_MAPPING['GardenArea']))
        if garden_area:
            etree.SubElement(advert, "GardenArea").text = str(garden_area)
        
        balcony_area = safe_int(safe_get(deal, FIELD_MAPPING['BalconyArea']))
        if balcony_area:
            etree.SubElement(advert, "BalconyArea").text = str(balcony_area)
        
        cellar_area = safe_int(safe_get(deal, FIELD_MAPPING['CellarArea']))
        if cellar_area:
            etree.SubElement(advert, "CellarArea").text = str(cellar_area)
        
        # ---- TITLES (multilingual with CDATA) ----
        
        # Use TITLE field from Bitrix
        title_text = safe_get(deal, 'TITLE', 'Property for Sale')
        titles = etree.SubElement(advert, "Titles")
        title_elem = etree.SubElement(titles, "Title", Language="en")
        title_elem.text = etree.CDATA(title_text)
        
        # ---- DESCRIPTIONS (multilingual with CDATA) ----
        
        # Use COMMENTS field from Bitrix
        description_text = safe_get(deal, 'COMMENTS', '')
        if description_text:
            descriptions = etree.SubElement(advert, "Descriptions")
            desc_elem = etree.SubElement(descriptions, "Description", Language="en")
            desc_elem.text = etree.CDATA(description_text)
        
        # ---- PHOTOS ----
        # Note: In your Bitrix setup, photos might be stored in a different way
        # You'll need to check how images are stored and adjust this section
        # For now, this is a placeholder
        photos = etree.SubElement(advert, "Photos")
        # TODO: Add logic to fetch photos from Bitrix24
        # This might require additional API calls to get file URLs
        
        # ---- PRICE ----
        
        price = safe_float(safe_get(deal, FIELD_MAPPING['Price']))
        if price:
            etree.SubElement(advert, "Price").text = str(price)
        
        currency = safe_get(deal, FIELD_MAPPING['PriceCurrency'], 'USD')
        etree.SubElement(advert, "PriceCurrency").text = str(currency)
        
        price_period = safe_get(deal, FIELD_MAPPING['PricePeriod'])
        if price_period:
            etree.SubElement(advert, "PricePeriod").text = str(price_period)
        
        show_price = safe_get(deal, FIELD_MAPPING['ShowPrice'])
        if show_price is not None:
            etree.SubElement(advert, "ShowPrice").text = 'True' if show_price else 'False'
        
        price_deposit = safe_float(safe_get(deal, FIELD_MAPPING['PriceDeposit']))
        if price_deposit:
            etree.SubElement(advert, "PriceDeposit").text = str(price_deposit)
        
        service_charge = safe_float(safe_get(deal, FIELD_MAPPING['ServiceCharge']))
        if service_charge:
            etree.SubElement(advert, "ServiceCharge").text = str(service_charge)
        
        price_min = safe_float(safe_get(deal, FIELD_MAPPING['PriceMin']))
        if price_min:
            etree.SubElement(advert, "PriceMin").text = str(price_min)
        
        price_max = safe_float(safe_get(deal, FIELD_MAPPING['PriceMax']))
        if price_max:
            etree.SubElement(advert, "PriceMax").text = str(price_max)
        
        # ---- LOCATION ----
        
        country = safe_get(deal, FIELD_MAPPING['Country'], 'DO')  # Default to Dominican Republic
        etree.SubElement(advert, "Country").text = str(country)
        
        address = safe_get(deal, FIELD_MAPPING['Address'], '')
        if address:
            etree.SubElement(advert, "Address").text = str(address)
        
        show_address = safe_get(deal, FIELD_MAPPING['ShowAddress'])
        if show_address is not None:
            etree.SubElement(advert, "ShowAddress").text = 'True' if show_address else 'False'
        
        postal_code = safe_get(deal, FIELD_MAPPING['PostalCode'])
        if postal_code:
            etree.SubElement(advert, "PostalCode").text = str(postal_code)
        
        city = safe_get(deal, FIELD_MAPPING['City'])
        if city:
            etree.SubElement(advert, "City").text = str(city)
        
        # Geolocation
        latitude = safe_get(deal, FIELD_MAPPING['Latitude'])
        longitude = safe_get(deal, FIELD_MAPPING['Longitude'])
        if latitude and longitude:
            geolocation = etree.SubElement(advert, "Geolocation")
            etree.SubElement(geolocation, "Latitude").text = str(latitude)
            etree.SubElement(geolocation, "Longitude").text = str(longitude)
        
        # ---- CONTACT INFORMATION (mandatory) ----
        
        contact = etree.SubElement(advert, "Contact")
        
        # Office information
        office_id = safe_get(deal, FIELD_MAPPING['OfficeOriginalId'], 'OFFICE_001')
        etree.SubElement(contact, "OfficeOriginalId").text = str(office_id)
        
        corporate_name = safe_get(deal, FIELD_MAPPING['CorporateName'], 'Dominican Republic Estate')
        etree.SubElement(contact, "CorporateName").text = str(corporate_name)
        
        email = safe_get(deal, FIELD_MAPPING['Email'], 'info@drestate.com')
        etree.SubElement(contact, "Email").text = str(email)
        
        land_phone = safe_get(deal, FIELD_MAPPING['LandPhone'])
        if land_phone:
            etree.SubElement(contact, "LandPhone").text = str(land_phone)
        
        mobile_phone = safe_get(deal, FIELD_MAPPING['MobilePhone'])
        if mobile_phone:
            etree.SubElement(contact, "MobilePhone").text = str(mobile_phone)
        
        fax = safe_get(deal, FIELD_MAPPING['Fax'])
        if fax:
            etree.SubElement(contact, "Fax").text = str(fax)
        
        website = safe_get(deal, FIELD_MAPPING['Website'])
        if website:
            etree.SubElement(contact, "Website").text = clean_url(website)
        
        logo = safe_get(deal, FIELD_MAPPING['Logo'])
        if logo:
            etree.SubElement(contact, "Logo").text = clean_url(logo)
        
        office_postal_code = safe_get(deal, FIELD_MAPPING['OfficePostalCode'])
        if office_postal_code:
            etree.SubElement(contact, "PostalCode").text = str(office_postal_code)
        
        office_city = safe_get(deal, FIELD_MAPPING['OfficeCity'])
        if office_city:
            etree.SubElement(contact, "City").text = str(office_city)
        
        office_address = safe_get(deal, FIELD_MAPPING['OfficeAddress'])
        if office_address:
            etree.SubElement(contact, "Address").text = str(office_address)
        
        office_country = safe_get(deal, FIELD_MAPPING['OfficeCountry'])
        if office_country:
            etree.SubElement(contact, "Country").text = str(office_country)
        
        # Agent information
        agent_id = safe_get(deal, FIELD_MAPPING['AgentId'])
        if agent_id:
            etree.SubElement(contact, "AgentId").text = str(agent_id)
            
            full_name = safe_get(deal, FIELD_MAPPING['FullName'])
            if full_name:
                etree.SubElement(contact, "FullName").text = str(full_name)
            
            agent_email = safe_get(deal, FIELD_MAPPING['AgentEmail'])
            if agent_email:
                etree.SubElement(contact, "AgentEmail").text = str(agent_email)
            
            agent_photo = safe_get(deal, FIELD_MAPPING['AgentPhoto'])
            if agent_photo:
                etree.SubElement(contact, "Photo").text = clean_url(agent_photo)
            
            agent_land_phone = safe_get(deal, FIELD_MAPPING['AgentLandPhone'])
            if agent_land_phone:
                etree.SubElement(contact, "AgentLandPhone").text = str(agent_land_phone)
            
            agent_mobile = safe_get(deal, FIELD_MAPPING['AgentMobilePhone'])
            if agent_mobile:
                etree.SubElement(contact, "AgentMobilePhone").text = str(agent_mobile)
            
            agent_website = safe_get(deal, FIELD_MAPPING['AgentWebsite'])
            if agent_website:
                etree.SubElement(contact, "AgentWebsite").text = clean_url(agent_website)
        
        properties_added += 1
    
    logger.info(f"Generated XML with {properties_added} properties")
    return root


def save_xml(root, output_path):
    """Save XML tree to file with proper formatting"""
    try:
        tree = etree.ElementTree(root)
        with open(output_path, 'wb') as f:
            tree.write(
                f,
                pretty_print=True,
                xml_declaration=True,
                encoding='UTF-8'
            )
        logger.info(f"XML saved to: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving XML: {e}")
        return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("Bitrix24 → Properstar XML Sync Starting")
    logger.info("=" * 80)
    
    # Step 1: Fetch deals from Bitrix24
    deals = fetch_all_deals()
    
    if not deals:
        logger.warning("No deals fetched from Bitrix24. Exiting.")
        return
    
    # Step 2: Generate XML
    xml_root = create_properstar_xml(deals)
    
    # Step 3: Save to temporary file first (atomic write)
    if save_xml(xml_root, OUTPUT_FILE_TEMP):
        # Step 4: Rename to final file (atomic operation)
        try:
            if os.path.exists(OUTPUT_FILE_FINAL):
                os.remove(OUTPUT_FILE_FINAL)
            os.rename(OUTPUT_FILE_TEMP, OUTPUT_FILE_FINAL)
            logger.info(f"Successfully created {OUTPUT_FILE_FINAL}")
            logger.info("=" * 80)
            logger.info("✓ Sync completed successfully!")
            logger.info("=" * 80)
        except Exception as e:
            logger.error(f"Error renaming file: {e}")
    else:
        logger.error("Failed to save XML file")


if __name__ == "__main__":
    main()
