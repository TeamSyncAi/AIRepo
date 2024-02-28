from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyALK9FqS1q-mBz_WSeniUaUlyn5yLM0v6o")

model = genai.GenerativeModel('gemini-pro')

@app.route('/generate_project_modules', methods=['POST'])
def generate_project_modules():
    data = request.get_json()

    input_text = f"Generate the modules  for {data.get('name')} and the steps for each modules and make respected number of modules and steps ( generate the module like this **Name of module** and the step  like this *name of step* :\n\n"
    input_text += f"Project Description: {data.get('description')}\n"
    input_text += f"some key words: {data.get('keywords')}\n"

    print("Input Text:", input_text)

    generated_content = model.generate_content(input_text)

    generated_content_text = generated_content.text

    print("Generated Content Text:", generated_content_text)


    modules = []
    tasks = []
    current_module = None

    for line in generated_content_text.split('\n'):
        if line.startswith("**"):
            if current_module:
                modules.append({"module_name": current_module, "tasks": tasks})
                tasks = []  # Reset tasks for the next module
            current_module = line.split(":")[1].strip()
        elif line.startswith("*"):
            task_name = line.split(":")[1].strip()
            tasks.append(task_name)

    if current_module:
        modules.append({"module_name": current_module, "tasks": tasks})

    print("Generated Modules:", modules)

    return jsonify({"modules": modules})

if __name__ == '__main__':
    app.run(debug=True)
