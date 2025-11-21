"""
Script para entrenar y guardar el modelo de regresión lineal.
Este script extrae el modelo del notebook y lo guarda para empaquetarlo.
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "notebooks" / "Importaciones2024.csv"
MODEL_DIR = BASE_DIR / "modelo_paquete" / "modelo_importaciones" / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def load_and_preprocess_data():
    """Carga y preprocesa los datos del CSV."""
    print("Cargando datos...")
    dfimp24 = pd.read_csv(DATA_PATH, encoding="latin-1", low_memory=False)
    
    # Limpieza y transformación de datos (simplificada del app.py)
    columnas = ['pbk','pnk','naban','canu','vafodo','flete','vacid','vacip','vadua','vrajus','baseiva','totalivayo','seguros','otrosg','porara']
    for c in columnas:
        if c in dfimp24.columns:
            dfimp24[c] = dfimp24[c].astype(str).str.replace('.', '', regex=False)
    for c in columnas:
        if c in dfimp24.columns:
            dfimp24[c] = dfimp24[c].str.strip().replace('', np.nan)
    for c in columnas:
        if c in dfimp24.columns:
            dfimp24[c] = dfimp24[c].astype(str).str.strip().replace(r'^-$', np.nan, regex=True)
    for c in columnas:
        if c in dfimp24.columns:
            dfimp24[c] = dfimp24[c].str.strip().replace(',', '.', regex=True).astype(float)
    
    # Eliminar columnas con suma 0
    df_numeric = dfimp24.select_dtypes(include=[np.number])
    cols_sum0 = [col for col in df_numeric if df_numeric[col].sum() == 0]
    if cols_sum0:
        dfimp24.drop(columns=cols_sum0, inplace=True, errors="ignore")
    
    # Eliminación de columnas según análisis previo
    for c in ['acuerdo','pnk','vafodo','vacip','cuidaimp','depim','deptodes','cuidaexp','bandera','codadad','luin','codluin','paiscom','vadua']:
        if c in dfimp24.columns:
            dfimp24.drop(columns=c, inplace=True, errors="ignore")
    
    # Tratamiento de faltantes
    if 'seguros' in dfimp24.columns:
        dfimp24 = dfimp24.dropna(subset=['seguros'])
    if 'otrosg' in dfimp24.columns:
        dfimp24['otrosg'] = dfimp24['otrosg'].fillna(0.00)
    if 'pbk' in dfimp24.columns:
        dfimp24 = dfimp24.dropna(subset=['pbk'])
    if 'flete' in dfimp24.columns:
        imputer = SimpleImputer(strategy='mean')
        dfimp24[['flete']] = imputer.fit_transform(dfimp24[['flete']])
    
    # Mapeos (simplificados)
    mapeo_clase = {'1': "Mixto", '2': "Privado", '3': "Publico", 'M': "Mixto", 'P': "Privado"}
    mapeo_transporte = {1: "Maritimo", 2: "Ferreo", 3: "Terrestre", 4: "Aereo", 5: "Correo", 7: "Instalaciones fijas", 8: "Aguas interiores", 9: "Otros modos"}
    mapeo_adua = {
        1: "Armenia", 3: "Bogota", 4: "Bucaramanga", 10: "Manizalez", 16: "Pereira",
        19: "Santa Marta", 25: "Riohacha", 27: "San Andres", 34: "Arauca", 35: "Buenaventura",
        36: "Cartago", 37: "Ipiales", 38: "Leticia", 39: "Maicao", 40: "Tumaco", 41: "Uraba",
        42: "Puerto Carreño", 43: "Inirida", 44: "Yopal", 46: "Puerto Asis", 48: "Cartagena",
        49: "Valledupar", 86: "Pamplona", 87: "Barranquilla", 88: "Cali", 89: "Cucuta", 90: "Medellin"
    }
    mapeo_tipo_imp = {
        1: "Reembolsable", 2: "Donación", 3: "Importación temporal", 4: "Importación por reposición",
        5: "Muestra promocional", 6: "Muestra para exhibición", 7: "Muestra experimental",
        8: "Resto de muestras", 9: "Otras no-reembolsables", 99: "Sin información"
    }
    mapeo_regimen = {
        'C1': "Importación ordinaria",
        'C2': "Importación con franquicia",
        'C3': "Reimportación",
        'C4': "Importación temporal para reexportación en el mismo estado",
        'C5': "Importación temporal para perfeccionamiento activo",
        'C6': "Importación para transformación y/o ensamble"
    }
    
    # Mapeo de continentes (simplificado - solo los más comunes)
    mapeo_continente = {
        27: "América", 13: "Asia", 40: "África", 41: "América", 15: "Europa", 17: "Europa",
        37: "Europa", 244: "Asia", 63: "América", 26: "Asia", 690: "Oceanía", 24: "Antártida",
        786: "Antártida", 43: "América", 69: "Oceanía", 72: "Europa", 74: "Asia", 115: "África",
        87: "Europa", 229: "África", 98: "América", 31: "África", 81: "Asia", 111: "Europa",
        80: "Asia", 77: "América", 29: "Europa", 693: "América", 91: "Europa", 88: "América",
        90: "América", 97: "América", 105: "América", 83: "América", 108: "Asia", 119: "Asia",
        102: "Antártida", 101: "África", 640: "África", 149: "América", 165: "Asia", 767: "Europa",
        211: "América", 215: "Asia", 193: "África", 145: "África", 888: "África", 177: "África",
        183: "Oceanía", 169: "América", 173: "África", 127: "África", 196: "América", 199: "América",
        200: "América", 511: "Oceanía", 137: "América", 221: "Asia", 644: "Europa", 23: "Europa",
        783: "África", 235: "América", 232: "Europa", 647: "América", 59: "África", 239: "América",
        240: "África", 243: "África", 685: "África", 245: "Europa", 251: "Europa", 253: "África",
        271: "Europa", 870: "Oceanía", 275: "Europa", 259: "Europa", 494: "Oceanía", 281: "África",
        628: "Europa", 287: "Asia", 327: "Europa", 289: "África", 293: "Europa", 329: "África",
        309: "América", 285: "África", 334: "África", 331: "África", 301: "Europa", 297: "América",
        305: "América", 317: "América", 325: "América", 313: "Oceanía", 337: "América", 351: "Asia",
        343: "Antártida", 345: "América", 198: "Europa", 341: "América", 355: "Europa", 365: "Asia",
        468: "Europa", 361: "Asia", 787: "Asia", 375: "Europa", 372: "Asia", 369: "Asia",
        379: "Europa", 383: "Asia", 386: "Europa", 391: "América", 401: "Europa", 403: "Asia",
        399: "Asia", 406: "Asia", 410: "África", 412: "Asia", 141: "Asia", 411: "Oceanía",
        695: "América", 190: "Asia", 413: "Asia", 420: "Asia", 431: "Asia", 434: "África",
        438: "África", 715: "América", 440: "Europa", 750: "Asia", 426: "África", 443: "Europa",
        445: "Europa", 429: "Europa", 447: "Asia", 698: "América", 474: "África", 498: "Europa",
        496: "Europa", 450: "África", 461: "Asia", 493: "América", 472: "Oceanía", 448: "Europa",
        464: "África", 467: "Europa", 93: "Asia", 500: "Europa", 497: "Asia", 469: "Oceanía",
        505: "África", 488: "África", 501: "América", 477: "América", 485: "África", 458: "África",
        455: "Asia", 489: "África", 507: "África", 542: "Oceanía", 525: "África", 535: "Oceanía",
        528: "África", 521: "América", 531: "Oceanía", 573: "Europa", 538: "Europa", 517: "Asia",
        508: "Oceanía", 548: "Oceanía", 556: "Asia", 576: "Asia", 580: "América", 593: "Oceanía",
        589: "América", 267: "Asia", 578: "Oceanía", 545: "Oceanía", 603: "Europa", 611: "América",
        187: "Asia", 607: "Europa", 586: "América", 579: "Asia", 599: "Oceanía", 618: "Asia",
        660: "África", 670: "Europa", 676: "Europa", 675: "África", 53: "Asia", 759: "África",
        728: "África", 741: "Asia", 710: "África", 772: "Europa", 677: "Oceanía", 735: "África",
        242: "América", 697: "Europa", 748: "África", 700: "América", 729: "Europa", 760: "África",
        720: "África", 770: "América", 246: "Europa", 247: "Europa", 764: "Europa", 773: "África",
        699: "América", 731: "África", 744: "Asia", 823: "América", 203: "África", 800: "África",
        776: "Asia", 774: "Asia", 805: "Oceanía", 825: "Asia", 788: "Asia", 810: "Oceanía",
        815: "América", 820: "África", 827: "Asia", 828: "Oceanía", 218: "Asia", 780: "África",
        833: "África", 830: "Europa", 566: "América", 845: "América", 249: "América", 847: "Asia",
        159: "Europa", 705: "América", 850: "América", 863: "América", 866: "América", 855: "Asia",
        551: "Oceanía", 875: "Oceanía", 687: "Oceanía", 129: "América", 130: "América", 131: "América",
        132: "América", 133: "América", 134: "América", 135: "América", 620: "América", 621: "América",
        622: "América", 623: "América", 624: "América", 625: "América", 626: "América", 631: "América",
        633: "América", 634: "América", 635: "América", 636: "América", 637: "América", 638: "América",
        650: "América", 651: "América", 653: "América", 655: "América", 902: "América", 903: "América",
        904: "América", 905: "América", 907: "América", 911: "América", 913: "América", 914: "América",
        915: "América", 916: "América", 917: "América", 918: "América", 919: "América", 920: "América",
        924: "América", 925: "América", 926: "América", 928: "América", 929: "América", 930: "América",
        931: "América", 933: "América", 934: "América", 935: "América", 936: "América", 937: "América",
        939: "América", 940: "América", 941: "América", 942: "América", 943: "América", 944: "América",
        945: "América", 948: "América", 950: "América", 951: "América", 953: "América", 954: "América",
        955: "América", 956: "América", 957: "América", 958: "América", 959: "América", 960: "América",
        961: "América", 962: "América", 963: "América", 964: "América", 965: "América", 966: "América",
        967: "América", 968: "América", 969: "América", 972: "América", 973: "América", 974: "América",
        976: "América", 977: "América", 979: "América", 980: "América", 981: "América", 982: "América",
        983: "América", 984: "América", 985: "América", 987: "América", 988: "América", 989: "América",
        991: "América", 996: "América", 997: "América", 998: "América", 880: "Asia", 756: "África",
        890: "África", 665: "África", 999: "No declarado"
    }
    
    map_fechas = {2401.0: 1, 2402.0: 2, 2403.0: 3, 2404.0: 4, 2405.0: 5, 2406.0: 6, 
                  2407.0: 7, 2408.0: 8, 2409.0: 9, 2410.0: 10, 2411.0: 11, 2412.0: 12}
    
    map_aduanas_agrupadas = {
        'Cartagena': 'Maritima y Fluvial', 'Buenaventura': 'Maritima y Fluvial',
        'Santa Marta': 'Maritima y Fluvial', 'Barranquilla': 'Maritima y Fluvial',
        'Uraba': 'Maritima y Fluvial', 'Bogota': 'Aereas y Terrestres',
        'Medellin': 'Aereas y Terrestres', 'Cali': 'Aereas y Terrestres',
        'Pereira': 'Aereas y Terrestres', 'Bucaramanga': 'Aereas y Terrestres',
        'Manizales': 'Aereas y Terrestres', 'Armenia': 'Aereas y Terrestres',
        'Yopal': 'Aereas y Terrestres', 'Puerto Asis': 'Aereas y Terrestres',
        'Leticia': 'Aereas y Terrestres', 'Maicao': 'Aereas y Terrestres',
        'Ipiales': 'Aereas y Terrestres', 'Cucuta': 'Aereas y Terrestres',
        'Manizalez': 'Aereas y Terrestres', 'Riohacha': 'Aereas y Terrestres'
    }
    
    # Aplicar mapeos
    if 'fech' in dfimp24.columns:
        dfimp24['fech'] = dfimp24['fech'].map(map_fechas)
    
    if 'copaex' in dfimp24.columns:
        dfimp24 = dfimp24.drop(dfimp24[dfimp24['copaex'] == 216].index)
        dfimp24['copaex'] = dfimp24['copaex'].map(mapeo_continente)
    if 'paisgen' in dfimp24.columns:
        dfimp24['paisgen'] = dfimp24['paisgen'].map(lambda x: mapeo_continente.get(x, x))
        dfimp24 = dfimp24.drop(dfimp24[dfimp24['paisgen'].isin([226, 216, 217, 654])].index)
    if 'paispro' in dfimp24.columns:
        dfimp24 = dfimp24.drop(dfimp24[dfimp24['paispro'].isin([226, 216, 217, 654])].index)
        dfimp24['paispro'] = dfimp24['paispro'].map(lambda x: mapeo_continente.get(x, x))
    
    if 'regimen' in dfimp24.columns:
        dfimp24['regimen'] = dfimp24['regimen'].astype(str).str[:2].map(mapeo_regimen).fillna("Otros")
    
    if 'clase' in dfimp24.columns:
        dfimp24['clase'] = dfimp24['clase'].map(mapeo_clase).fillna("OtrasClases")
    if 'viatrans' in dfimp24.columns:
        dfimp24['viatrans'] = dfimp24['viatrans'].map(mapeo_transporte)
    
    if 'adua' in dfimp24.columns:
        dfimp24 = dfimp24.drop(dfimp24[dfimp24['adua'] == 24].index)
        dfimp24['adua'] = dfimp24['adua'].map(mapeo_adua)
        dfimp24['adua'] = dfimp24['adua'].map(map_aduanas_agrupadas)
    
    if 'tipoim' in dfimp24.columns:
        dfimp24['tipoim'] = dfimp24['tipoim'].map(mapeo_tipo_imp)
    
    # Crear variable trimestre
    if 'fech' in dfimp24.columns:
        dfimp24['trimestre'] = np.select(
            [
                dfimp24['fech'].between(1, 3),
                dfimp24['fech'].between(4, 6),
                dfimp24['fech'].between(7, 9),
                dfimp24['fech'].between(10, 12)
            ],
            [1, 2, 3, 4]
        )
    
    # Eliminar columnas adicionales
    for c in ['naban','coda','actecon','imp1']:
        if c in dfimp24.columns:
            dfimp24.drop(columns=c, inplace=True, errors="ignore")
    
    # Variables auxiliares del mes
    if 'fech' in dfimp24.columns:
        dfimp24['sin_fech'] = np.sin(2 * np.pi * dfimp24['fech'] / 12)
        dfimp24['cos_fech'] = np.cos(2 * np.pi * dfimp24['fech'] / 12)
    
    # Seleccionar solo las columnas necesarias
    needed = ['vacid','fech','sin_fech','cos_fech','adua','paispro','tipoim']
    keep = [c for c in needed if c in dfimp24.columns]
    df = dfimp24[keep].dropna()
    
    return df

def train_and_save_model():
    """Entrena el modelo y lo guarda."""
    print("Preprocesando datos...")
    df = load_and_preprocess_data()
    
    print("Preparando datos para entrenamiento...")
    target = 'vacid'
    features = ['fech','sin_fech','cos_fech','adua','paispro','tipoim']
    
    X = df[features].copy()
    y = df[target].copy()
    
    num_cols = ['fech','sin_fech','cos_fech']
    cat_cols = ['adua','paispro','tipoim']
    
    # Pipeline de preprocesamiento y modelo
    preprocess = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), cat_cols)
        ]
    )
    
    # Crear pipeline completo con modelo de regresión lineal
    pipe = Pipeline(steps=[
        ('prep', preprocess),
        ('reg', LinearRegression())
    ])
    
    # División de datos
    print("Dividiendo datos en entrenamiento y prueba...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenamiento
    print("Entrenando modelo...")
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    
    # Métricas
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nMétricas del modelo:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.4f}")
    
    # Guardar modelo
    print(f"\nGuardando modelo en {MODEL_DIR}...")
    joblib.dump(pipe, MODEL_DIR / "modelo_regresion_lineal.pkl")
    
    # Guardar información de las categorías para validación
    info = {
        'paises': sorted(X['paispro'].dropna().astype(str).unique().tolist()),
        'aduanas': sorted(X['adua'].dropna().astype(str).unique().tolist()),
        'tipos': sorted(X['tipoim'].dropna().astype(str).unique().tolist()),
        'metricas': {
            'MAE': float(mae),
            'RMSE': float(rmse),
            'R2': float(r2)
        }
    }
    joblib.dump(info, MODEL_DIR / "modelo_info.pkl")
    
    print("¡Modelo guardado exitosamente!")
    return pipe, info

if __name__ == "__main__":
    train_and_save_model()

