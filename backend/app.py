from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def match_all(symptoms, keywords):
    return all(kw in symptoms for kw in keywords)

PATHWAYS = [
    {
        "name": "Irritable Bowel Syndrome",
        "criteria": [
            "intermittent lower abdominal pain", "cramping", "pain relieved by defecation",
            "alternating constipation diarrhea", "urgency", "incomplete evacuation", "mucus stools"
        ],
        "diagnosis": "Irritable Bowel Syndrome (IBS)",
        "tests": ["Sigmoidoscopy", "Colonoscopy", "Barium enema", "Rectal biopsy", "Stool exam"],
        "treatment": ["Symptomatic relief", "Diet adjustment", "Stress reduction"],
        "followup": ["As needed"]
    },
    # Add more pathways here...
]

def format_response(pathway):
    response = f"Tentative Diagnosis: {pathway['diagnosis']}\n"
    if "tests" in pathway:
        response += "Order: " + ", ".join(pathway["tests"]) + "\n"
    if "treatment" in pathway:
        response += "Treatment: " + ", ".join(pathway["treatment"]) + "\n"
    if "followup" in pathway:
        response += "Follow-up: " + ", ".join(pathway["followup"])
    return response

@app.route('/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    data = request.get_json(force=True)
    symptoms = data.get("symptoms", "").lower()
    followup_answers = data.get("followupAnswers", {})

    for pathway in PATHWAYS:
        if pathway.get("criteria") and match_all(symptoms, pathway["criteria"]):
            return jsonify({
                "success": True,
                "analysis": format_response(pathway),
                "requiresFollowup": False,
                "followupQuestions": []
            })

    followup_questions = []
    if "abdominal pain" in symptoms or "distention" in symptoms or "bloating" in symptoms:
        if not followup_answers.get("pain_location"):
            followup_questions.append("Where is the pain located? (e.g., upper, lower, right, left, central)")
        if not followup_answers.get("pain_character"):
            followup_questions.append("Can you describe the pain? (e.g., sharp, dull, cramping, constant, intermittent)")
        if not followup_answers.get("pain_severity"):
            followup_questions.append("How severe is the pain on a scale of 1-10?")
        if not followup_answers.get("pain_duration"):
            followup_questions.append("How long have you had this pain?")
        if not followup_answers.get("associated_symptoms"):
            followup_questions.append("Are there any associated symptoms? (e.g., fever, vomiting, diarrhea, constipation, blood in stool, urinary symptoms, vaginal bleeding)")

    if followup_questions:
        return jsonify({
            "success": True,
            "analysis": "To help narrow down the diagnosis, please answer the following questions:",
            "requiresFollowup": True,
            "followupQuestions": followup_questions
        })

    return jsonify({
        "success": False,
        "analysis": "Unable to determine a specific diagnosis based on the provided symptoms. Please consult a healthcare professional for further assessment.",
        "requiresFollowup": False,
        "followupQuestions": []
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
