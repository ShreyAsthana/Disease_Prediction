from flask import Flask, render_template, request
import pickle
import numpy as np
from myTraining import data_dict
from statistics import mode

app = Flask(__name__)
file = open("svm_model.pkl", "rb")
svm_model = pickle.load(file)
file.close()

file = open("nb_model.pkl", "rb")
nb_model = pickle.load(file)
file.close()

file = open("rf_model.pkl", "rb")
rf_model = pickle.load(file)
file.close()

def predictDisease(symptoms):
    symptoms = symptoms.split(",")
    
    # creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1
        
    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1,-1)
    
    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][svm_model.predict(input_data)[0]]
    
    # making final prediction by taking mode of all predictions
    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])
    return final_prediction

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        dict = (request.form)
        print(dict)
        # print(predictDisease("Itching,Skin Rash,Nodal Skin Eruptions,Dischromic  Patches"))
        Disease = predictDisease(f"{','.join(dict.getlist('Symptoms'))}")
        print(Disease)
        return render_template("index.html" , prediction = Disease)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
