from flask import Flask, request, jsonify
import requests
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyALK9FqS1q-mBz_WSeniUaUlyn5yLM0v6o")
model = genai.GenerativeModel('gemini-pro')
NODE_SERVER_URL = 'http://localhost:3000/modules/receive_modules'

@app.route('/generate_project_modules', methods=['POST'])
def generate_project_modules():
    try:
        data = request.get_json()
        project_id = data.get('projectID')  # Extract project ID from request

        input_text = f"Generate the modules and the steps for each module for {data.get('name')} please make it a rich planning and in this form **Module name** and *steps name*  :\n\n"
        input_text += f"Project Description: {data.get('description')}\n"
        input_text += f"some key words: {data.get('keywords')}\n"
        input_text += f"and i want it always in this form example(**Module 1: Data Collection** * **Step 1:** Scrape historical stock data from financial websites)"

        generated_content = model.generate_content(input_text)
        generated_content_text = generated_content.text

        modules = []
        tasks = []
        current_module = None

        for line in generated_content_text.split('\n'):
            split_line = line.split(":")
            if len(split_line) >= 2:
                if line.startswith("**"):
                    if current_module:
                        # Append the project ID to each module
                        modules.append({"projectID": project_id, "module_name": current_module, "tasks": tasks})
                        tasks = []
                    current_module = split_line[1].strip().rstrip('**')
                elif line.startswith("*"):
                    task_name = split_line[1].strip().lstrip('**')
                    tasks.append(task_name)

        if current_module:
            modules.append({"projectID": project_id, "module_name": current_module, "tasks": tasks})

        response = requests.post(NODE_SERVER_URL, json={"projectID": project_id, "modules": modules})
        response_data = response.json()
        return jsonify({"message": "Modules sent successfully", "response": response_data})
    except Exception as e:
        return jsonify({"error": f"Failed to generate and send modules: {str(e)}"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
