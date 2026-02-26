from flask import Flask, request, jsonify

import os

import subprocess

import time

import pyautogui



app = Flask(__name__)



# Constants

TARGET_DIR = r'C:\Users\Hp\My_AI_works\n8n\UI_automation'

FILE_NAME = 'socialeagle.txt'

FILE_PATH = os.path.join(TARGET_DIR, FILE_NAME)



@app.route('/update-notepad', methods=['POST'])

def update_notepad():

    # 1. Get the payload from the request

    data = request.get_json()

   

    if not data or 'content' not in data:

        return jsonify({"error": "Missing 'content' in JSON payload"}), 400

   

    content = data['content']



    try:

        # 2. File System Logic

        if not os.path.exists(TARGET_DIR):

            os.makedirs(TARGET_DIR)

           

        mode = 'a' if os.path.exists(FILE_PATH) else 'w'

        prefix = '\n' if mode == 'a' else ''

       

        with open(FILE_PATH, mode) as f:

            f.write(f"{prefix}{content}")



        # 3. UI Automation Sequence

        # Open Notepad with the file

        subprocess.Popen(['notepad.exe', FILE_PATH])

       

        # Give Notepad a moment to gain focus

        time.sleep(1.5)

       

        # Save and Close

        pyautogui.hotkey('ctrl', 's')

        time.sleep(0.5)

        pyautogui.hotkey('alt', 'f4')



        return jsonify({"message": f"Successfully updated and closed {FILE_NAME}"}), 200



    except Exception as e:

        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':

    # Running on port 5000 by default

    app.run(host='0.0.0.0', port=5000, debug=True)