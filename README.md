# Entrepreneur-Assistant

**Entrepreneur-Assistant** is an AI-powered web application that helps new business owners in India find the licenses or approvals they need based on their **business structure**, **activity**, and **location**. It uses LLMs, fuzzy matching, and self-learning logic to make regulatory navigation smarter and easier.

---

## 🧠 Features

- AI-generated license suggestions using a custom LLM
- Fuzzy matching of licenses with your database
- Learns from user interactions to improve future predictions
- Secure user authentication (Register/Login/Logout)
- Stores and maps license data by structure, activity, and location

---

## Distinctiveness and Complexity

Entrepreneur-Assistant is distinct from any of the CS50W projects in both intent and architecture. Unlike social networks or e-commerce applications, this project is centered around regulatory technology and compliance automation—an uncommon domain for student projects.

### Why it's Distinct:

- **Domain-Specific Use Case**: Focuses on Indian business regulations, a niche but practical area with real-world impact.
- **AI-Enhanced Prediction**: Uses scikit-learn to predict likely licenses based on business inputs (activity, structure, location).
- **Feedback-Based Learning**: Stores user inputs and AI predictions for retraining the model, enabling self-improvement.
- **Not CRUD-Centric**: Rather than just managing user-generated content, this system performs intelligent recommendations and backend analysis.
- **No resemblance to e-commerce or social media**: There are no listings, carts, feeds, or user follow systems. It offers guided AI-based form processing and dynamic license suggestion.

### Why it's Complex:

- **Custom ML Pipeline**: A custom-trained ML model is saved with `joblib`, retrained periodically using Django management commands.
- **NLP & Rule Matching**: License name extraction is enhanced using NLP techniques like spaCy and fuzzy matching.
- **Dynamic Recommendations**: Uses ManyToMany relationships and filtering logic in Django ORM to generate contextual suggestions.
- **User Feedback Logging**: System stores cases where the AI failed or partially succeeded to improve training data.

---

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Django Templates)
- **AI Integration**: OpenAI-compatible API (e.g., OpenRouter)
- **Database**: SQLite (default, can be upgraded)
- **Fuzzy Matching**: `fuzzywuzzy`
- **NER (planned)**: spaCy / Transformers

---

## File Structure

### Backend (`/backend`)

- `views.py`: Handles keyword-based form submission, AI license prediction, user feedback logging, and response rendering.
- `models.py`: Defines `ApprovalMapping`, `Approval`, `UserQuery`, and related models.
- `ai_model/`: Contains the scikit-learn training pipeline, preprocessing utilities, and a retrain command.
- `urls.py`: Routes API endpoints and web views.
- `admin.py`: Admin interface for managing approvals and queries.
- `requirements.txt`: Lists backend dependencies (Django, scikit-learn, spaCy, fuzzywuzzy).

### Frontend (`/templates` + JS)

- `index.html`: Form interface for users to input business details.
- `result.html`: Displays license recommendations.
- `script.js`: Handles frontend logic like form submission and dynamic response rendering.
- TailwindCSS or Bootstrap (used for responsiveness).

---

## How to Run the Application

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/weeaboo23/entrepreneur-assistant.git
cd entrepreneur-assistant

### 2.Install dependencies
pip install -r requirements.txt


### 3.Create a .env file in the project root with:
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://your-openai-compatible-api.com/v1

### 4.Run database migrations
python manage.py migrate

### 5.Start the development server
python manage.py runserver


## How It Works
Users input:

Business structure (e.g., Private Ltd)

Activity (e.g., Food Delivery)

Location (e.g., Maharashtra)

AI model returns a list of licenses

Licenses are cleaned and matched with existing data

Mappings are stored and reused to reduce API calls

New licenses are learned and saved for future use

## Author :
Ankit Kashyap
ankit2kashyap2@gmail.com
GitHub - weeaboo23

## Additional Notes

- Model retraining is based on new entries in the `UserQuery` model.
- The AI model is modular—easy to replace with more sophisticated transformers in the future.
- The system will later support license application tracking and auto-prefilled forms using department APIs.

---

## Future Enhancements

- Add authentication and user dashboards
- Integrate NSWS or state-specific APIs for real-time license applications
- Improve the ML model using transformer-based embeddings for better semantic accuracy

## Requirements

The `requirements.txt` includes:
- `Django`
- `scikit-learn`
- `joblib`
- `spaCy`
- `fuzzywuzzy`
- `python-Levenshtein`
- `pandas`

---
```
