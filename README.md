# FIFA-Analysis

FIFA-Analysis is a full-stack web application that allows users to find similar players based on FIFA player data using a K-Nearest Neighbors (KNN) algorithm. This project leverages **FastAPI** for the backend, **Next.js** with Tailwind CSS for the frontend, and a robust machine learning pipeline for player similarity recommendations.

## Features

* **Player Similarity Finder**: Input a player's name and get a list of players with similar attributes.
* **Customizable ML Pipeline**: Preprocesses and transforms player data with categorical, ordinal, and numeric features.
* **Interactive Frontend**: Built with Next.js for a responsive and user-friendly experience.
* **Backend API**: Powered by FastAPI for seamless data exchange and model inference.

## Project Structure

```
├── app/                    # Next.js frontend application
├── backend/               # FastAPI backend
├── components/            # Reusable React components
├── data/raw/             # Raw FIFA dataset
├── lib/                  # Helper utilities
├── notebooks/            # Jupyter Notebooks for ML experimentation
├── start.js              # Script to run backend and frontend
└── README.md             # Project documentation
```

## Technologies Used

### Backend
* **FastAPI**: RESTful API development
* **Scikit-learn**: ML preprocessing and KNN implementation
* **Pandas & NumPy**: Data manipulation and analysis

### Frontend
* **Next.js**: React framework for server-side rendering
* **Tailwind CSS**: Responsive styling

### Machine Learning
* **K-Nearest Neighbors**: Player similarity calculation
* **Preprocessing Pipelines**: Handling categorical, ordinal, and numeric features

## Installation

### Prerequisites
Ensure the following tools are installed:
* **Node.js** and **npm**
* **Python 3.9+**
* **Git**

### Clone the Repository
```bash
git clone https://github.com/Sathyavrv/FIFA-Analysis.git
cd FIFA-Analysis
```

### Setup and Run

1. Install Dependencies

   **Frontend**
   ```bash
   cd app
   npm install
   ```

   **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run the Application

   Use the provided `start.js` script to start both the backend and frontend:
   ```bash
   node start.js
   ```

   Alternatively, you can run them manually:

   **Backend**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Frontend**
   ```bash
   cd app
   npm start
   ```

## API Endpoints

### `/api/similar-players`
**Method**: `POST`  
**Description**: Returns similar players for a given player name.  
**Request Body**:
```json
{
    "playerName": "Lionel Messi"
}
```

**Response**:
```json
[
    {
        "name": "Riyad Mahrez",
        "age": 30,
        "overall": 86,
        "potential": 86,
        "value": "65500000",
        "country": "Algeria",
        "club": "Manchester City",
        "best_position": "RW",
        "preferred_foot": "Left",
        "similarity_score": 0.92
    },
    ...
]
```

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Enter a player's name in the input field and click **Find Similar Players**
3. View the list of similar players and their attributes

## Machine Learning Workflow

1. **Dataset**: The FIFA dataset is preprocessed to extract features like `age`, `overall`, `potential`, and more.
2. **Preprocessing**:
   * **One-Hot Encoding**: Categorical features (e.g., `country`, `club`)
   * **Ordinal Encoding**: Ordered features (e.g., `work rate`)
   * **Standard Scaling**: Numeric features
3. **KNN Model**: Finds similar players based on cosine similarity

## Example Output

**Input**: "Lionel Messi"

| Name | Age | Overall | Potential | Value | Club | Position | Preferred Foot |
|------|-----|---------|-----------|--------|------|----------|----------------|
| Riyad Mahrez | 30 | 86 | 86 | 65,500,000 | Manchester City | RW | Left |
| Antoine Griezmann | 30 | 85 | 85 | 53,000,000 | Atlético de Madrid | ST | Left |
| Memphis Depay | 27 | 85 | 85 | 58,500,000 | FC Barcelona | CF | Right |
