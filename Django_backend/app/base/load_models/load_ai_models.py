import pickle
diabetes_model_path = "base/save_models/diabetes_classifier_model.sav"
heartattack_model_path = "base/save_models/diabetes_classifier_model.sav"

def use_ai_diabetes(test_values=[[]]):
    loaded_model = pickle.load(open(diabetes_model_path, 'rb'))   
    result = loaded_model.predict(test_values)[0]
    return "no" if result == 0 else "yes"

def use_ai_heart_disease(test_values=[[]]):
    loaded_model = pickle.load(open(heartattack_model_path, 'rb'))   
    result = loaded_model.predict(test_values)[0]
    return "no" if result == 0 else "yes"