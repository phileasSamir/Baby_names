# Exploring french baby names
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

 If no name was provided :  
5. A map of name diversity by department over the given time range,
6. When selecting a department from the map, a plot of name diversities by gender over the given time range.  

 If a name was provided :  
7. A map of the frequency of that name by department over the given time range,
8. A plot of the national frequency of that name over the given time range.

### Choices made
There can be several ways to express popularity and progression. We thought that the absolute count of a given name is not a reliable value, as it does not take into account the evolution of natality for instance. We rather calculated frequencies, at different scales (dep. or national), which is the ratio of the name count divided by all the births of the same sex for a given year.  
The most/least popular name is the name that has the highest average national frequency over the considered time range.  
The progressions are calculated as a difference of the national frequency from one year to another. So a "+1" progression could mean "from 10% frequency to 11% frequency", and also "from 20% to 21%". We could have made a relative progression, but we did not like the fact that a 1-to-2%-evolution would be a +100% progression, and a 10-to-15%-one would "only" be +50%, even though it is more impressive at a global scale.

### Answering the questions
- *How do baby names evolve over time?* : all plots participate in the answer.
- *Are there names that have consistently remained popular or unpopular?* : we provide the most popular names and unpopular names over any given time range (plot 3), and we provide the frequency over time for any given name (plot 8).
- *Are there some that were suddenly or briefly popular or unpopular? Are there trends in time?* : we can find both "fads" and long-term trends thanks to plots 3, 4 and 8.
- *Is there a regional effect in the data?* : map 5 shows diversity by department.
- *Are some names more popular in some regions? Are popular names generally popular across the whole country?* : map 7 shows the popularity of a name by department.
- *Are there gender effects in the data?* : plots 1, 2, 3, 4, 6 differentiate over sex.
- *Does popularity of names given to both sexes evolve consistently?* : plots 1 and 2 answer that question (we see that female names tend to be more diverse over the entire time range, but volatility seems to be comparable for both sexes).
We provide additional remarks in the web application.

### How to make it work :
1. Run the `data_cleaning` notebook.
2. Run the `Altair` notebook.
3. We created a webapp thanks to this repo : https://github.com/lemoncyb/flasked-altair.git. It provides better interactivity. You can run it with `python app.py`, and open it in your browser.
4. You can find the initial sketches in the `sketches` directory.
