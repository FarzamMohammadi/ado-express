# ADO Express 🚀
![GitHub release](https://img.shields.io/github/v/release/FarzamMohammadi/ado-express)
![GitHub](https://img.shields.io/github/license/FarzamMohammadi/ado-express)

Welcome to the ADO Express codebase, your new go-to tool for release management. This application is crafted to simplify and enhance the Azure DevOps release deployment process. It's intuitive, efficient, and powerful; ADO Express will revolutionize the way you handle releases.

## Quick Start

You have two options to get started:

1. **CLI Tools & Executables**: Get tasks done efficiently using either CLI tools or our plug-and-play executables. The CLI requires either Docker or Python, while executables are a hassle-free option requiring no preliminary installations—ideal for getting started right away. For more on CLI, see [CLI Usage](#%EF%B8%8F-cli-usage), and for executables, check out [Executables](#executables).

2. **Web Application**: For those who prefer a more graphical approach with an intuitive user interface, you can opt for the full web application. For this option, proceed to [Web Application Usage](#%EF%B8%8F-web-application-usage).

---

# 🖥️ CLI Usage

Run various tasks through the CLI with minimal setup. You can either use Docker or have Python installed. Not only will your results be logged, but they will also be saved into an Excel file located in [deployment-plan](ado_express\files\search-results\deployment-plan.xlsx).

0. [Environment Variables & Command Line Arguments](#environment-variables--command-line-arguments)
    - [List of Variables/Arguments](#list-of-variablesarguments)
    - [Command-Line Argument Order](#command-line-argument-order)
1. [Docker Deployment](#docker-deployment)
2. [Docker Development Container](#docker-development-container)
3. [Executables](#executables)
4. [Additional CLI Options](#additional-cli-options) (Deprecated)

## Environment Variables & Command Line Arguments
### List of Variables/Arguments

> **Note**: The default values for these variables are either `null` or `false`.

- **EXPLICIT_RELEASE_VALUES**: A dictionary where the key specifies the type of explicit release values (`include` or `exclude`), and the value is an array of release definitions.
  ```sh
  {'include': ['releaseOne', 'releaseTwo', 'releaseThree']}  
                  (OR)
  {'exclude': ['releaseOne', 'releaseTwo', 'releaseThree']}
  ```

- **CRUCIAL_RELEASE_DEFINITIONS**: An array of critical release definitions, delineated by commas. These releases take precedence and will be deployed first. If any of these deployments fail, the entire process will be halted.
   ```sh
   releaseOne
         (OR)
   releaseOne,releaseTwo,releaseThree
   ```

- **ORGANIZATION_URL**: The root URL of your organization's Azure DevOps instance.
  ```sh
  https://dev.azure.com/{organization}
  ```

- **PERSONAL_ACCESS_TOKEN**: Your personal access token. [Learn more.](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows)

- **QUERIES**: A list of IDs or URL paths to ADO queries, separated by commas.
  ```sh
   queryId
         (OR)
   queryId,queryId,queryId
  ```

- **RELEASE_NAME_FORMAT**: The format for the release name.
   ```sh
   Release-$(rev:r)
   ```

- **RELEASE_TARGET_ENV**: The environment to which you want to deploy your releases.
   ```sh
   prod
   ```

- **SEARCH_ONLY**: A Boolean variable to specify whether or not to deploy the search results.
   ```sh
   True
   (OR)
   False
   ```

- **VIA_ENV**: A Boolean variable to specify whether the search should be based on the release environment. (Set to `True` unless searching for **NON**-deployable results.)
   ```sh
   True
   (OR)
   False
   ```

- **VIA_ENV_LATEST_RELEASE**: A Boolean variable to determine whether to retrieve the latest release from the environment. (Set to `True` only if searching via query OR for **NON**-deployable results; otherwise, set to False.)
    ```sh
   True
   (OR)
   False
   ```

- **VIA_ENV_SOURCE_NAME**: The name of the environment where you've previously deployed releases (the same environment from which you retrieve Rollback releases).
  ```sh
   qa
   ```

### Command-Line Argument Order
   ```sh
    <EXPLICIT_RELEASE_VALUES> <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERIES> <RELEASE_NAME_FORMAT> <RELEASE_TARGET_ENV> <SEARCH_ONLY> <VIA_ENV> <VIA_ENV_LATEST_RELEASE> <VIA_ENV_SOURCE_NAME>
   ```

## Docker Deployment

1. **Prerequisite**: Ensure Docker is running.
2. **Build Container**: Navigate to the repository directory and execute the following command:
    ```sh
    docker build -t <CONTAINER_NAME> .
    ```
3. **Environment Variables**: Configure the required environment variables in the [.env](/.env) file.
4. **Run Container**: Execute the following command from within the repository directory:
    ```sh
    docker run --env-file ./.env -it <CONTAINER_NAME>
    ```
> For more details on run configurations, refer to the [Environment Variables & Command Line Arguments](#environment-variables--command-line-arguments) section.

## Docker Development Container

1. **Prerequisite**: Ensure Docker is running.
2. **VS Code Setup**: Open the repository directory in Visual Studio Code.
3. **Environment Variables**: Update your [.env](/.env) file with necessary variables.
4. **Quick Start**: Press `F1`, then search for and select `Dev Containers: Rebuild and Reopen in Container`.

> For more details on run configurations, refer to the [Environment Variables & Command Line Arguments](#environment-variables--command-line-arguments) section.

## Executables

Download the executables from the [GitHub Releases](https://github.com/FarzamMohammadi/ado-express/releases) page. Opt for the [latest](https://github.com/FarzamMohammadi/ado-express/releases/tag/1.36.0) to stay up-to-date with the newest features.

To run the executable for your OS, execute the following command:

```sh
./ado-express-{OS}.exe <EXPLICIT_RELEASE_VALUES> <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERIES> <RELEASE_NAME_FORMAT> <RELEASE_TARGET_ENV> <SEARCH_ONLY> <VIA_ENV> <VIA_ENV_SOURCE_NAME> <VIA_ENV_LATEST_RELEASE>
```

**Note**: Executables will log output solely to the terminal and won't generate log or search result files. For such functionality, please refer to other [CLI execution methods](#%EF%B8%8F-cli-usage).

> For more details on run configurations, refer to the [Environment Variables & Command Line Arguments](#environment-variables--command-line-arguments) section.

## Additional CLI Options (Deprecated)

For comprehensive CLI options, navigate to the dedicated README in the `./ado_express` directory. 

Quick Access: [CLI README](./ado_express/README.md)

> **Note**: Although most of the information in this document is still applicable, the document itself is deprecated and will no longer be updated.

Discover various instructions, tips, and tricks for optimizing your CLI experience!

# 🖥️ Web Application Usage

To operate the ADO Express Web Application, you must start both the [Frontend](#-frontend) and [Backend](#-backend-api) services of this project.

## 🎨 Frontend

The frontend of ADO Express is a sleek and modern web application. Let's get it running:

1. Navigate into the frontend directory:
   ```sh
   cd ado_express_app
   ```
2. Install Dependencies:
   ```sh
   npm i
   ```
4. Run the development server:
   ```sh
   npm run start
   ```
   Voila! You should now have the ADO Express web application running locally.

## 🔧 Backend (API)

The backend (API) of ADO Express powers all of the magic behind the scenes. To get it running, follow these steps:

### Preparation

First, you need to set up a virtual environment and install the necessary dependencies:

1. Create a virtual environment:
   ```sh
   python -m venv ./venv
   ```
2. Activate the virtual environment:
   - Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - Linux/macOS:
     ```sh
     source venv/bin/activate
     ```
3. Install Dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Run the API

With the virtual environment set up, you can now run the API:

1. Navigate into the API directory:
   ```sh
   cd ado_express_api
   ```
2. Start the application:
   ```sh
   daphne asgi:application
   ```

That's it! You should now have the ADO Express API running locally.

## 🌟 Shine Bright

ADO Express is more than just a tool; it's a game changer. With an emphasis on usability and performance, this app aims to simplify the complexities of release management, allowing you to focus on what truly matters - creating outstanding software.

Feel free to explore the repository, try out the application, and even contribute. Enjoy your journey with ADO Express!

## 🎥 See It To Believe It: The ADO Express Demo

Ever wondered how 'seamless' and 'efficient' looks in action? Well, wonder no more! [Click here to witness ADO Express revolutionizing Azure DevOps release management right before your eyes!](https://www.linkedin.com/posts/farzam-m_warmest-greetings-everyone-time-does-indeed-activity-7083582850511372288-Ov6c?utm_source=share&utm_medium=member_desktop) Experience the UI, functionality, and the game-changing features that will redefine your approach to release management. Don't just take our word for it—see it for yourself!

## 💡 Features

ADO Express boasts a range of features to simplify your Azure DevOps release management process. Here are some of the highlights:

- **Automated Release Management**: ADO Express automates your entire release management process, saving you time and ensuring uniformity in all your deployments. It prevents unwanted releases in deployments, and takes you from start to finish in your Continuous Deployment pipeline.

- **Search and Export**: With ADO Express, you can easily search through your releases and export your results to an Excel file. Whether you're using an ADO query or a deployment plan Excel file, ADO Express provides you with a detailed log of your release deployments.

- **Detailed Release Deployment**: ADO Express offers three types of detailed deployments: via query, via release number, and via environment. Each deployment type comes with its unique advantages, giving you the flexibility to choose the deployment method that best suits your needs.

- **Crucial Release Deployment Management**: ADO Express lets you mark certain releases as 'crucial.' These crucial deployments are run first, and in case of a deployment error, the application attempts to rollback and stop the processes.

- **Easy Run Options**: ADO Express provides you with a variety of ways to run the tool, from Docker to local execution, giving you the flexibility to choose the method that fits best in your workflow.

- _And many more..._: Dive in and discover what ADO Express has in store!

## 🛠️ Built With

ADO Express utilizes a robust tech stack:

- Frontend: **Svelte**, **Typescript**, **Tailwind**
- Backend: **Python**, **Django**

## 🤝 Contributions & Feedback

While we don't currently have a formal contribution guide, we still warmly welcome contributions from all! If you have suggestions, bug reports, or want to contribute code, please feel free to open an issue or pull request on our GitHub repository.

Also, if you encounter any issues or have ideas for enhancements, we would love to hear from you! Just head over to the [ADO Express Issues](https://github.com/FarzamMohammadi/ado-express/issues) page and drop us a note.

Whether you're providing feedback, reporting issues, or contributing to the code, your involvement is what makes this project shine. Thanks for being a part of ADO Express!

## 📝 License

This project is licensed under the terms of the [MIT license](LICENSE).

## 📮 Get in Touch

Have questions, suggestions, or just want to chat about ADO Express? Reach out!

- Farzam Mohammadi: [Email](mailto:farzammohammadia@gmail.com)
