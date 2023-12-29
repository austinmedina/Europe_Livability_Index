from flask import Flask, request, render_template, url_for, flash, redirect, session
import pandas as pd
import requests
from Weather.computeWeatherscore import runLivabilityIndex

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boop'

userChoices = []

@app.route("/", methods = ["GET", "POST"])
def home():
   return render_template("LivabilityHome.html")

@app.route("/calculate", methods = ["GET", "POST"])
def livabilityIndex():
   if request.method == "POST":
      spring_temp = request.form.get("springTemp") 
      summer_temp = request.form.get("summerTemp") 
      fall_temp = request.form.get("fallTemp") 
      winter_temp = request.form.get("winterTemp") 

      spring_snow = request.form.get("springSnow") 
      summer_snow = request.form.get("summerSnow") 
      fall_snow = request.form.get("fallSnow") 
      winter_snow = request.form.get("winterSnow") 

      spring_rain = request.form.get("springRain") 
      summer_rain = request.form.get("summerRain") 
      fall_rain = request.form.get("fallRain") 
      winter_rain = request.form.get("winterRain") 

      unit_temp = request.form.get("unitTemp")
      unit_snow = request.form.get("unitSnow")
      unit_rain = request.form.get("unitRain")

      if not all([spring_temp, summer_temp, fall_temp, winter_temp]):
            flash('Temperatures are required!')
      elif not all([spring_snow, summer_snow, fall_snow, winter_snow]):
            flash('Snowfall amounts are required!')
      elif not all([spring_rain, summer_rain, fall_rain, winter_rain]):
            flash('Rainfall amounts are required!')
      else:
         session['userChoices'] = [[spring_temp, summer_temp, fall_temp, winter_temp], 
                                   [spring_snow, summer_snow, fall_snow, winter_snow], 
                                   [spring_rain, summer_rain, fall_rain, winter_rain], 
                                   [unit_temp, unit_snow, unit_rain]]
         return redirect(url_for('getLocationElements'))
   
   return render_template("LivabilityCalculator.html")

@app.route("/showResults", methods = ["GET", "POST"])
def showResults():
   top10 = session['top10']
   locationURLS = session['locationURLS']
   return render_template('LivabilityResults.html', top10=top10, locationURLS=locationURLS)

@app.route("/showResults/getLocationElements", methods = ["GET", "POST"])
def getLocationElements():

   userChoices = session['userChoices']
   top10=runLivabilityIndex(userChoices)
   session['top10'] = top10

   locations = []
   for index, row in top10.iterrows():
      temp = []
      temp.append(row[0].replace(' ', '%20'))
      temp.append(row[1].replace(' ', '%20'))
      locations.append(temp)
   
   print("LOOKS HERE FOR THE LOCATIONS AHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
   print(locations)
   url = "https://api.unsplash.com/search/photos"
   locationURLS = []

   for loc in locations: 
      query = loc[0] + "%20" + loc[1] + "%20nature"
      print("GOT HERE!!!!!!!!!!!!!!!!!!!!!!")
      print(query)
      params = {'query': query, 'client_id':'EGNZwSaZsNgcA6Ffy-93TRcHkZNHH0lNaGXSE2miloM', 'per_page':'1', 'order_by':'relevent'}
      unsplash = requests.get(url, params=params, allow_redirects=True)

      if (unsplash.status_code == 200):
         us = unsplash.json()
         locationURLS.append(us['results'][0]['urls']['raw'])
   
   session['locationURLS'] = locationURLS
   return redirect(url_for('showResults'))

@app.route("/about", methods = ["GET", "POST"])
def about():
   return render_template('About.html')