# Chat With GPT
<img width="1792" alt="image" src="https://github.com/jiawen7777/chat-with-gpt/assets/43628912/ac407a90-479e-4953-b6e9-b48de3cecbdd">

# Features
 - Stream output: The application allows for streaming output, providing real-time updates.
 - MongoDB integration: The chat history is stored in MongoDB, ensuring data persistence.
 - Custom Model Parameters: The model parameters can be customized based on specific requirements.
 - Function Calling: The application supports calling functions to perform specific tasks like the plugin of GPT

# Usage

The project structure consists of two folders: `server` for the backend and `web` for the frontend. Please follow the instructions below for setting up the environment.



## Setup Backend Environment
Please refer to `server/README.md` for instructions on setting up the backend of the project.

### Setup your API
you need to set up your  [Amap Weather API](https://lbs.amap.com/api/webservice/guide/api/weatherinfo/#t1) and [OpenAI API](https://openai.com/blog/openai-api) in
`server/chatbot/.env`


## Setup Frontend Environment
It is recommended to use `nvm` for managing Node versions on your device. Ensure you have Node and `npm` installed, preferably with the following versions:
```bash
❯ node -v
v18.17.1
❯ npm -v
9.6.7
```

To set up the frontend environment, navigate to the `web/app` folder and execute the following command to install all the required dependencies:
```bash
npm i
```

Once the installation is complete, run the following command to start the project. By default, it will run on port `5173`. Visit `http://localhost:5173/` to access the application.
```bash
npm run dev
```
Enjoy bro!
