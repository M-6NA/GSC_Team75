

# SITE_EMOJI = ":tangerine:"
SITE_EMOJI = "assets/orange.png"


COMPONENT_COLORS = {
    "Pack 1L": "#6a4c93",
    "PET": "#1982c4",
    "Orange": "#fb8500",
    "Mango": "#8ac926",
    "Vitamin C": "#ff595e",
    "Açaí": "#c792ea",
    "Bag": "#d6eaf8",
    "Capsule": "#ffc0cb",
    "Capsule (orange)": "#ffc000",
    "Capsule (red)": "#c70039",
}

ROUND_COLORS = {
    -2: "#8ac926",  #8ecae6
    -1: "#06d6a0",  #219ebc
    0: "#8338ec",   #126782
    1: "#fd9e02",   #023047
    2: "#126782",   #ffb703
    3: "#8ecae6",   #fd9e02
    4: "#219ebc",   #8338ec
    5: "#126782",   #06d6a0
    6: "#8ac926"    #8ac926
}

ROUND_VALUES = [-2, -1, 0, 1, 2, 3, 4]
ROUND_TEXT = ['-2', '-1', '0', '1', '2', '3', '4', '5', '6']

PRODUCT_COLORS = {
    "Fressie Orange PET": "#264653",
    "Fressie Orange/C-power PET": "#2a9d8f",
    "Fressie Orange/Mango PET": "#8ab17d",
    "Fressie Orange 1 liter": "#e9c46a",
    "Fressie Orange/Mango 1 liter": "#f4a261",
    "Fressie Orange/Mango+C 1L": "#e76f51",
    "Fressie Orange/Açai PET": "#2ecc71",
    "Frespressie Orange/Açai": "#b2d03f",
    "Frespressie Orange": "#9b30ff"
}

SALES_OBSOLETE_PROD = {
    'rounds': ['-2', '-1', '0', '1', '2', '3'],
    'values': [6.5, 13.7, 13.7, 13.7, 5.6, 2.7],
}

SALES_SERVICE_LEVEL = {
    'rounds': ['-2', '-1', '0', '1', '2', '3'],
    'values': [85.5, 87.1, 87.1, 87.1, 95.7, 87.8],
}

SUPPLY_CHAIN_STOCK_COMPONENTS_WEEKS_DATA = {
    'rounds': ROUND_TEXT,
    'values': [3.6, 4.4, 4.4, 4.4, 4.3, 4.9],
}

SUPPLY_CHAIN_STOCK_PRODUCT_WEEKS_DATA = {
    'rounds': ROUND_TEXT,
    'values': [2.4, 3.3, 3.3, 3.3, 3.1, 1.9],
}
