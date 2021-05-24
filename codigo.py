# -*- coding: utf-8 -*-
"""Codigo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15Rn8I8tMr9FVYtGMEyDeRjtudCZXXF6Q

# Importación de Librerias
"""

from math import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import pairwise_distances_argmin
from collections import Counter, defaultdict

"""# Importación de Datos

"""

dataset = pd.DataFrame(pd.read_csv("/housing.csv"))
dataset.head()
#Dataset.head() por default muestra 5 datos, se puede agregar un número dentro de los paréntesis para mostrar más datos

"""# Estadistíca Descriptiva de los datos 
Media, Desviación, mínimos, máximos, etc
"""

print(dataset.shape)
dataset.describe()
#La herramienta Describir dataset proporciona una vista general de sus big data. 
#De forma predeterminada, la herramienta genera una capa de tabla que contiene resúmenes de sus valores de campos
# así como una vista general de los ajustes de geometría y tiempo de la capa de entrada.

"""# Porcentaje de Datos Faltantes
Aquí podemos ver que faltan datos en total de dormitorios
"""

print(dataset.isnull().sum()*100/dataset.shape[0])
print(dataset.shape)

dataset=dataset.dropna()
print(dataset.isnull().sum()*100/dataset.shape[0])
print(dataset.shape)
#La función dropna () de Pandas DataFrame se utiliza para eliminar filas y columnas con valores Null / NaN.
#De forma predeterminada, esta función devuelve un nuevo DataFrame y el DataFrame de origen permanece sin cambios.

"""# Diagramas de caja de las variables """

for i in range(2,9):
  plt.title(dataset.columns[i])
  plt.boxplot(dataset.iloc[:,i])
  plt.show()

"""#Algoritmo de regresión lineal

###Relación que hay entre la cantidad de habitaciones y dormitorios, población, valor medio de la casa, edad promedio de la vivienda
"""

sns.pairplot(dataset, x_vars=['total_rooms','population','median_house_value','housing_median_age'], y_vars='total_bedrooms', height=5, aspect=1, kind='scatter')
plt.show()

"""###Matriz de correlaciones
 Aquí podemos ver que las variables que más se correlacionan con la predicción de los dormitorios es la variable de poblacion en esta área de California.
 
"""

mask = np.triu(np.ones_like(dataset[['total_rooms','population','median_house_value','housing_median_age','total_bedrooms']].corr(), dtype = bool))
sns.heatmap(dataset[['total_rooms','population','median_house_value','housing_median_age','total_bedrooms']].corr(),cmap="GnBu",mask=mask, annot = True,fmt='.2g',linewidths = 1)
plt.show()

"""###Entrenamiento del modelo """

X = dataset['population']
y = dataset['total_bedrooms']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.7, test_size = 0.3, random_state = 100)
#70% entrenamiento y 30% prueba

import statsmodels.api as sm

# Agrega una constante para obtener una intersección
X_train_sm = sm.add_constant(X_train)

# Ajusta la línea de resistencia usando 'OLS'
lr = sm.OLS(y_train, X_train_sm).fit()

# Imprime los parámetros, es decir, la intersección y la pendiente de la línea de regresión ajustada
lr.params

"""###Efectividad del modelo
Se presenta la $R^2$ del modelo 
"""

y_train_pred = lr.predict(X_train_sm) #Realizamos la predicción utilizando los datos de prueba.
res = (y_train - y_train_pred)
X_test_sm = sm.add_constant(X_test)
y_pred = lr.predict(X_test_sm)
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
np.sqrt(mean_squared_error(y_test, y_pred))

r_squared = r2_score(y_test, y_pred)
r_squared

"""#Algoritmo k-mean

###Lectura de datos
"""

x=dataset['median_income'] #Ingresos medios
y=dataset['median_house_value'] #Valor medio de la casa 
x_label = ""
y_label = ""
X = np.vstack((x, y)).T

"""###Gráfica de dispersión de datos """

plt.title('Diagrama de disperción de Ingreso medio de la familia vs Costo medio del hogar')
plt.xlabel('Ingreso medio de la familia')
plt.ylabel('Costo medio del hogar')
plt.scatter(x, y, color='#76c2b4')
plt.show()

"""###Función para clasificar
Se define la función find_clusters para poder encontrar los centroides
"""

def find_clusters(X, n_clusters, rseed=2):
    
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]
    while True:
        labels = pairwise_distances_argmin(X, centers)
        new_centers = np.array([X[labels == i].mean(0) for i in
        range(n_clusters)])
        if np.all(centers == new_centers):
            break
        centers = new_centers
    return centers, labels

#número de centroides que queremos 
clust_num = 5

"""###Gráfica de dispersión de los datos agrupados """

centers, labels = find_clusters(X, clust_num)
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
plt.title('Diagrama de dispeción de Ingreso medio de la familia vs Costo medio del hogar')
plt.xlabel('Ingreso medio de la familia')
plt.ylabel('Costo medio del hogar')
plt.show()

print("\nNumero de zonas por cluster:")
print(Counter(labels))

clusters_indices = defaultdict(list)
for index, c in enumerate(labels):
    clusters_indices[c].append(index)