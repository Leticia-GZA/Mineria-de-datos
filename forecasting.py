# -*- coding: utf-8 -*-
"""forecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HhefBSG_10Yn4cW2aBJ7Zhs4Kc_WH6PX
"""

#librerias
from sklearn import datasets
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

#datos
dataset = pd.DataFrame(pd.read_csv("/content/base.csv"))
dataset.head()

plot = dataset['PrecioDeCierreAjustado'].plot(figsize=(10, 8))

# Aplicando el filtro Hodrick-Prescott para separar en tendencia y 
# componente ciclico.
dataset_ciclo, dataset_tend = sm.tsa.filters.hpfilter(dataset['PrecioDeCierreAjustado'])
dataset['tend'] = dataset_tend

# graficando la variacion del precio real con la tendencia.
dataset[['PrecioDeCierreAjustado', 'tend']].plot(figsize=(10, 8), fontsize=12);
legend = plt.legend()
legend.prop.set_size(14);

# graficando rendimiento diario
plot = dataset['var_diaria'].plot(figsize=(10, 8))