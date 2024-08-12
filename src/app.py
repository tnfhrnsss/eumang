from flask import Flask, request, jsonify, render_template
import sys, os

from main.provider import gemini_api

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#from provider import gpt_api
#from provider import gemini_api
from main.utils import ocr_

app = Flask(__name__)

# 이미지 업로드 폴더 경로 설정
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # 여기서 추가적인 이미지 처리를 할 수 있습니다.
        extracted_text = ocr_.extract_text_from_upload(filename)

        print(extracted_text)
        print("============")
        gpt_response = gemini_api.call_api(extracted_text)
        print(gpt_response)


        if gpt_response == '0':
            return jsonify({"result": "This is a phishing SMS according to Ai"}), 200
        else:
            custom_model_result = gemini_api.call_model(extracted_text)
            print("============")
            print(custom_model_result)
            if custom_model_result == '1':
                return jsonify({"result": "This is a safe SMS."}), 200
            else:
                return jsonify({"result": "This might still be a phishing SMS according to the Ai"}), 200
    return jsonify({'result': "There is no data."}), 200



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
