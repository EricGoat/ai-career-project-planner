# AI Career Project Planner

An AI-driven career planning system that analyzes a user's resume and target job description, identifies missing skills, and generates project and learning recommendations to help close those skill gaps.

## Backend Setup
### 1. Go to project root
```bash
cd ai-career-project-planner
```

### 2. Create and activate virtual environment
macOs / Linux
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
### 3. Upgrade pip
```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install backend dependencies
```bash
pip install "numpy<2"
pip install flask flask-cors python-dotenv
pip install spacy==3.7.5
pip install scikit-learn sentence-transformers sqlalchemy pandas pytest
```

### 5. Download the spaCy English model
```bash
python -m spacy download en_core_web_sm
```

### 6. Create the database
```bash
python -m backend.models.database
```

## Frontend Setup

### 1. Go to angular app folder
```bash
cd frontend/angular-app
```

### 2. Install frontend dependencies
```bash
npm install
```

## Run Application

### Terminal 1: Backend (root dir)
```bash
python -m backend.app
```

### Terminal 2: Frontend (angular-app dir)
```bash
ng serve
```