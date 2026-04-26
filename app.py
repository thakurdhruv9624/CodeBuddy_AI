import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# आपकी API Key यहाँ पहले से है, मैंने बस उसे सुरक्षित फॉर्मेट में रखा है
api_key = os.getenv("AIzaSyBs4WrcJn4WS8Lo87Aw_aaH9j5c4l7lmhs")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
genai.configure(api_key="AIzaSyBs4WrcJn4WS8Lo87Aw_aaH9j5c4l7lmhs")

# मॉडल का नाम 'gemini-1.5-flash' रखें, यह सबसे स्टेबल है
# यह अपने आप सही मॉडल ढूंढ लेगा
def get_active_model():
    """Return the first model that supports content generation."""
    model_list = genai.list_models()
    for model_item in model_list:
        if "generateContent" in model_item.supported_generation_methods:
            return model_item.name

    raise RuntimeError("No compatible Gemini model found.")


active_model = get_active_model()
model = genai.GenerativeModel(active_model)
print(f"बधाई हो! हम इस मॉडल का इस्तेमाल कर रहे हैं: {active_model}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=["POST"])
def ask():
    # यहाँ हम देख रहे हैं कि 'message' नाम से डेटा आ रहा है या नहीं
    data = request.get_json()
    user_message = data.get('message') or data.get('user_input') # दोनों चेक करेगा
    
    if not user_message:
        return jsonify({'reply': 'खाली मैसेज मिला है!'})

    try:
        # AI को मैसेज भेज रहे हैं
        # AI को निर्देश (Personality) देना
        instructions = "You are 'CodeBuddy AI', a cool and helpful coding expert. Use emojis, keep it professional yet friendly, and explain complex things simply."
        full_prompt = f"{instructions} \nUser: {user_message}"
        
        # अब हम सीधा user_message नहीं, बल्कि full_prompt भेज रहे हैं
        full_prompt = f"{instructions}\nUser: {user_message}"

        response = model.generate_content(full_prompt)
        return jsonify({'reply': response.text})
    

    except Exception as exc:
        # अगर कोई एरर आता है, तो वह आपके टर्मिनल (VS Code) में दिखेगा
        print(f"DEBUG ERROR: {exc}")
        return jsonify({'reply': f"Oops! एरर आया: {str(e)[:50]}..."})

if __name__ == '__main__':
    app.run(debug=True)