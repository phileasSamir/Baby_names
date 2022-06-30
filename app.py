###############################################
# Created by iiSeymour
# Changed by Mandeep Singh
# Changed date: 03/21/2019
# Licensce: free to use
#############################################

from flask import Flask, render_template, session, request
import altair as alt
import pandas as pd
import geopandas as gpd
from functools import partial

alt.data_transformers.disable_max_rows()

app = Flask(__name__)

dictsex = {1:"Male",2:"Female"}

##########################
# Flask routes
##########################
# render index.html home page
@app.route("/", methods=["GET","POST"])
def index():
    global name, sex, yearmin, yearmax, displaysex
    name = ""
    sex = [1, 2]
    displaysex = "Either"
    yearmin = df["annais"].min()
    yearmax = df["annais"].max()
    if request.method == "POST":
        yearmin = int(request.form["yearmin"])
        yearmax = int(request.form["yearmax"])
        if request.form["sex"]:
            sex = [int(request.form["sex"])]
        name = request.form["name"].upper()
    if len(sex) == 1:
        displaysex = dictsex[sex[0]]
    return render_template('index.html', name=name, displaysex=displaysex, sex=sex, yearmin=yearmin, yearmax=yearmax)

#########################
### Altair Data Routes
#########################

df = pd.read_csv("data_complet.csv", dtype={"progression":float}, 
                keep_default_na=False, na_values="").fillna(0)

df = df[df["preusuel"]!="_PRENOMS_RARES"]

# Définition de tables et fonctions indépendantes de l'entrée utilisateur

###### podiums et graphe de progression

df_p = df[['annais','sexe','preusuel','freq_an','progression']].drop_duplicates()


def podium_prenom_par_an(df, year, s, top=1):
    """
    top des progression ou regressions 
    s(sexe)= 1 , 2 respectivvement garçon et fille 
    top = 1,0 , respectivement pour progression ou regression
    """
    mask = (df.annais == year) & (df.sexe == s)
    df = df[mask]
    if top==1:
        return df.nlargest(1,["progression"])
    else:
        return df.nsmallest(1,["progression"])

# top des progressions des garçons
table1_top = pd.concat([podium_prenom_par_an(df_p, year , 1 , 1) for year in range(1900, 2021)], axis = 0)
# Top des regressions des garçons
table1_bottom = pd.concat([podium_prenom_par_an(df_p, year , 1 , 0) for year in range(1900, 2021)], axis = 0)
# top des progression des filles
table2_top = pd.concat([podium_prenom_par_an(df_p, year , 2 , 1) for year in range(1900, 2021)], axis = 0)
# Top des regressions des filles
table2_bottom = pd.concat([podium_prenom_par_an(df_p, year , 2 , 0) for year in range(1900, 2021)], axis = 0)
 

#fonction qui retourne top(1)/bottom(0) nb(=3) prenoms par popularité/progression par par plage d'année
def top_n(df, year1=1900, year2=2020, s=1, top=1, nb=3, mode="pop"):
    """
    Fonction qui renvoie les nb prénoms les 
    - plus (top=1) ou moins (top=0) 
    - populaires (mode="pop") ou progressifs (mode="prog")
    - sur la période allant de year1 à year2 inclus
    - pour un sexe s donné (1=M, 2=F)
    
    Par défaut, renvoie le podium des 3 prénoms masculins
    les plus populaires sur l'ensemble de la période disponible.
    """
    df = df[(df["annais"]>=year1) & (df["annais"]<=year2) & (df["sexe"] == s)]
    if mode=="pop":
        df = df[["annais", "freq_an", "preusuel", "sexe"]
               ].drop_duplicates().groupby("preusuel", as_index=False
                                          ).agg({'freq_an':'sum', 'sexe':"first"})
        df["freq_an"] = df["freq_an"]/(year2-year1+1)
        
        if top == 1:
            return df.nlargest(nb,["freq_an"])
        elif top == 0:
            return df.nsmallest(nb,["freq_an"])
    elif mode=="prog":
        df = df[["annais", "progression", "preusuel","sexe"]
               ].drop_duplicates().groupby("preusuel", as_index=False
                                          ).agg({'progression':'sum', 'sexe':"first"})
        df["progression"] = df["progression"]/(year2-year1+1)
        if top == 1:
            return df.nlargest(nb,["progression"])
        elif top == 0:
            return df.nsmallest(nb,["progression"])
        
    
