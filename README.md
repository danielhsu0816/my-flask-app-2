[README.md](https://github.com/user-attachments/files/35129668/README.md)
# Facial Expression Recognition with Flask and TensorFlow Lite

A Flask web application that classifies facial expressions in uploaded images using a pretrained TensorFlow Lite model. The application preprocesses each image, runs inference, and displays the predicted expression and its confidence score alongside the uploaded image.

This project demonstrates a complete image inference workflow, from browser uploads and image preprocessing to model execution and result presentation.

## Features

- Upload PNG, JPG, or JPEG images through a web interface.
- Classify images into seven expression categories.
- Display the predicted label and model confidence percentage.
- Validate file extensions and upload size in the browser and backend.
- Run inference using `tflite_runtime`, with Flask, Pillow, and NumPy.
- Package the application with the included Dockerfile.

The upload and results pages currently use Traditional Chinese interface text. Prediction labels are in English.

## Expression Categories

| Model output index | Label |
| --- | --- |
| 0 | Angry |
| 1 | Disgust |
| 2 | Fear |
| 3 | Happy |
| 4 | Sad |
| 5 | Surprise |
| 6 | Neutral |

## How It Works

1. The user submits an image to the `/` route.
2. Flask saves the image in `static/uploads/`.
3. Pillow converts the image to grayscale and resizes it to 48 × 48 pixels.
4. NumPy converts the image to `float32`, normalizes pixel values by dividing by 255, and reshapes the input to `(1, 48, 48, 1)`.
5. The TensorFlow Lite interpreter runs `trained_model.tflite`.
6. The application selects the output with the highest score and renders the result page.

The displayed confidence is the highest model output multiplied by 100 and rounded to two decimal places. Its calibration has not been documented.

## Technology Stack

| Component | Technology |
| --- | --- |
| Backend | Python, Flask |
| Model inference | TensorFlow Lite Runtime 2.14.0 |
| Image preprocessing | Pillow, NumPy |
| Frontend | HTML, CSS, JavaScript, Jinja templates |
| Containerization | Docker |

## Project Structure

```text
my-flask-app-2/
├── app.py
├── trained_model.tflite
├── requirements.txt
├── Dockerfile
├── README.md
├── tflite_runtime-2.14.0-cp310-cp310-manylinux2014_x86_64.whl
├── templates/
│   ├── upload.html
│   └── result.html
└── static/
    ├── css/styles.css
    ├── js/script.js
    └── uploads/.gitkeep
```

## Local Setup

The bundled runtime wheel targets **CPython 3.10 on Linux x86_64**. Use a compatible Linux environment or WSL2 on Windows. On other platforms, use a compatible runtime package or the Docker instructions below.

```bash
git clone https://github.com/danielhsu0816/my-flask-app-2.git
cd my-flask-app-2

python3.10 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install ./tflite_runtime-2.14.0-cp310-cp310-manylinux2014_x86_64.whl
python -m pip install -r requirements.txt

python app.py
```

Open **http://127.0.0.1:5000** in your browser. Run the command from the repository root so the application can locate the model and upload directory.

`requirements.txt` installs Flask, Pillow, and `numpy<2`. The TensorFlow Lite Runtime must be installed separately using the wheel above.

## Run with Docker

From the repository root, build and run the image for Linux AMD64 to match the bundled runtime wheel.

```bash
docker build --platform linux/amd64 -t facial-expression-app .
docker run --rm --platform linux/amd64 -p 5000:5000 facial-expression-app
```

Open **http://localhost:5000**. On ARM computers, this requires Docker support for AMD64 emulation. The container uses the Flask development server.

## Try It

1. Open the upload page.
2. Select a PNG, JPG, or JPEG image smaller than 1 MB.
3. Click **上傳** to submit the image.
4. Review the predicted expression and confidence score.
5. Click **返回上傳頁面** to try another image.

For a more suitable input, use a clear image cropped around a single face. The application resizes the entire uploaded image and does not automatically detect or crop faces.

Feel free to upload your own photo and give it a try! You can also try a synthetic face image from [This Person Does Not Exist](https://thispersondoesnotexist.com/).

Flask limits the entire upload request to 1,048,576 bytes, including multipart form overhead, so files close to that limit may be rejected.

## Model Information

The repository includes `trained_model.tflite`, an approximately 15 MB pretrained model. The application expects a grayscale `float32` input with shape `(1, 48, 48, 1)` and seven output scores in the category order listed above.

Training code, dataset provenance, architecture details, evaluation metrics, and model licensing are not documented in the repository. No accuracy claim is made here. The predictions describe visual expression categories and should not be treated as a reliable measurement of a person's internal emotional state.

## Current Limitations

- Uploaded files remain in `static/uploads/` and are accessible through Flask's static file routes. Automatic deletion is not implemented.
- The backend uses the original uploaded filename. Uploads with the same filename can overwrite earlier files.
- The app uses one shared interpreter without synchronization for concurrent inference requests.
- `python app.py` enables Flask debug mode. Public deployment requires a production server and additional upload handling controls.
- The shared JavaScript also runs on the result page and attempts to attach an event listener to a form that is only present on the upload page. This can produce a browser console error on the result page.

## Author

Daniel Hsu

## License

The repository does not currently include a license file. Reuse permissions for the application and pretrained model should be confirmed with the repository owner.
