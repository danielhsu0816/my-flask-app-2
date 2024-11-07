import os  
from tflite_runtime.interpreter import Interpreter  # 正確的引入方式 
from PIL import Image
import numpy as np 
from flask import Flask, request, render_template, redirect


app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 限制最大上傳檔案大小為 1MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 載入輕量化 tflite 模型
interpreter = Interpreter(model_path="trained_model.tflite")
interpreter.allocate_tensors()

# 為此 Dataset 定義的 mapping 關係
Emotion_Rule = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Sad",
    5: "Surprise",
    6: "Neutral"
}

def read_plot_and_test(image_path):
    """
    測試上傳到雲端平台 vercel 使用了輕量化的 PIL 套件來替套一些原本的影像處理功能，
    另外還有 tensorflow.lite 僅作為預測使用，可大幅減少所需依賴的套件資源
    """

    with Image.open(image_path).convert('L') as img:
            img_resized = img.resize((48, 48))
            test_sample = np.array(img_resized).reshape(1, 48, 48, 1).astype('float32') / 255.0

    # 設定模型輸入與輸出
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], test_sample)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index']).flatten()
    
    # 取得最高機率的類別與信心值
    index = np.argmax(prediction)
    confidence = round(prediction[index] * 100, 2)
    return Emotion_Rule[index], confidence

def allowed_file(filename):
    """
    判斷檔案擴展副檔名是否有在符合的需求範圍內。
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)

        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        emotion, confidence = read_plot_and_test(file_path)
        return render_template('result.html', emotion=emotion, confidence=confidence, filename=filename)

    return render_template('upload.html')

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
