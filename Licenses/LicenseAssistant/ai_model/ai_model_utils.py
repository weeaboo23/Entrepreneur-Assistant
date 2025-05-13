import joblib

clf = joblib.load("ai_model/model.pkl")
vectorizer = joblib.load("ai_model/vectorizer.pkl")
mlb = joblib.load("ai_model/label_binarizer.pkl")

def predict_licenses(structure, activity, location):
    text = f"{structure} {activity} {location}"
    X = vectorizer.transform([text])
    y_pred = clf.predict(X)
    return mlb.inverse_transform(y_pred)[0]
