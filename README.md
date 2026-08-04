# SkinVision

SkinVision is an AI-powered skin tracking web application that helps users monitor visible skin changes over time. Users can upload facial images, receive a skin analysis, view progress charts, and manage skincare routines and products from a personal dashboard.

The application combines a deep-learning age estimation model with computer-vision based skin metric estimation for hydration, fine lines, and texture.

## Features

- User registration, login, JWT authentication, and password reset flow
- Photo upload with face detection and analysis
- AI-based facial age estimation using EfficientNetB0
- Computer-vision estimates for hydration, fine lines, and texture
- Analysis history with uploaded images and metric details
- Progress dashboard and visual charts
- Skincare routine and product management
- Admin login, user management, user search, and dashboard metrics
- GraphQL API with file upload support

## Tech Stack

### Frontend

- Vue 3
- Vite
- Vue Router
- Axios
- Chart.js

### Backend

- Flask
- GraphQL with Graphene
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- TensorFlow / Keras
- OpenCV

## Project Structure

```text
SkinVision_final/
├── backend/
│   ├── app/
│   │   ├── AIScript/
│   │   │   ├── face_analysis.py
│   │   │   ├── train_age_model.py
│   │   │   ├── test_age.py
│   │   │   └── haarcascade_frontalface.xml
│   │   ├── schema/
│   │   │   ├── queries.py
│   │   │   ├── types.py
│   │   │   └── mutations/
│   │   ├── models.py
│   │   ├── config.py
│   │   └── graphql_routes.py
│   ├── migrations/
│   ├── requirements.txt
│   └── wsgi.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── routes/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── RETRAIN_MODEL.sh
└── README.md
```

## How It Works

1. A user creates an account or logs in.
2. The user uploads a clear facial image from the dashboard.
3. The backend stores the photo and runs face detection.
4. The age model predicts facial age from the detected face.
5. Computer-vision logic estimates hydration, fine lines, and texture from the face image.
6. The analysis is saved and shown in the user's dashboard, history page, and progress charts.
7. The user can create skincare routines and add products based on their analysis.

## AI and Skin Metrics

SkinVision uses AI for facial age estimation. The model is trained on the UTKFace dataset, which provides age labels.

Hydration, fine lines, and texture are not trained from UTKFace because UTKFace does not include labels for those skin conditions. Instead, those metrics are estimated using image-processing techniques such as edge density, local contrast, brightness, and Laplacian variance.

This makes the system more transparent and avoids training a neural network on artificial labels.

## Getting Started

### Prerequisites

- Python 3.10+ or compatible local Python environment
- Node.js and npm
- Docker and Docker Compose, optional
- UTKFace dataset for model training

## Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
python3 wsgi.py
```

The backend runs at:

```text
http://localhost:5001
```

GraphQL endpoint:

```text
http://localhost:5001/graphql/
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

## Run With Docker

```bash
docker-compose up --build
```

Docker exposes:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:5001`

## Training the Model

The age model is trained from the UTKFace dataset. The dataset is expected at:

```text
/Users/raghdanaam/Downloads/archive/UTKFace
```

To retrain:

```bash
cd /Users/raghdanaam/Documents/SkinVision_final
./RETRAIN_MODEL.sh
```

The trained model is saved as:

```text
backend/app/AIScript/face_analysis_model.keras
```

To evaluate age prediction:

```bash
cd backend/app/AIScript
../../venv/bin/python test_age.py
```

## Environment Variables

The backend supports environment-based configuration through `.env`.

Useful variables:

```text
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///path/to/database.db
```

If these are not provided, development defaults are used.

## Database

The application uses SQLite by default. Main tables include:

- users and admins
- photos
- analyses
- routines
- products
- reports
- skin progress

Database migrations are managed with Flask-Migrate.

## Notes

- This project is intended for skin tracking and educational analysis.
- It is not a medical diagnosis tool.
- Hydration, fine lines, and texture are visual estimates, not clinical measurements.
- For better real-world accuracy, a labeled dermatology or skincare dataset would be needed for those specific skin metrics.

## Author

Developed by Raghdanaam.
