## Prerequisites

Before you begin, make sure you have the following installed on your machine:

- **Node.js** (for running the React frontend) - [Download Node.js](https://nodejs.org/)
- **npm** (Node Package Manager for managing frontend dependencies) - [npm Documentation](https://www.npmjs.com/)
- **Python 3** (for running the Python backend) - [Download Python 3](https://www.python.org/downloads/)
- **pip** (Python package installer) - [pip Documentation](https://pip.pypa.io/en/stable/)

---

## Installation and Running the Project Locally

### Step 1: Frontend Setup

1. Open a terminal and navigate to the following directory:

   ```bash
   cd src/UI/Product_UI/
   ```
2. Install the frontend dependencies by running:

   ```bash
   npm i
   ```
3. Once the dependencies are installed, start the React development server:

   ```bash
   npm start
   ```

### Step 2: Server Setup

1. Open a terminal and navigate to the following directory:

   ```bash
   cd src/UI/Product_UI/src/server
   ```
2. Install the server dependencies by running:

   ```bash
   pip install Flask flask-cors requests flask-caching pymongo pyjwt werkzeug pandas numpy joblib lime mistralai xgboost
   ```
3. Once the dependencies are installed, start the React development server:

   ```bash
    python3 server.py
   ```