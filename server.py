from flask import Flask, render_template,request
import pickle
import json
import numpy as np
app = Flask(__name__)




# data
__locations = None
__data_columns = None
__model = None


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    with open("./columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")





@app.route('/')
def home():
    return render_template('index.html', locations=__locations )


@app.route('/send',methods = ['GET','POST'])
def send():
    price = 0
    if request.method == 'POST':
        
        area = float(request.form['area'])
        bhk = int(request.form["bhk"])
        bath = int(request.form["bath"])
        location= request.form['location']
        
        try:
            loc_index = __data_columns.index(location.lower())
        except:
            loc_index = -1
        
        x = np.zeros(len(__data_columns))
        x[0] = area
        x[1] = bath
        x[2] = bhk
        if loc_index>=0:
            x[loc_index] = 1

        price = round(__model.predict([x])[0],2)      




        return render_template('index.html' , price=str(price))
    return render_template('index.html')

if __name__ == '__main__':
    load_saved_artifacts()
    app.run()
