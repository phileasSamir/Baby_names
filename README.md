# Exploring french baby names
## *Onomastics visualizations*
*Mohamed FRIKHA, Zoubir LANSEUR, Philéas SAMIR, Gwladys SANCHEZ, Pooran SHAHDI*

### Introduction
We explored french baby names between 1900 and 2020.  
We were asked to produce three visualizations :
- Visualization 1: How do baby names evolve over time? Are there names that have consistently remained popular or unpopular? Are there some that have were suddenly or briefly popular or unpopular? Are there trends in time?
- Visualization 2: Is there a regional effect in the data? Are some names more popular in some regions? Are popular names generally popular across the whole country?
- Visualization 3 (bonus): Are there gender effects in the data? Does popularity of names given to both sexes evolve consistently? (Note: this data set treats sex as binary; this is a simplification that carries into this assignment but does not generally hold.)

### Plots
In order to meet these requirements, we let the user supply a name, a gender and a time range and produce multiple plots regarding the inputs. We provide :
1. A plot of the number of distinct names by gender over the given time range,
2. A plot of the volatility of names by gender over the given time range, i.e. the biggest progression in % and the biggest regression in % by year,
3. Plots of the most and least popular names by gender over the given time range, 
4. Plots of the biggest progressions and regressions by gender over the given time range.  
**If no name was provided :**
5. A map of name diversity by department over the given time range,
6. When selecting a department from the map, a plot of name diversities by gender over the given time range in the selected department (before selecting a department, the national diversity is displayed).  
**If a name is provided :** 
7. A map of the frequency of that name by department over the given time range,
8. A plot of the frequency of that name in the department over the given time range (before selecting a department, the national frequency is displayed).  

Please note that default selections work in the Altair notebook, but do not work in the app, hence you might see some weird curves for plots 6 and 8 until a selection is made.

### Choices made
There can be several ways to express **popularity** and **progression**. We thought that the absolute count of a given name is not a reliable value, as it does not take into account the evolution of natality for instance. We rather calculated frequencies, at different scales (dep. or national), which is the ratio of the name count divided by all the births of the same sex for a given year.  
The most/least popular name is the name that has the highest average national frequency over the considered time range.  
The progressions are calculated as a difference of the national frequency from one year to another. So a "+1" progression could mean "from 10% frequency to 11% frequency", and also "from 20% to 21%". We could have made a relative progression, but we did not like the fact that a 1-to-2%-evolution would be a +100% progression, and a 10-to-15%-one would "only" be +50%, even though it is more impressive at a global scale.  
We excluded the "_PRENOM_RARES" rows as well as rows with missing department or year values.

### Answering the questions
##### Some notes on user interaction
We wanted our visualization to be able to answer all questions at once, without navigating from one dashboard to another. Schematically, there were 3 main axis to take into account in our plots: gender, location and time.
In order to encode gender, we differentiated over gender in most visualizations. The user can also select a gender in a drop-down menu.
In order to encode time, we let the user select a time range to inspect. This can be the entire range (1900-2020) or a chosen year.
In order to encode location, we provide maps. The user can select a given department on the map to filter the data in some plots.
Since the user could want to study a single name, we also let them select a name of their choice.
We think interactivity is the best way to make a visualization adaptable to many questions, and this is why we made these design choices.

##### Explanations
- *How do baby names evolve over time? Are there names that have consistently remained popular or unpopular? Are there some that were suddenly or briefly popular or unpopular? Are there trends in time?* : We provide the most popular names and unpopular names over any given time range in the form of bar plots, with bar height encoding frequency (**plot 3**). We provide the frequency over time for any name provided by the user in the form of a line plot over the user-selected time range (**plot 8**). It should be noted that due to privacy reasons, "unpopular names" are the most unpopular excluding names with frequencies that are too low (that are grouped under "_PRENOMS_RARES" or anonymized with "XX" department value, more info on the Insee website). We can find both "fads" and long-term trends thanks to our bar **plots (3 and 4)** and our **line-plot (8)**.
- *Is there a regional effect in the data? Are some names more popular in some regions? Are popular names generally popular across the whole country?* : **Map 5** shows name diversity by department (color encodes diversity). **Line-plot 6** reacts to a selection on **map 5** to show diversity over time in the chosen department. **Map 7** shows the popularity of a name by department (color encodes frequency). **Line-plot 8** reacts to a selection on **map 7** to show the frequency of the given name in the selected department over time. 
If no selection is made on the map, **line-plot 6** and **line-plot 8** show national diversity and name frequency, respectively.
- *Are there gender effects in the data? Does popularity of names given to both sexes evolve consistently?* : As we mentioned, most plots differentiate over sex. We provide two line-plots that show the biggest changes in frequency over the provided time range (we see that female names tend to be more diverse over the entire time range, but volatility seems to be comparable for both sexes).
We provide additional remarks and trivia in the web application.

### How to make it work :
You can find the necessary data here: https://perso.telecom-paristech.fr/eagan/new/class/igr204/data/dpt2020.csv
and here: https://github.com/gregoiredavid/france-geojson/blob/master/departements-version-simplifiee.geojson

1. Run the `data_cleaning` notebook.
2. Run the `Altair` notebook.
3. We created a webapp thanks to this repo : https://github.com/lemoncyb/flasked-altair.git. It provides better interactivity. You can run it with `python app.py`, and open it in your browser.
4. You can find the initial sketches in the `sketches` directory.
5. You can find .png files of the dashboards in the `figs` directory.
