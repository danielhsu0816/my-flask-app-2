# 使用官方的 Python 3.10 基礎映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔案並安裝依賴
COPY requirements.txt /app/
COPY tflite_runtime-2.14.0-cp310-cp310-manylinux2014_x86_64.whl /app/ 
RUN pip install --no-cache-dir /app/tflite_runtime-2.14.0-cp310-cp310-manylinux2014_x86_64.whl
RUN pip install --no-cache-dir -r requirements.txt 

# 複製應用程式代碼到容器中
COPY . .

# 開放 Flask 默認端口
EXPOSE 5000

# 設定環境變量以便 Flask 可以運行
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 啟動 Flask 應用
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
