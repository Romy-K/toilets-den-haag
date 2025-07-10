# Public Toilets for Seniors in Den Haag

A Jumping-Off Point for Public Toilet Policy in Den Haag

It's a commonly heard complaint: there is a lack of public toilets in Den Haag. 
The aim of this project is to show that while investing in public toilets is obviously worth it in terms of citizens' health and wellbeing, it might be economically viable, too. 
It focuses particularly on seniors, a group that states that a lack of toilets is a reason for them to skip on outings they otherwise would have gone on.

## Data used
- Public Toilets Den Haag 
  https://data.overheid.nl/dataset/openbaretoiletten
- Den Haag demographics
  https://denhaag.incijfers.nl/mosaic/nl-nl/overzichten/bevolking
- Senior toilet survey
  https://anbo-pcob.nl/belangenbehartiging/nationaal-seniorenpanel/onderzoek-openbare-toiletten-nationaal-seniorenpanel/
- Leisure survey
  https://www.nbtc.nl/nl/site/download/download-rapport-nvto-nl?disposition=inline
- Toilet norm
  https://www.iederewctelt.nl/iedere-wc-telt/

## Strategy 
Use data about spending per outing, outings missed, senior population, current toilet density and ideal toilet density to model extra senior spending as a result of adding toilets to the city. 

## Product
A Streamlit app with the following features: 

### 1-Year Simulation: 
- use a slider to model the economic consequences of adding a certain number of toilets to the city in 1 year
- see current toilets on the map of Den Haag and generate hypothetical toilets to be added
- see illustration of sigmoid function used to model behavorial outcomes
- 
### 10-Year simulation:
- use a slider to model the economic consequences of adding a certain number of toilets to the city each year for 10 years (2025 - 2034)
- view and download detailed table with year-by-year outcomes for your chosen scenario

### Some facts, figures and recommendations
- preliminary facts used for the simulations
- recommendations for the city

## Technologies Used
- Python 3.9+
- Streamlit (for the web application)
- Pandas (for data manipulation)
- NumPy (for numerical operations, especially sigmoid function)
- Plotly Express (for interactive visualizations)
- MySQL Workbench (for database)

## Contact
romykoreman@live.nl 
https://www.linkedin.com/in/romy-koreman/

### NB
This project was my final project for the Ironhack Data Analytics bootcamp. 
