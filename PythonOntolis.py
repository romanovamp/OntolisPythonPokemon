
#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import random as r
import sys
from onto.onto import Onto

def findColumn(ontoData, onto, columnName):
    ontoColumns = onto.get_nodes_linked_from(ontoData, "has")
    for ontoColumn in ontoColumns:
        if ontoColumn["name"] == columnName:
            return ontoColumn
    return None

def checkNode(node):
    if (node == None): 
        print ('Онтология задана некорректно')
        sys.exit(0)


onto = Onto.load_from_file("onto.ont")

ds = onto.first(onto.get_nodes_by_name("Data Source"))
checkNode(ds)
csvDS = onto.first(onto.get_nodes_linked_to(ds, "is_a"))
checkNode(csvDS)
myData = onto.first(onto.get_nodes_linked_to(csvDS, "instance_of"))
checkNode(myData)

df = pd.read_csv(myData["attributes"]["path"], delimiter=";")
indx = 0
plt.figure(figsize=(16,8))
plt.suptitle("types pokemons")

# заранее найдем все цвета, чтобы далее исключать использованные
nodeColor = onto.first(onto.get_nodes_by_name("color"))
checkNode(nodeColor)
colorTypes = onto.get_nodes_linked_to(nodeColor,"is_a")
checkNode(colorTypes)


for column in df.columns: 
    ontoColumn = findColumn(myData, onto, column) #находим столбцы, наименование которых есть в онтологии (Type1, Type2)
    if ontoColumn:
        indx = indx + 1
        ontoCharts = onto.get_nodes_linked_from(ontoColumn, "use_for")
        checkNode(ontoCharts)
        for ontoChart in ontoCharts:
            # один тип графика
            chartType = onto.first(onto.get_nodes_linked_from(ontoChart,"instance_of")) 
            visCodeChartType = chartType["attributes"]["exec"]

            # выбор цвета, исключение его из списка
            colorType=colorTypes[r.randint(0, len(colorTypes)-1)]
            colorTypes.remove(colorType)

            # отрисовка графика
            plt.subplot(1, 2, indx)
            exec("df[column].value_counts().plot." + visCodeChartType + "(color = '" + colorType["name"] +"')");
            plt.xlabel(ontoColumn["name"])

plt.show()
