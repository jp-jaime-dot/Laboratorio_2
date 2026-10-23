from pathlib import Path

"""  
Codigo de lectura 
"""

def leer_posiciones(ruta: Path):
    """Leer caida_libre_sintetica.CSV con columnas tiempo_s, altura_m, icertidumbre_m"""
    filas = []

    with ruta.open(encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip()
        print(encabezado)
        
        if encabezado != "tiempo_s,altura_m,incertidumbre_m":
            raise ValueError("Encabezado Inesperado")
         
        
        for numero, linea in enumerate(archivo, start=2):
            if linea.strip() == "": 
                continue
            campos = linea.strip().split(",")
            
            if len(campos) != 3:
                raise ValueError(f"Linea {numero}: se esperaban tres columnas")
            try:
                tiempo = float(campos[0])
                altura = float(campos[1]) 
                incertidumbre = float(campos[2]) 
            except ValueError as error:
                raise ValueError(f"Fila número {numero}: valor no numérico")
        
            filas.append([tiempo, altura, incertidumbre]) 
    
    if not filas:
        raise ValueError("El archivo no contiene mediciones") 
        
    return filas

"""   
Codigo de validación 
"""

def validar_filas(filas, h0=10.0): 
    tiempo_anterior = None
    for numero, fila in enumerate(filas, start=2): 
         tiempo, altura, incertidumbre = fila  
         
         if altura < 0 or altura > h0: 
             raise ValueError(f"Fila {numero}: la altura debe estar entre 0 y {h0}") 
         
         if incertidumbre <= 0: 
             raise ValueError(f"Fila {numero}: la incertidumbre debe ser positiva")   
         
         if tiempo_anterior is not None and tiempo <= tiempo_anterior: 
             raise ValueError(f"Fila {numero}: solo tiempos crecientes")
         
         tiempo_anterior=tiempo


""" 
Codigo para calcular la gravedad en cada fila
"""

def calcular_g(filas, h0=10.0): 
    """ Calcula g=2(h0-h)/t**2 para las filas con tiempos positivos""" 
    estimaciones = [] 
    for tiempo, altura, incertidumbre in filas: 
        if tiempo > 0: 
            g= 2*(h0 - altura)/tiempo**2 
            estimaciones.append([tiempo, altura, g])
    
    return estimaciones 

"""  
Media, desviación, mínimo, máximo y rango 
"""

def resumir(estimaciones): 
    valores_g =[] 
    for tiempo, altura, g in estimaciones: 
        valores_g.append(g) 
    n = len(valores_g) 
    suma = 0.0
    for g in valores_g: 
        suma += g 
    media = suma / n 

    acumulado = 0.0 
    for g in valores_g: 
        acumulado += (g -media)**2 
    desviacion = (acumulado / n)**0.5 

    minimo = min(valores_g) 
    maximo = max(valores_g) 
    return media, desviacion, minimo, maximo 





if __name__=='__main__':
    base = Path(__file__).resolve().parent
    ubicacion = base / "caida_libre_sintetica.csv"
    datos = leer_posiciones(ubicacion) 
    validar_filas(datos)
    print("Archivo:", datos) 
    print("Datos validos:", len(datos), "filas") 
    estimaciones = calcular_g(datos) 
    print("Estimaciones de g:", len(estimaciones)) 
    print("t (s) h (m) g (m/s^2)") 
    for tiempo, altura, g in estimaciones: 
        print(f"{tiempo:.1f}  {altura:.2f}  {g:.2f}") 
    media, desviacion, minimo, maximo = resumir(estimaciones)
    print(f"Media de g: {media:.3f} m/s^2")
    print(f"Desviación: {desviacion:.3f} m/s^2")
    print(f"Mínimo: {minimo:.2f} m/s^2")
    print(f"Máximo: {maximo:.2f} m/s^2")
    print(f"Rango: {maximo - minimo:.2f} m/s^2")  
    """ Comparacion de valores obtenidos con g=9.81""" 
    g_ref = 9.81 
    dif_abs = abs(media -g_ref) 
    dif_rel = dif_abs / g_ref 
    print(f"Diferencia absoluta: {dif_abs:.3f} m/s^2") 
    print(f"Diferencia relativa: {dif_rel*100:.2f} %") 
    