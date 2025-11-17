# mbot: For Svelte and FastAPI Chat with OpenAI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Overview

**mbot** is an open-source starter project for building AI-powered chatbot applications. Combining a modern tech stack of **Svelte** for the frontend and **FastAPI** for the backend, it provides Firebase authentication and integrates seamlessly with OpenAI APIs.

This project is designed for:

- **AI startup enthusiasts** building chat applications.
- **Developers** exploring Svelte and FastAPI.
- **Hobbyists** experimenting with OpenAI's GPT models.

## Features

- Modern Frontend: Built with SvelteKit for reactive UI.
- FastAPI Backend: Async API integration with OpenAI.
- Secure Authentication: Firebase for user authentication.
- Boilerplate for AI Apps: A great foundation for interactive AI chat solutions.

## Demo

<img src="docs/assets/images/mbot_preview.gif" alt="mbot Demo" width="220">

## Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Environment Variables](#environment-variables)
5. [Running the Project](#running-the-project)
6. [Authentication](#authentication)
7. [Contributing](#contributing)
8. [License](#license)

## Getting Started

### Prerequisites

1. Node.js
    Install from [Node.js official site](https://nodejs.org).
2. Python
    Install from [Python's official site](https://www.python.org).
3. Firebase Project
    Create a Firebase project for authentication (free tier is sufficient).
4. OpenAI API Key
    Obtain an API key from [OpenAI's platform](https://platform.openai.com).

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/mthomason/mbot.git
cd mbot
```

#### 2. Set Up the Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate (On Windows: venv\Scripts\activate)
pip install -r ../requirements.txt
```

Alternatively, you can install the `.venv` in the projects root directory

```bash
python -m venv .venv
source .venv/bin/activate (On Windows: .venv\Scripts\activate)
pip install requirements.txt
```

#### 3. Set Up the Frontend

```bash
cd frontend
npm install
```

#### 4. Add your Environment Variables

See [Environment Variables](#environment-variables)

#### 5. Run the project (see Running the Project)

## Project Structure

```bash
frontend/         # SvelteKit app for the UI
backend/          # FastAPI app for APIs
backend/app/      # FastAPI endpoints and logic
backend/mserv/    # Backend utilities and config
electron/         # Optional Electron app (if applicable)
docs/             # Documentation files
```

## Environment Variables

To configure your environment variables, create a `.env` file in the root directory of the project with the following structure:

```bash
# Used for Firebase authentication
GOOGLE_PROJECT_ID_MBOT=my-firebase-project-id 

# Used for OpenAI services
OPENAI_API_KEY_MBOT=sk-xxxxxxxxxxxxxxxxxxxx
```

- **GOOGLE_PROJECT_ID_MBOT**: Your Firebase project ID, used for authentication.
- **OPENAI_API_KEY_MBOT**: Your API key for OpenAI services. Remember that usage may incur costs.

## Running the Project

This project was developed using Visual Studio Code as the IDE and includes a pre-configured launch profile for a seamless startup experience.

The recommended way to run the application is by using the provided "Launch mbot (client and server)" debug configuration. The configuration file, `launch.json`, is included in the `.vscode` folder.

To run the project:

1. Open the project root in VSCode.
2. After you've created the `venv` virtual environment, VS Code should automatically detect it and ask if you want to use it for the workspace. Click "Yes" to accept.
3. If you are not prompted, you can manually select the interpreter by opening the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and typing "Python: Select Interpreter". Choose the interpreter located in the `venv/bin` (or `venv\Scripts` on Windows) directory.
4. Navigate to the "Run and Debug" view (usually in the left-hand sidebar).
5. Select the `Launch mbot (client and server)` configuration from the dropdown menu.
6. Press F5 or click the green play button to start both the frontend and backend servers.

Alternatively, you can run the components manually:

### Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:fastapi_app --reload
```

### Frontend

```bash
cd frontend
npm run dev
```

## Authentication

To use the chat functionality, you must be authenticated. This is a deliberate feature of this starter project to demonstrate how to protect routes and integrate authentication in a modern web application.

**Note:** Currently, there is no warning message if you attempt to use the chat without being authenticated. The chat simply will not respond. This is a known issue and will be addressed in a future update.

## Contributing

Contributions are welcome! Please fork the repo and submit a pull request. Before contributing, make sure to:

1. Write clear documentation for new features.
2. Follow the existing code style.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Webfront

This project has a webfront [here](https://mthomason.github.io/mbot/).
