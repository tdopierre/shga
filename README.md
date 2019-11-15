# SHGA
**S**econd **H**and **G**oods **Alerts**

Notifications for Second-Hand market websites:
- [Vinted](https://www.vinted.fr/)
- [Leboncoin](https://www.leboncoin.fr/)

# Get started
## Clone the repository
```shell script
mkdir -p ~/Projects && cd ~/Projects
git clone https://github.com/tdopierre/shga.git && cd shga
```
## Setup environment & project requirements
```shell script
python3 -m virtualenv .venv --python=/usr/bin/python3
.venv/bin/pip install -r requirements.txt
```
## Setup Telegram Bot
In order to use this repository, you will need to create a Telegram Bot. Here are the steps:
1. Open Telegram App
2. Say `/start` to BotFather, and follow the instructions
3. Once done, BotFather will give you the `token` and a link to talk to the bot
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
    "https://www.vinted.fr/vetements?order=newest_first",
    "..."
  ],
  "lbc_urls": [
    "https://www.leboncoin.fr/annonces/offres/ile_de_france/",
    "..."  
  ]
}
```


## Run the app
To run the app once, simply use the following command:
```shell script
.venv/bin/python app.py
```
If you want to run it on a regular basis, you can use a scheduling tool like [cron](https://en.wikipedia.org/wiki/Cron).

Example line in `crontab` file:

```shell script
* * * * * cd ~/Projects/shga && .venv/bin/python app.py
```
