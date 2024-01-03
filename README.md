# Mr Nags

Mr Nags is a complaint filing chatbot using egov digit platform.


## Installation

1. Create a file `ops/.env` and add the following lines to it:
    ```
    OPENAI_API_KEY=<OPENAI_API_KEY>
    TELEGRAM_BOT_TOKEN=<TELEGRAM BOT TOKEN>
    ```

2. Run the following commands:
    ```
    pip install -r requirements.txt
    ```
3. Once the installaton is complete, run the following command to start the bot:
    ```
    python main.py
    ```
4. Open Telegram and search for `@YourBotName` and start chatting with the bot.


## Usage

1. To start a conversation with the bot, start having a conversation by saying hey, hello or I have a complaint
2. The bot will ask you to describe your complaint
3. Once you have described your complaint, the bot will file the complaint and give you your complaint number.
4. Todo: You can use the complaint number to check the status of your complaint. 




