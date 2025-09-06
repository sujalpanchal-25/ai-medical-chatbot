import os
import pandas as pd
import google.generativeai as genai

# ===============================
# ✅ Set your Gemini API key
# ===============================
API_KEY = "AIzaSyB0kUURH9SvniAOq4oxV2BjkP0EPT8kQfc"  # Replace with your key
genai.configure(api_key=API_KEY)

# ===============================
# ✅ CSV path
# ===============================
CSV_PATH = os.path.join(os.path.dirname(__file__), "ai-medical-chatbot.csv")

# ===============================
# ✅ Load dataset safely
# ===============================
try:
    df = pd.read_csv(CSV_PATH)
    print("✅ CSV Loaded Successfully!")
    print("📊 Preview of dataset:")
    print(df.head())
except Exception as e:
    print("❌ Error loading CSV:", e)
    exit()

# ===============================
# 🔹 Function to retrieve answer from dataset
# ===============================
def retrieve_answer(user_input):
    user_input = user_input.lower()
    matched_symptoms = []

    # Assume first column is "diseases" or "Description" to skip
    for symptom in df.columns[1:]:
        if symptom.lower() in user_input:
            matched_symptoms.append(symptom)

    if not matched_symptoms:
        return None  # no match found

    # Filter diseases based on matched symptoms
    possible_diseases = df[df[matched_symptoms].sum(axis=1) > 0][df.columns[0]].unique()

    # Take top 5 diseases
    top_diseases = list(possible_diseases[:5])

    return f"Based on your symptoms ({', '.join(matched_symptoms)}), possible diseases may include: {', '.join(top_diseases)}"

# ===============================
# 🔹 Main chatbot response function
# ===============================
def chatbot_response(user_input):
    user_input_lower = user_input.lower().strip()

    # 1️⃣ Handle greetings
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    farewells = ["bye", "exit", "quit", "goodbye"]

    if user_input_lower in greetings:
        return " Hello! How are you feeling today?.\n\tHow can I help you today with health-related questions?"
    elif user_input_lower in farewells:
        return " Take care! Goodbye 👋"

    # 2️⃣ Check dataset
    context = retrieve_answer(user_input)
    if context:
        return context

    # 3️⃣ Fallback to Gemini
    if API_KEY:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            You are a helpful health assistant.
            The user asked: {user_input}
            Provide a safe, simple, and clear health suggestion.
            If it may indicate something serious, advise them to consult a doctor.
            """
            response = model.generate_content(prompt)
            return response.text + "\n⚠️ Please consult a doctor for serious or persistent issues."
        except Exception as e:
            print("⚠️ Gemini API Error:", e)
            return "Sorry, I could not connect to the health knowledge base. Please consult a doctor."
    else:
        return "Please consult a doctor."

def get_response(user_input):
    return chatbot_response(user_input)
# ===============================
# 🔹 Chat loop
# ===============================
def chatbot():
    print("🤖 Hello! How are you feeling today?\n  How can I help you today with health-related questions?(type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in ["exit", "quit", "bye", "goodbye"]:
            print("🤖 HealthBot: Take care! Goodbye 👋")
            break
        response = chatbot_response(user_input)
        print("🤖 HealthBot:", response)

# ===============================
# Run chatbot
# ===============================
if __name__ == "__main__":
    chatbot()
