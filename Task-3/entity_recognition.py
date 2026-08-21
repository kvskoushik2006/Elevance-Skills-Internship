import re

def extract_medical_entities(question):

    question = question.lower()

    diseases = [
        "diabetes",
        "leukemia",
        "asthma",
        "cancer",
        "covid",
        "arthritis",
        "heart disease",
        "hypertension",
        "stroke",
        "anemia"
    ]

    question_types = {
        "symptoms": ["symptom", "symptoms", "sign", "signs"],
        "treatment": ["treatment", "treat", "therapy", "medicine"],
        "diagnosis": ["diagnosis", "diagnose", "test", "tests"],
        "prevention": ["prevent", "prevention"],
        "causes": ["cause", "causes", "reason"],
        "research": ["research", "clinical trial"],
        "stages": ["stage", "stages"],
        "outlook": ["prognosis", "outlook", "survival"]
    }

    disease = None

    for d in diseases:
        if d in question:
            disease = d.title()
            break

    qtype = "General"

    for key, words in question_types.items():
        for word in words:
            if re.search(r"\b" + re.escape(word) + r"\b", question):
                qtype = key.title()
                break

    return {
        "Disease": disease,
        "Question_Type": qtype
    }


if __name__ == "__main__":

    while True:

        q = input("Enter Question : ")

        if q.lower() == "exit":
            break

        print(extract_medical_entities(q))