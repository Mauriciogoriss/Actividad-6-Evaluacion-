import pandas as pd
# Funcion 1: Cargamos un archivo con extensión .csv o .xlsx y se convierte en un DataFrame (Si el archivo es de extensión, sale un error)
def carga_de_archivo(df):
    if df.endswith('.csv'):
        return pd.read_csv(df)
    elif df.endswith('.xlsx'):
        return pd.read_excel(df)
    else:
        formato = df.split('.')[-1]
        raise ValueError(f"Este formato no está soportado para esta función: .{formato}")
#Sustituye los valores nulos en promedio mean si es numerico par, 99 si es numerico impar y con "es valor nulo" si es variable no numerica
def sustitucion_valores_nulos(df):

    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:  # Si la columna es numérica
            if df[col].isnull().sum() > 0:  # Si tiene valores nulos
                if df.columns.get_loc(col) % 2 == 0:  # Si  es par
                    df[col].fillna(df[col].mean(), inplace=True)
                else:  # Si es impar
                    df[col].fillna(99, inplace=True)
        else:  # Si la columna no es numérica
            df[col].fillna("Este_es_un_valor_nulo", inplace=True)
    return df
#Identificamos valores nulos en el Dataframe
def identificar_valores_nulos(df):
    
    nulos_por_columna = df.isnull().sum().to_dict()
    nulos_por_DF = df.isnull().sum().sum()
    return {"nulos_por_columna": nulos_por_columna, "total_nulos": nulos_por_DF}
#Sustituimos valores aripicos en el dataframe
def sustitucion_valores_atipicos(df):
    
    for col in df.select_dtypes(include=['int64', 'float64']).columns: #Aseguramos que solo usemos columnas numericas(int64, float64)
        C1 = df[col].quantile(0.25) #Valor que deja el 25% de los datos abajo
        C3 = df[col].quantile(0.75) #Deja el 75€ de los datos por debajo
        IQR = C3 - C1 #Se saca ,a diferencia entre cuartil 3 y 1 para medir dispersion dejando de laod valores atipicos
        limite_inferior = C1 - 1.5 * IQR #todo lo que este por debajo de el limite inferior es valor atipico
        limite_superior = C3 + 1.5 * IQR #todo lo que este por arriba del limite superior tambien sera valor atipico
        median_value = df[col].median() 
        df[col] = df[col].apply(lambda x: median_value if x < limite_inferior or x > limite_superior else x) #usamos lambda para que recorra y aplique la pequeña regla de los limites a cada valor, si son valores atipicos los sustituye por la mediana
    return df
