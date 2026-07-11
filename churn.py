import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Verbindung zur SQLite-Datei
con = sqlite3.connect(r"C:\Users\irina\Downloads\churn.db")

# churn-Quote pro Land aus der Db holen
df_land = pd.read_sql_query("""
    SELECT Geography,
           ROUND(AVG(Exited)*100, 1) AS Quote_Prozent
    FROM Churn_Modelling
    GROUP BY Geography
""", con)

print(df_land)   # zeigt die Tabelle im Terminal

# Erste Grafik: Balkendiagramm der Churn-Quote pro Land
plt.bar(df_land["Geography"], df_land["Quote_Prozent"], color="steelblue")
plt.title("Churn-Quote pro Land")
plt.ylabel("Churn in %")
plt.savefig("churn_pro_land.png", dpi=150,
            bbox_inches="tight")  # speichert als Bild
plt.show()   # zeigt das Diagramm in einem Fenster

# Chart 2: Churn nach Anzahl Produkte

df_produkte = pd.read_sql_query("""
    SELECT NumOfProducts,
           ROUND(AVG(Exited)*100, 1) AS Quote_Prozent
    FROM Churn_Modelling
    GROUP BY NumOfProducts
    ORDER BY NumOfProducts
""", con)

print(df_produkte)

plt.figure()                     # neue Grafik
plt.bar(df_produkte["NumOfProducts"],
        df_produkte["Quote_Prozent"], color="indianred")
plt.title("Churn nach Anzahl Produkte")
plt.ylabel("Churn in %")
plt.xlabel("Anzahl Produkte")
plt.savefig("churn_pro_produkt.png", dpi=150, bbox_inches="tight")
plt.show()

df_age = pd.read_sql_query("""
   SELECT CASE WHEN Age < 40 THEN 'unter 40' ELSE '40 und älter' END AS Altersgruppe,
       COUNT(*)                    AS Kunden,
       SUM(Exited)                 AS Gekuendigt,
       ROUND(AVG(Exited)*100, 1)   AS Quote_Prozent
FROM Churn_Modelling
GROUP BY Altersgruppe
""", con)

print(df_age)

plt.figure()                     # neue Grafik
plt.bar(df_age["Altersgruppe"], df_age["Quote_Prozent"], color="lightcoral")
plt.title("Churn nach Altersgruppe")
plt.ylabel("Churn in %")
plt.xlabel("Altersgruppe")
plt.savefig("churn_pro_alter.png", dpi=150, bbox_inches="tight")
plt.show()
