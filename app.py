from flask import Flask, render_template, jsonify, request
import pymongo
import pandas as pd
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split # function for splitting data to train and test sets
import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
# %matplotlib inline
from subprocess import check_output
import plotly
import plotly.graph_objs as go
import json






app=Flask(__name__)
app = Flask(__name__, static_url_path='')

@app.route("/")
def echo():

    return render_template("index(1).html")

@app.route("/api/consigue/", methods=["POST"])
def consigue():
     # conectarme a mi mongo
    deleg = request.json["deleg"]
    myclient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydb= myclient["Geodat"]
    mycol= mydb["Geojsn2"]
     # obtener items
    list_jsons  = [x for x in mycol.find({},{"_id":False})]
    Delitos_DF=pd.DataFrame(list_jsons)
    Delitos_DF["tipoDelito"]=Delitos_DF.properties.map(lambda x: x["delito"])
    Delitos_DF["delegacion"]=Delitos_DF.properties.map(lambda x: x["alcaldia_hechos"])
    Delitos_DF["latitud"]=Delitos_DF.properties.map(lambda x : x["latitud"])
    Delitos_DF["longitud"]=Delitos_DF.properties.map(lambda x : x["longitud"])
    Delitos_DF["año"]=Delitos_DF.properties.map(lambda x : x["ao_hechos"])
    Geopoint=Delitos_DF[["latitud","longitud","tipoDelito","delegacion"]] 
    infoMapaX=Geopoint["delegacion"]== deleg #nombre de la delegacion de D3
    infoMapa=Geopoint.loc[infoMapaX,:]
    infoToMap=infoMapa.to_dict()
        
    crimejson=[]
    for i in range(infoMapa.shape[0]):
        crimejson.append(infoMapa.iloc[i].to_dict())    

    return jsonify({
              "crimejson": crimejson #Diccionario con datos para mapa
    })

@app.route("/wordcloud", methods=["GET"]) 
def wordcloud():
    data = pd.read_csv('./tweetsCrimeCDMX.csv',error_bad_lines=False)
    # Keeping only the neccessary columns
    data = data[['text']]
    stop_words_sp = set(stopwords.words('spanish'))
    def generateWordCloud(data,title):
        wordcloud = WordCloud(background_color='white',
        stopwords=stop_words_sp,
        max_words=300,
        max_font_size=50, 
        scale=5,
        random_state=42).generate(str(data))
        wordcloud.recolor(random_state=42)
        plt.figure(figsize=(20, 15))
        plt.title(title, fontsize=20,color='blue')
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.savefig("static/wordcloud.jpg")
        #plt.show()

             
    return render_template("index(1).html",words=generateWordCloud(data,'Crimen'))


@app.route("/plot")
def plots():
     # conectarme a mi mongo
    deleg = request.json["deleg"]
    myclient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydb= myclient["Geodat"]
    mycol= mydb["Geojsn2"]
     # obtener items
    list_jsons  = [x for x in mycol.find({},{"_id":False})]
    Delitos_DF=pd.DataFrame(list_jsons)
    Delitos_DF["tipoDelito"]=Delitos_DF.properties.map(lambda x: x["delito"])
    Delitos_DF["delegacion"]=Delitos_DF.properties.map(lambda x: x["alcaldia_hechos"])
    Delitos_DF["latitud"]=Delitos_DF.properties.map(lambda x : x["latitud"])
    Delitos_DF["longitud"]=Delitos_DF.properties.map(lambda x : x["longitud"])
    Delitos_DF["año"]=Delitos_DF.properties.map(lambda x : x["ao_hechos"])
    Aos=Delitos_DF["año"].value_counts()
    # Tipo=Delitos_DF["tipoDelito"].value_counts()
    # Crimen=Delitos_DF["delegacion"].value_counts()
    Delito_aos = Aos.to_frame()
    Delito_aos=Delito_aos.rename(columns={"delegacion":"Count"})
    Delito_aos=Delito_aos.reset_index()
    Delito_aos=Delito_aos.rename(columns={"index":"Delegacion"}) 

    data=[
        go.Bar(
            x=Delito_aos["Delegacion"],
            y=Delito_aos["Count"]
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

    
    


if __name__=="__main__":
    app.run(debug=True)