###### Définition des données pour la carte
depts = gpd.read_file('departements-version-simplifiee.geojson')

depts = depts[(depts["code"] != "2A") & (depts["code"] != "2B")]
depts["code"] = depts["code"].astype(int)

@app.route("/data/map")
def data_map():

    global name, yearmin, yearmax, sex, displaysex

    ######### GLOBAL NAMES DIVERSITY ##########*

    dfh = df[['annais', 'sexe', 'nb_distinct_fr_s']].loc[(df.annais >= yearmin) & 
                                                           (df.annais <= yearmax)
                                                          ].drop_duplicates(
            )

    base = alt.Chart(dfh).transform_calculate(
                sexe=alt.expr.if_(alt.datum.sexe == 1, 'Male', 'Female')
            ).properties(height=150, width = 500)

    color_scale = alt.Scale(domain=['Male', 'Female'],
                            range=["steelblue", "salmon"])

    pink_blue = alt.Scale(domain=(1, 2),
                      range=["steelblue", "salmon"])

    left = base.transform_filter(
        alt.datum.sexe == 'Female'
    ).encode(
        x=alt.X('annais:O', axis=None),
        y=alt.Y('nb_distinct_fr_s:Q',
                title='Number of distinct names (female)'),
        color=alt.Color('sexe:N', scale=color_scale, legend=None),
        tooltip=["annais:O"]
    ).mark_bar().properties(title=f'Name diversity between {yearmin} and {yearmax}')

    """middle = base.encode(
        x=alt.X('annais:O', axis=None),
        #text=alt.Text('annais:Q')
    ).mark_text(angle=270).properties(height=5)
    """
    right = base.transform_filter(
        alt.datum.sexe == 'Male'
    ).encode(
        x=alt.X('annais:O', axis=None),
        y=alt.Y('nb_distinct_fr_s:Q', 
                title='Number of distinct names (male)',
                sort=alt.SortOrder('descending')),
        color=alt.Color('sexe:N', scale=color_scale, legend=None),
        tooltip=["annais:O"]
    ).mark_bar()

    pyramid = alt.vconcat(left, 
                        #middle, 
                        right, spacing=5)

    ######### GLOBAL PROGRESSION GRAPH ##########

    ## GARCONS
    garcon_Top = alt.Chart(table1_top.loc[(table1_top.annais >= yearmin) & (table1_top.annais <= yearmax)]
                        ).mark_line(size=0.7, point= alt.OverlayMarkDef(size=8)).encode(
    x =alt.X('annais',title='Year'),
    y =alt.Y('progression:Q', title="Progression"),
    color=alt.Color('sexe:N', scale=pink_blue, legend=None),
    tooltip=['preusuel:N'])

    garcon_Bottom = alt.Chart(table1_bottom.loc[(table1_bottom.annais >= yearmin) & (table1_bottom.annais <= yearmax)]
                            ).mark_line(size=0.7,point= alt.OverlayMarkDef(size=8)).encode(
    x =alt.X('annais',title='Year'),
    y =alt.Y('progression:Q', title="Progression"),
    color=alt.Color('sexe:N', scale=pink_blue, legend=None),
    tooltip=['preusuel:N'])

    ## FILLES
    fille_Top = alt.Chart(table2_top.loc[(table2_top.annais >= yearmin) & (table2_top.annais <= yearmax)]
                        ).mark_line(size=0.7, point= alt.OverlayMarkDef(size=8), color='red').encode(
    x =alt.X('annais',title='Year'),
    y =alt.Y('progression:Q', title="Progression"),
    color=alt.Color('sexe:N', scale=pink_blue, legend=None),
    tooltip=['preusuel:N'])

    fille_Bottom = alt.Chart(table2_bottom.loc[(table2_bottom.annais >= yearmin) & (table2_bottom.annais <= yearmax)]
                            ).mark_line(size=0.7,point = alt.OverlayMarkDef(size=8),  color='red').encode(
    x =alt.X('annais',title='Year'),
    y =alt.Y('progression:Q', title="Progression"),
    color=alt.Color('sexe:N', scale=pink_blue, legend=None),
    tooltip=['preusuel:N'])

    ## Global Vis
    prog_reg_M_F = garcon_Top + garcon_Bottom + fille_Top + fille_Bottom
    prog_reg_M_F = prog_reg_M_F.properties(title=f"First name volatility between {yearmin} and {yearmax}", height=300, width=500)


    ######### PODIUMS ##########

    pink_blue = alt.Scale(domain=(1, 2),
                        range=["steelblue", "salmon"])

    ## Top popular
    map_top_pop_male = alt.Chart(top_n(df_p, yearmin, yearmax, s=1, top=1, mode="pop"), 
                                title = "Most popular names").mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('freq_an:Q', title="Frequency", 
                scale=alt.Scale(domain=(0, 14)), axis=None
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("freq_an:Q",format=".4f")
    ).properties(width=260, height=150)


    map_top_pop_female = alt.Chart(top_n(df_p, yearmin, yearmax, s=2, top=1, mode="pop"),
                                # title = "TOP POPULAR NAME"
                                ).mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('freq_an:Q', title = None, axis = None,
                scale=alt.Scale(domain=(0, 14))
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("freq_an:Q",format=".4f")
    ).properties(width=260, height=150)


    ## Less popular
    map_less_pop_male = alt.Chart(top_n(df_p, yearmin, yearmax, s=1, top=0, mode="pop"),
                                title = "Least popular names").mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('freq_an:Q', title=None, axis=None
                #scale=alt.Scale(domain=(0, 0.00001))
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("freq_an:Q",format=".4f")
    ).properties(width=260, height=150)

    map_less_pop_female = alt.Chart(top_n(df_p, yearmin, yearmax, s=2, top=0, mode="pop"),
                                # title = "LESS POPULAR NAME"
                                ).mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('freq_an:Q', title = None, axis = None,
                #scale=alt.Scale(domain=(0, 0.00001)) 
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("freq_an:Q",format=".4f")
    ).properties(width=260, height=150)

    ## Most progression
    map_top_progression_male = alt.Chart(top_n(df_p, yearmin, yearmax, s=1, top=1, mode="prog"),
                                        title = "Top 3 progressions").mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('progression:Q', axis=None
                #scale=alt.Scale(domain=(-3, 3))
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("progression:Q",format=".4f")
    ).properties(width=260, height=150)


    map_top_progression_female = alt.Chart(top_n(df_p, yearmin, yearmax, s=2, top=1, mode="prog"),
                                        # title = "TOP PROGRESSIVE NAME"
                                        ).mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('progression:Q', title = None, axis = None,
                #scale=alt.Scale(domain=(-3, 3)
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("progression:Q",format=".4f")
    ).properties(width=260, height=150)


    ## Less progression
    map_less_progresion_male = alt.Chart(top_n(df_p, yearmin, yearmax, s=1, top=0, mode="prog"),
                                        title = "Top 3 regressions").mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('progression:Q', title=None, axis=None
                # scale=alt.Scale(domain=(-3, 0.05))
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("progression:Q",format=".4f")
    ).properties(width=260, height=150)


    map_less_progression_female = alt.Chart(top_n(df_p, yearmin, yearmax, s=2, top=0, mode="prog"),
                                        # title = "LESS PROGRESSIVE NAME"
                                        ).mark_bar().encode(
        x=alt.X('preusuel:N', title=None, sort= "-y" ),
        y=alt.Y('progression:Q', title = None, axis = None,
                #scale=alt.Scale(domain=(-0.1, 0.01)),  
            ),
        color=alt.Color('sexe:N', scale=pink_blue, legend=None),
        tooltip=alt.Tooltip("progression:Q",format=".4f"),
    ).properties(width=260, height=150)


    ## Global Vis
    podiums = alt.vconcat(alt.hconcat(map_top_pop_male,
                                    map_top_pop_female,
                                    map_less_pop_male,
                                    map_less_pop_female
                                    ).resolve_scale(y='independent'),
                        ( alt.hconcat(map_top_progression_male,
                                    map_top_progression_female,
                                    map_less_progresion_male,
                                    map_less_progression_female
                                    ).resolve_scale(y='shared')))


    ######### MAP ##########
    if not name or name=="UNIQUE":
        # Carte par défaut
        select_dpt = alt.selection_single(name="dpt", fields=['dpt'], init={"dpt":0})#, bind=input_dropdown)
        
        grouped1 = df[(df["annais"] >= yearmin) & (df["annais"] <= yearmax)][["dpt","nb_distinct_dpt"]].drop_duplicates().groupby(["dpt"], as_index=False).mean()
        grouped1 = depts.merge(grouped1, how='left', left_on='code', right_on='dpt') # Add geometry data back in

        grouped1["unique"] = grouped1["nb_distinct_dpt"].fillna(0).apply(round)

        carte = alt.Chart(grouped1).mark_geoshape(stroke='white').encode(
                        tooltip=['nom', 'unique', 'dpt'],
                        color=alt.Color('unique', scale=alt.Scale(scheme='yellowgreen')),
                    ).properties(width=500, height=500).add_selection(select_dpt)
        
        # Evoulution de la diversité des prénoms sur la période (échelle nationale) (à afficher quand pas de name sélectionné)    
        graphe = alt.Chart(df[["annais","nb_distinct_dpt_s","sexe", 'dpt']].loc[(df.annais >= yearmin) & (df.annais <= yearmax)].drop_duplicates()
                            #, width=400, height=300
                            ).mark_line().encode(
            x=alt.X('annais:Q', scale=alt.Scale(zero=False), title="Year"), #alt.Scale(domainMin=yearmin, domainMax=yearmax)
            y=alt.Y('nb_distinct_dpt_s:Q', 
                    #scale=alt.Scale(domainMin=4000, domainMax=30000), 
                    scale=alt.Scale(zero=False),
                    title="Number of different names"),
            color=alt.Color('sexe:N', legend=None)
        ).properties(title=f"Name diversity between {yearmin} and {yearmax}")
        graphe = graphe.transform_filter(select_dpt).properties(width=400, height=500)

    elif name!="UNIQUE":
        select_dpt = alt.selection_single(fields=['dpt'], init={'dpt':0})#, bind=input_dropdown)
        # Carte après filtrage d'un nom
        grouped2 = df[(df["annais"]>=yearmin) & (df["annais"]<=yearmax) & (df["preusuel"]==name) & (df["sexe"].apply(lambda x: x in sex))].groupby(['dpt', 'preusuel', 'sexe'], as_index=False).sum()
        grouped2 = depts.merge(grouped2, how='left', left_on='code', right_on='dpt') # Add geometry data back in
        grouped2["frequence"] = grouped2["freq_dep_an"]/(yearmax+1-yearmin)
        grouped2["frequence"] = grouped2["frequence"].fillna(0).apply(partial(round, ndigits=4))

        carte = alt.Chart(grouped2).mark_geoshape(stroke='white').encode(
                    tooltip=['nom', 'frequence'],
                    color=alt.Color('frequence', scale=alt.Scale(scheme='yellowgreen')),
                ).properties(width=500, height=500).add_selection(select_dpt
                )# .configure(background = "black")
        
        # Evoulution du prénom choisi sur la période (échelle nationale)
        graphe = alt.Chart(df[["annais","preusuel","sexe","freq_dep_an", "dpt"]].loc[
                                    (df.preusuel == name) & (df.sexe.apply(lambda x: x in sex)) & 
                                    (df.annais >= yearmin) & (df.annais <= yearmax)
                                ].drop_duplicates(),
                        #width=800, height=400
                            ).mark_line().encode(
                        x=alt.X('annais:Q', scale=alt.Scale(zero=False), title="Year"),
                        y=alt.Y('freq_dep_an:Q', title="Frequency"),
                        color = alt.Color('sexe:N', legend=None)
        ).properties(width=400, height=500, title=f"Evolution for {name} ({displaysex}) between {yearmin} and {yearmax}"
        ).transform_filter(select_dpt)

    chart = (pyramid | prog_reg_M_F) & podiums & (carte | graphe)

    return chart.to_json()



if __name__ == "__main__":
    app.run(debug=True)
