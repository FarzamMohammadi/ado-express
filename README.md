# ADO Express 🚀
![GitHub release](https://img.shields.io/github/v/release/FarzamMohammadi/ado-express)
![GitHub](https://img.shields.io/github/license/FarzamMohammadi/ado-express)

ADO Express simplifies Azure DevOps release management by streamlining the deployment process. It's intuitive and efficient, revolutionizing how you handle releases.

## 💡 Features

- **Automated Release Management**: Streamlines your release process, ensuring uniform deployments.
- **Search and Export**: Search releases and export results to Excel.
- **Detailed Release Deployment**: Deploy via query, release number, or environment.
- **Crucial Release Management**: Prioritize crucial releases; halt on failure.
- **Flexible Run Options**: Run via Docker, locally, or through scripts.

## Quick Start

Choose your preferred method:

1. **CLI**: Efficiently perform tasks via the command line. Requires Docker or Python. See [CLI Usage](#️-cli-usage).
2. **Web Application**: Use an intuitive UI for a graphical approach. See [Web Application Usage](#️-web-application-usage).

## 🎥 Demo

Experience ADO Express in action: [Watch the Demo](https://www.linkedin.com/posts/farzam-m_warmest-greetings-everyone-time-does-indeed-activity-7083582850511372288-Ov6c?utm_source=share&utm_medium=member_desktop)

---

# 🖥️ CLI Usage

Run tasks through the CLI with minimal setup using Docker or Python. Results are logged and saved to [deployment-plan.xlsx](ado_express/files/search-results/deployment-plan.xlsx).

## Environment Variables & Command Line Arguments

Set the following variables (defaults are `null` or `false`):

- **EXPLICIT_RELEASE_VALUES**: Dict specifying releases to include or exclude.
  ```sh
  {'include': ['releaseOne', 'releaseTwo']}
  # or
  {'exclude': ['releaseOne', 'releaseTwo']}
  ```
- **CRUCIAL_RELEASE_DEFINITIONS**: Comma-separated critical release definitions to deploy first.
  ```sh
  releaseOne,releaseTwo
  ```
- **ORGANIZATION_URL**: Your Azure DevOps organization URL.
  ```sh
  https://dev.azure.com/{organization}
  ```
- **PERSONAL_ACCESS_TOKEN**: Your Azure DevOps personal access token.
- **QUERIES**: Comma-separated ADO query IDs or paths.
  ```sh
  queryId1,queryId2
  ```
- **RELEASE_NAME_FORMAT**: Format for release names.
  ```sh
  Release-$(rev:r)
  ```
- **RELEASE_TARGET_ENV**: Target deployment environment (e.g., `prod`).
- **SEARCH_ONLY**: `True` to search without deploying, `False` otherwise.
- **VIA_ENV**: `True` to search based on release environment.
- **VIA_ENV_LATEST_RELEASE**: `True` to retrieve latest release from environment.
- **VIA_ENV_SOURCE_NAME**: Name of the source environment (e.g., `qa`).

**Command-Line Argument Order**:
```sh
<EXPLICIT_RELEASE_VALUES> <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERIES> <RELEASE_NAME_FORMAT> <RELEASE_TARGET_ENV> <SEARCH_ONLY> <VIA_ENV> <VIA_ENV_LATEST_RELEASE> <VIA_ENV_SOURCE_NAME>
```

## Docker Deployment

1. **Prerequisite**: Ensure Docker is running.
2. **Build Container**:
   ```sh
   docker build -t <CONTAINER_NAME> .
   ```
3. **Set Environment Variables**: Configure variables in [.env](/.env).
4. **Run Container**:
   ```sh
   docker run --env-file ./.env -it <CONTAINER_NAME>
   ```

Refer to [Environment Variables & Command Line Arguments](#environment-variables--command-line-arguments) for details.

## Docker Development Container

1. **Prerequisite**: Ensure Docker is running.
2. **Open in VS Code**: Open the repository in Visual Studio Code.
3. **Set Environment Variables**: Update [.env](/.env).
4. **Start Dev Container**: Press `F1`, select `Dev Containers: Rebuild and Reopen in Container`.

---

# 🖥️ Web Application Usage

Start both the [Frontend](#-frontend) and [Backend](#-backend-api) services.

## Quick Start

You can quickly start both the frontend and backend using npm scripts:

1. **Install Dependencies**:
   - **Windows**:
     ```sh
     npm run install-all
     ```
   - **Unix-based systems**:
     ```sh
     npm run install-all-unix
     ```
2. **Start the Application**:
   ```sh
   npm run start
   ```
   This command will concurrently start both the frontend and backend.

## Detailed Setup

### 🎨 Frontend

1. Navigate to the frontend directory:
   ```sh
   cd ado_express_app
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Run the development server:
   ```sh
   npm run start
   ```
   The frontend should now be running locally.

### 🔧 Backend (API)

#### Preparation

1. Create a virtual environment:
   ```sh
   python -m venv ./venv
   ```
2. Activate the virtual environment:
   - **Windows**:
     ```sh
     .\venv\Scripts\activate
     ```
   - **Linux/macOS**:
     ```sh
     source venv/bin/activate
     ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

#### Run the API

1. Navigate to the API directory:
   ```sh
   cd ado_express_api
   ```
2. Start the application:
   ```sh
   daphne asgi:application
   ```
   The backend API should now be running locally.

---

## 🛠️ Built With

- **Frontend**: Svelte, TypeScript, Tailwind CSS
- **Backend**: Python, Django

## 🤝 Contributions & Feedback

Contributions are welcome! Open an issue or pull request on [GitHub](https://github.com/FarzamMohammadi/ado-express/issues).

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 📮 Get in Touch

- Farzam Mohammadi: [Email](mailto:farzammohammadia@gmail.com)