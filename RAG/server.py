import os
import base64
import tempfile
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import worker

# 1. Initialize Flask App & CORS
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)


# 2. Route: Home Page (UI)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# 3. Route: Process PDF Document Upload
@app.route("/process-document", methods=["POST"])
def process_document_route():
    try:
        data = request.get_json()
        if not data or "fileData" not in data:
            return jsonify({"botResponse": "No document data received."}), 400

        file_data = data["fileData"]

        # Parse base64 data URL from browser reader: "data:application/pdf;base64,..."
        if "," in file_data:
            file_data = file_data.split(",")[1]

        pdf_bytes = base64.b64decode(file_data)

        # Save to a temporary PDF file for PyPDFLoader
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_bytes)
            temp_pdf_path = temp_file.name

        # Process document through worker RAG chain
        result_msg = worker.process_document(temp_pdf_path)

        # Clean up temp file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

        return jsonify({
            "botResponse": f"✅ Document processed successfully! You can now ask questions about it."
        })

    except Exception as e:
        return jsonify({"botResponse": f"Error processing document: {str(e)}"}), 500


# 4. Route: Process Chat Prompt
@app.route("/process-message", methods=["POST"])
def process_message_route():
    try:
        data = request.get_json()
        user_message = data.get("userMessage", "").strip()

        if not user_message:
            return jsonify({"botResponse": "Please enter a valid message."}), 400

        # Query worker RAG engine
        bot_response = worker.process_prompt(user_message)

        return jsonify({"botResponse": bot_response})

    except Exception as e:
        return jsonify({"botResponse": f"Error answering question: {str(e)}"}), 500


# 5. Start Server
if __name__ == "__main__":
    print("🚀 RAG Assistant Server starting on http://127.0.0.1:8000 ...")
    app.run(host="0.0.0.0", port=8000, debug=True)