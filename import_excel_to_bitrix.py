#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import properties from Excel file to Bitrix24 CRM
This script imports the 217 properties from your Dominican Republic Estate export
"""

import os
import sys
import pandas as pd
import requests
import time
import logging
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

BITRIX24_WEBHOOK_URL = os.environ.get('BITRIX24_WEBHOOK_URL')
if not BITRIX24_WEBHOOK_URL:
    print("ERROR: BITRIX24_WEBHOOK_URL environment variable is not set!")
    print("Please set it to: https://your-domain.bitrix24.com/rest/USER_ID/WEBHOOK_CODE/")
    sys.exit(1)

EXCEL_FILE = 'Dominican_Republic_Estate_listings_data_export__3_.xlsx'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# FIELD MAPPING - Excel columns to Bitrix24 UF_CRM fields
# ============================================================================

# Map Excel columns to Bitrix24 custom fields
EXCEL_TO_BITRIX_MAPPING = {
    # Identity
    'id': 'UF_CRM_201',                    # AdvertId
    'reference': 'UF_CRM_202',             # Reference
    
    # Type mapping
    'transactionTypeId': 'UF_CRM_204',     # AdvertType (Sale/Rent)
    'propertyType': 'UF_CRM_205',          # SubType (Apartment/House/etc)
    
    # Rooms & Spaces
    'numberOfRooms': 'UF_CRM_208',         # Rooms
    'numberOfBedrooms': 'UF_CRM_209',      # Bedrooms
    'numberOfBathrooms': 'UF_CRM_210',     # Bathrooms
    'numberOfToiletrooms': 'UF_CRM_211',   # Toiletrooms
    'numberOfBalconies': 'UF_CRM_220',     # Balconies
    'numberOfParkingLotsInside': 'UF_CRM_216',   # ParkingLotsInside
    'numberOfParkingLotsOutside': 'UF_CRM_217',  # ParkingLotsOutside
    'numberOfTerraces': 'UF_CRM_221',      # Terraces
    
    # Areas
    'areaLiving': 'UF_CRM_222',            # LivingArea
    'areaLand': 'UF_CRM_223',              # LandArea
    
    # Price
    'priceValue': 'UF_CRM_232',            # Price
    'currencyId': 'UF_CRM_233',            # PriceCurrency
    
    # Location
    'placeAddress1': 'UF_CRM_240',         # Address
    'placePostcode': 'UF_CRM_241',         # PostalCode
    'placeCity': 'UF_CRM_242',             # City
    'placeCountryISO': 'UF_CRM_243',       # Country
    'latitude': 'UF_CRM_245',              # Latitude
    'longitude': 'UF_CRM_246',             # Longitude
    
    # Construction year (if needed for other fields)
    'constructionYear': None,  # Not in standard mapping, can add if needed
}

# Transaction type conversion
TRANSACTION_TYPE_MAP = {
    'Sale': 'Sale',
    'Rent': 'Rent',
    'sale': 'Sale',
    'rent': 'Rent',
}

# Property type conversion (adjust based on your Bitrix24 list values)
PROPERTY_TYPE_MAP = {
    'Apartment': 'Apartment',
    'House': 'House',
    'Villa': 'Villa',
    'Land': 'PlotOfLand',
    'Commercial': 'Commercial',
}

# ============================================================================
# BITRIX24 API FUNCTIONS
# ============================================================================

def create_deal_in_bitrix(deal_data):
    """Create a new deal in Bitrix24"""
    try:
        url = f"{BITRIX24_WEBHOOK_URL}crm.deal.add.json"
        payload = {
            'fields': deal_data
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if 'result' in result:
            return result['result']  # Returns the new deal ID
        else:
            logger.error(f"Error creating deal: {result}")
            return None
            
    except Exception as e:
        logger.error(f"Exception creating deal: {e}")
        return None


def check_deal_exists(advert_id):
    """Check if a deal with this AdvertId already exists"""
    try:
        url = f"{BITRIX24_WEBHOOK_URL}crm.deal.list.json"
        payload = {
            'filter': {
                'UF_CRM_201': str(advert_id)  # Filter by AdvertId field
            },
            'select': ['ID']
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if 'result' in result and len(result['result']) > 0:
            return result['result'][0]['ID']
        return None
        
    except Exception as e:
        logger.error(f"Exception checking deal: {e}")
        return None


# ============================================================================
# IMPORT LOGIC
# ============================================================================

def convert_excel_row_to_bitrix(row):
    """Convert a single Excel row to Bitrix24 deal format"""
    deal_data = {}
    
    # Standard fields
    deal_data['TITLE'] = f"{row.get('propertyType', 'Property')} in {row.get('placeCity', 'Dominican Republic')}"
    deal_data['COMMENTS'] = row.get('text', '')
    deal_data['OPPORTUNITY'] = row.get('priceValue', 0)  # Price also goes to standard field
    deal_data['CURRENCY_ID'] = row.get('currencyId', 'USD')
    
    # Set publication date
    deal_data['UF_CRM_206'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # Map custom fields from Excel
    for excel_col, bitrix_field in EXCEL_TO_BITRIX_MAPPING.items():
        if bitrix_field is None:
            continue
        
        value = row.get(excel_col)
        
        # Skip empty values
        if pd.isna(value) or value == '' or value == 'null':
            continue
        
        # Special handling for specific fields
        if excel_col == 'transactionTypeId':
            # Convert transaction type
            value = TRANSACTION_TYPE_MAP.get(str(value), 'Sale')
        elif excel_col == 'propertyType':
            # Convert property type
            value = PROPERTY_TYPE_MAP.get(str(value), str(value))
        elif excel_col in ['numberOfRooms', 'numberOfBedrooms', 'numberOfBathrooms', 
                          'numberOfToiletrooms', 'numberOfBalconies', 
                          'numberOfParkingLotsInside', 'numberOfParkingLotsOutside',
                          'numberOfTerraces']:
            # Convert to integer
            try:
                value = int(float(value))
            except:
                continue
        elif excel_col in ['areaLiving', 'areaLand']:
            # Convert to integer (m²)
            try:
                value = int(float(value))
            except:
                continue
        elif excel_col == 'priceValue':
            # Convert to float
            try:
                value = float(value)
            except:
                continue
        elif excel_col in ['latitude', 'longitude']:
            # Keep as string with decimal
            value = str(value)
        
        deal_data[bitrix_field] = value
    
    # Set default office information if not present
    if 'UF_CRM_267' not in deal_data:  # OfficeOriginalId
        deal_data['UF_CRM_267'] = 'DR_ESTATE_001'
    
    if 'UF_CRM_268' not in deal_data:  # CorporateName
        deal_data['UF_CRM_268'] = 'Dominican Republic Estate'
    
    if 'UF_CRM_269' not in deal_data:  # Email
        deal_data['UF_CRM_269'] = 'info@drestate.com'
    
    return deal_data


def import_properties_from_excel():
    """Main import function"""
    logger.info("=" * 80)
    logger.info("Starting import from Excel to Bitrix24")
    logger.info("=" * 80)
    
    # Load Excel file
    try:
        df = pd.read_excel(EXCEL_FILE)
        logger.info(f"Loaded {len(df)} properties from Excel")
    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        return
    
    # Statistics
    created = 0
    skipped = 0
    errors = 0
    
    # Process each row
    for index, row in df.iterrows():
        advert_id = row.get('id')
        
        if pd.isna(advert_id):
            logger.warning(f"Row {index + 1}: No ID, skipping")
            skipped += 1
            continue
        
        # Check if already exists
        existing_id = check_deal_exists(advert_id)
        if existing_id:
            logger.info(f"Row {index + 1}: Property {advert_id} already exists (Deal ID: {existing_id}), skipping")
            skipped += 1
            continue
        
        # Convert to Bitrix format
        deal_data = convert_excel_row_to_bitrix(row)
        
        # Create deal
        logger.info(f"Row {index + 1}: Creating property {advert_id}...")
        new_deal_id = create_deal_in_bitrix(deal_data)
        
        if new_deal_id:
            logger.info(f"Row {index + 1}: ✓ Created deal ID: {new_deal_id}")
            created += 1
        else:
            logger.error(f"Row {index + 1}: ✗ Failed to create property {advert_id}")
            errors += 1
        
        # Be nice to the API
        time.sleep(0.5)
    
    # Summary
    logger.info("=" * 80)
    logger.info("Import completed!")
    logger.info(f"Created: {created}")
    logger.info(f"Skipped: {skipped}")
    logger.info(f"Errors: {errors}")
    logger.info("=" * 80)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    if not os.path.exists(EXCEL_FILE):
        logger.error(f"Excel file not found: {EXCEL_FILE}")
        logger.error("Please place the file in the same directory as this script")
        sys.exit(1)
    
    import_properties_from_excel()
