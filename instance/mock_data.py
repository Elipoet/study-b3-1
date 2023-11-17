import random
import pandas as pd
from faker import Faker
import locale 
import matplotlib.pyplot as plt
import seaborn as sns
import grid 

locale_list = ['fr-FR']
locale_fake = Faker(locale_list)

# fake_id_client = locale_fake.random_int(1, 10000)
# fake_name = locale_fake.name()
# fake_date = locale_fake.date_between('-2y',)
# fake_csp = ' '.join(locale_fake.random_choices(elements =('Agriculteurs exploitants','Artisans. commerçants. chefs entreprise','Cadres et professions intellectuelles supérieures','Professions intermédiaires','Employés','Ouvriers','Retraités','Autres personnes sans activité professionnelle'), length=1))
# fake_cat_ha = ' '.join(locale_fake.random_choices(elements = ('Bébé','Enfant','Adolescent','Adulte'), length=1))

def generate_values1():
    return {
        'DATE_HA' : locale_fake.date_between('-2y',),
        'CLIENT_ID' : locale_fake.random_int(1, 10000),
        'NOM_PRENOM' : locale_fake.name(),
        'CSP' : ' '.join(locale_fake.random_choices(elements =('Agriculteurs exploitants','Artisans. commerçants. chefs entreprise','Cadres et professions intellectuelles supérieures','Professions intermédiaires','Employés','Ouvriers','Retraités','Autres personnes sans activité professionnelle'), length=1)),
        'CATEGORIE_HA' : ' '.join(locale_fake.random_choices(elements=('Bébé','Enfant','Adolescent','Adulte'), length=1)),
        'HA_TOTAL' : locale_fake.random_int(1,100)
    }

ventes = [generate_values1() for _ in range(10000)]

df = pd.DataFrame(ventes)
# df1 = pd.unique(df['CSP'])
# print(type(df1))
# print(df)

# df.plot(kind='bar',x='CSP',y='HA_TOTAL')
# plt.show()

# df.groupby('CSP')['CLIENT_ID'].nunique().plot(kind='bar')
# plt.show()

# df.groupby(['CSP','HA_TOTAL']).size().unstack().plot(kind='bar', stacked=True)
# plt.show()-

df.groupby('CSP')['HA_TOTAL'].sum().plot(kind='bar')
plt.xticks(fontsize=4, rotation=25)
plt.subplots_adjust(bottom=0.2)
plt.title("Dépenses par Panier Moyen en fonction des CSP")    
plt.show()

df.groupby(['CSP','CATEGORIE_HA'])['HA_TOTAL'].sum().unstack().plot(kind="bar", stacked=True)
plt.legend(loc=0,fontsize=10)
plt.xticks(fontsize=4, rotation=25)
plt.subplots_adjust(bottom=0.2)
plt.title("Dépenses par Catégorie de produits en fonction des CSP")
plt.show()

# grid.newpage()
