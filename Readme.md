# U-Bot
**This is a completed project that was transfered from [completed private branch](https://github.com/SamuelSau/gitReady)** 
<!-- ![U-BOT](/ubot_transparent.png) -->

This is a web based application that allows you to practice with a AI-powered voice assistant that conducts a software engineering technical interview using natural language. The voice assistant primarily uses OpenAI's ChatGPT API, OpenAI's Whisper API, and ElevenLabs API to power the voice assistance feature. The web application is hosted on the cloud provider Google Cloud, with PostgreSQL as the DBMS and Django as the backend framework.

![Picture of program](/screenshot.png)

## Getting Started

To use the voice assistant, simply navigate to the web application's URL in your browser. Once the page has loaded, you can press the start recording button to speak with the AI. Ensure that your microphone and speakers are unmuted. The AI will speak back to you when you finish when you stop recording and submit it.

## Start the web application:

Navigate to <insertUrl> in your web browser to access the web application.

## To Run On Your Local Computer

Inside the frontend folder within the terminal, run

> yarn

then in the package manager, run

> yarn dev

Inside the backend folder, install python dependencies and then run

> python manage.py runserver

NOTE: you will need .env file containing your API keys for openAI as well as ElevenLabs.

## Credits

This web application was developed by _Samuel Sau_, _Cory Zastoupil_, _Janpaul Paredero_, and _Pedro Mir Reynoso_

## License

This project is licensed under the MIT License.
