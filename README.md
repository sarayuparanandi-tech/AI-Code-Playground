# AI-Powered Online Code Playground

An interactive online code editor for **HTML, CSS, and JavaScript** that:
- Lets you write & run code in the browser with live preview
- Uses a **Machine Learning model (Naive Bayes)** to predict whether your code is *Error-Free* or *Contains Errors*
- Uses a **Generative AI** assistant to suggest debugging fixes

## Project Structure
Sarayu_AICodePlayground/
├── Frontend/          # HTML, CSS, JS — the code editor UI
│   ├── index.html
│   ├── style.css
│   └── script.js
├── Backend/           # Flask API (ML + GenAI endpoints)
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
├── ML/
│   ├── dataset/code_samples.csv         # Training data
│   ├── notebook/train_model.ipynb       # Training notebook
│   └── saved_model/model.pkl            # Trained Naive Bayes model
├── Docs/
│   └── Project_Documentation.md
└── README.md

## Setup Instructions

### 1. Install Python dependencies
```bash
cd Backend
pip install -r requirements.txt

### 2. Run the server
```bash
python app.py
```
Visit **http://localhost:5000** in your browser.

## ▶ Steps to Run the Project
1. `pip install -r Backend/requirements.txt`
2. `python Backend/app.py`
3. Open `http://localhost:5000`
4. Write code in the editor → click **Run** to preview
5. Click **Predict Errors (ML)** → Naive Bayes classifies the code
6. Click **AI Debug (GenAI)** → get correction suggestions

## Re-train the model
```bash
cd ML/notebook
jupyter notebook train_model.ipynb
```
Run all cells — outputs are saved to `ML/saved_model/model.pkl`.

## Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python · Flask · Flask-CORS
- **ML:** scikit-learn (Multinomial Naive Bayes, char n-grams)
- **GenAI:** AI-based debugging suggestion module

## Modules
| Module | Tech | Purpose |
|---|---|---|
| Code Editor | HTML/CSS/JS | Write & run code, live preview |
| Error Predictor | Naive Bayes | Classify code as clean / error |
| AI Debugger | Generative AI | Suggest fixes for buggy code |
| Integration | Flask REST API | Connects all modules |

Author: **Sarayu**
