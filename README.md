🤬 Toxic Comment ClassifierA full-stack Machine Learning application that detects toxic language in real-time using a microservices architecture.Badges📋 OverviewThis project is an end-to-end Machine Learning solution designed to identify toxic comments (insults, threats, obscenity) in text. It is built as a distributed system with a clear separation of concerns:Machine Learning: A Scikit-Learn pipeline (TF-IDF + Logistic Regression) trained on the Kaggle Jigsaw Dataset.Backend: A high-performance REST API built with FastAPI to serve model predictions.Frontend: An interactive web interface built with Streamlit.Infrastructure: Fully containerized using Docker and orchestrated with Docker Compose.🏗 ArchitectureThe application follows a microservices pattern where the frontend and backend run in isolated containers and communicate over a private Docker network.graph LR
    User[User] -- Browser --> Frontend[Streamlit Container\nPort: 8501]
    Frontend -- HTTP POST --> Backend[FastAPI Container\nPort: 8000]
    Backend -- Loads --> Model[ML Model (.pkl)]
    Backend -- JSON --> Frontend
🚀 Technologies UsedLanguage: Python 3.10ML Framework: Scikit-Learn, Pandas, JoblibBackend: FastAPI, Uvicorn, PydanticFrontend: StreamlitDevOps: Docker, Docker Compose🛠️ Installation & SetupPrerequisitesDocker Desktop installed and running.Git.Quick Start (Recommended)You can run the entire application with a single command.Clone the repositorygit clone [https://github.com/yourusername/toxic-classifier.git](https://github.com/yourusername/toxic-classifier.git)
cd toxic-classifier
Start the Applicationdocker-compose up --build
Access the AppFrontend (UI): Open http://localhost:8501 in your browser.Backend (API Docs): Open http://localhost:8000/docs to see the Swagger UI.💻 Usage1. Using the Web InterfaceSimply type a sentence into the text box and click Analyze. The app will display whether the comment is "Safe" or "Toxic" along with a confidence score.2. Using the API directlyYou can send a POST request to the local API:curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "You are amazing!"
}'
Response:{
  "is_toxic": false,
  "confidence": 0.02
}
📂 Project Structuretoxic-classifier/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py          # API Endpoints
│   │   ├── schemas.py       # Pydantic Models
│   │   └── resources/       # Trained ML Model (.pkl)
│   ├── Dockerfile           # Backend Container Config
│   └── requirements.txt
├── frontend/                # Streamlit Frontend
│   ├── main.py              # UI Logic
│   ├── Dockerfile           # Frontend Container Config
│   └── requirements.txt
├── model_training/          # ML Scripts
│   └── train_model.py       # Script to train and save the model
├── docker-compose.yml       # Orchestration file
└── README.md
🔮 Future ImprovementsImplement a Deep Learning model (BERT) for higher accuracy.Add multi-label classification (e.g., distinguishing between "Insult" vs "Threat").Deploy to a cloud provider (AWS/GCP).📄 LicenseThis project is open source and available under the MIT License.