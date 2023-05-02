import pandas as pd
import seaborn as srn
import statistics as est

# importing data of the company to check the churn
dataset = pd.read_csv("churn.csv", sep=";")

dataset.head()

# As we are going to name the columns (first problem identified), we need to know the exact number of columns.
dataset.shape

# We have 12 columns. So we will need 12 names.
dataset.columns = ["Id", "Score", "Estado", "Gênero", "Idade", "Patrimônio", "Saldo", "Produtos", "TemCartCred", 
                   "Ativo", "Salário", "Saiu"]

dataset.head()

# Let's analyze a specific error. Take the states column and check if everything is ok.
# Remembering that this bank only serves people from the southern region of the country; any deviation from this is error.
agrupado = dataset.groupby(["Estado"]).size()
agrupado

# We noticed that there are users registered as SP (not part of the South);
# There are users from two non-existent states: RP and TD
# When changing, you must use the "mode", because that way, everything goes to the one with the greatest amount.

# In this case, we will see the information in graphic form:
agrupado.plot.bar(color = "gray")
agrupado

# Checking for possible errors in the "Gender" column
agrupgenero = dataset.groupby(["Gênero"]).size()
agrupgenero
# We noticed that there are numerous entries with different writings for the same keys.

# Checking in chart
agrupgenero.plot.bar(color = "red")
agrupgenero

# In this case, you cannot use the moda, because, if it is for the majority, there will be women registered as men.
# You have to take the F and Fem values directly for the Female, and the M values for the Male.

dataset.columns = ["Id", "Score", "Estado", "Gênero", "Idade", "Patrimônio", "Saldo", "Produtos", "TemCartCred", 
                   "Ativo", "Salário", "Saiu"]

# How to explore a numeric column
# describe() shows the mean, median, range, maximum number.
dataset["Score"].describe()

# snr is the abbreviation for Seaborn
# asked for a boxplot (which is this type of graph) from the "dataset" worksheet with data from the "Score" column
# Name the image with the set_title command
# WARNING: from now on, for the boxplot, you will need to use x=dataset["columnname"] and no longer dataset["columnname"]
srn.boxplot(x=dataset["Score"]).set_title("Tabela Score")

# You should no longer use distplot, but histplot or displot (without the t)
srn.histplot(dataset["Score"]).set_title("Score")

# It can be noticed that there is a minimum value of -20 (impossible to have age -20), that is, there is an error to be corrected;
# The maximum value is 140 (impossible to have a customer in the bank aged 140), that is, there is an error to be corrected.
dataset["Idade"].describe()

# In the graph, we identified two entries below zero and one above 100 (there are the errors).
srn.boxplot(x=dataset["Idade"]).set_title("Idade")

srn.displot(dataset["Idade"])

dataset["Salário"].describe()

# How to check for null data (those that have not been filled) - this is a serious error in the system
# There are 8 nulls in Gender and 7 in Salary
dataset.isnull().sum()

# Let's start processing the data.
dataset["Salário"].describe()

# I need to know the median value because I'm going to treat the data by replacing nulls with the median.
mediana = est.median(dataset["Salário"])
mediana

dataset["Salário"].fillna(mediana, inplace=True)

# We verify that, now, there are no more null data in Salary.
dataset.isnull().sum()

# Let's solve the Gender problems:
# 1. There is a lack of standardization. Let's check:
agrupamento = dataset.groupby(["Gênero"]).size()
agrupamento

#2.The other error is null data.
# Let's start with this one. Null data must always be filled in by the majority.
# Most entries are in male; so let's use the mode. We will include all in Male
dataset["Gênero"].fillna("Masculino", inplace = True)
dataset["Gênero"].isnull().sum()

# nulls fixed.

# Now, let's fix the lack of standardization of the entered data
# All must be Female or Male (not F, Female, M, Male)
dataset.loc[dataset["Gênero"] == "M", "Gênero"] = "Masculino"
dataset.loc[dataset["Gênero"].isin(["F", "Fem"]), "Gênero"] = "Feminino" # the isin command means "is in" (is in).
# ".isin()" is used for sets.
# Now, let's visualize the result
agrupamento = dataset.groupby(["Gênero"]).size()
agrupamento

# In the age column, there are the following errors: people aged below zero and much above 100
# Let's check how many people are above this issue
dataset.loc[(dataset["Idade"] < 0) | (dataset["Idade"] > 120)]
"""We noticed that we have one person in the Female with the age below zero and two in the Male with error
(one with age below zero and another with age above one hundred)"""

# Check the median to be able to replace these ages
mediana = est.median(dataset["Idade"])
mediana

dataset.loc[(dataset["Idade"] < 0) | (dataset["Idade"] > 120), "Idade"] = mediana

dataset["Idade"].describe()
# problem fixed

# We can also go through the path of the table and see that there is no more data.
dataset.loc[(dataset["Idade"] < 0) | (dataset["Idade"] > 120)]

# In the chart, we can see the fixed data as well.
srn.boxplot(x=dataset["Idade"]).set_title("Idade")

# Let's check for duplicate data:
dataset[dataset.duplicated(["Id"], keep=False)]

# Let's handle the repetitions:
dataset.drop_duplicates(subset="Id", keep="first", inplace=True)
# Let's check
dataset[dataset.duplicated(["Id"], keep=False)]
# He kept (keep) the first ones of each and deleted (drop) the duplicates.
# Notice, in the table below, that there are no more duplicate Ids.

