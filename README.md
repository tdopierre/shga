# Vinted Alerts
App which sends notifications when a new Vinted item matching a pre-defined search appears

# Get started
## Install requirements
```shell script
pip install -r requirements.txt
```
## Setup Telegram Bot
In order to use this repository, you will need to create a Telegram Bot. Here are the steps:
1. Open Telegram App
2. Say `/start` to BotFather, and follow the instructions
3. Once done, BotFather will give you the `token`
4. Talk to your bot once. Be gentle!
5. Get your `chat_id`: 
```shell script
$ curl -X GET https://api.telegram.org/bot<token>/getUpdates \
	| jq '.result[0].message.chat.id'
```

## Create a config file
```shell script
touch config.json
```
The config file should have the following structure:
```json
{
  "telegram_token": "<token>",
  "telegram_chat_id": "<chat_id>",
  "vinted_urls": [
    "<URL_1>",
    "<URL_2>",
    "..."
  ]
}
```
The `vinted_urls` field lists all urls corresponding to searches you want to monitor. 

Example: `https://www.vinted.fr/vetements?order=newest_first`


## Run the app
To run the app once, simply use the following command:
```shell script
python app.py
```
If you want to run it on a regular basis, you can use a scheduling tool like [cron](https://en.wikipedia.org/wiki/Cron).

Example line in `crontab` file:

```shell script
* * * * * cd ~/Projects/vinted_alerts && python app.py
```
