#!/bin/bash
### Catuserbot Config vars setter by KD

pprint (){
	cpurple='\033[0;35m'
	eval "export color='$cpurple'"
	
    printf "$color $1"
}

color_reset(){ printf '\033[0;37m';}

pprint "Welcome to Catuserbot Config setter\n\n"
sleep 1
clear
pprint "\n\nScript needs sudo privileges in order to edit config vars\n"
sudo test
clear
sleep 2

pprint "\nEnter Your Values Below\n\n\n"
pprint "#get this values from the my.telegram.org"
pprint "\nAPI ID: "; color_reset; read api_id
pprint "#get this values from the my.telegram.org"
pprint "\nAPI HASH: "; color_reset; read api_hash
pprint "#the name to display in your alive message write inside " " "
pprint "\nALIVE_NAME: "; color_reset; read alive_name
pprint "# create any PostgreSQL database (i recommend to use elephantsql) and paste"
pprint "\nDB URI: "; color_reset; read database_url
pprint "# create a new bot in @botfather and fill the following vales with bottoken"
pprint "\nBOT TOKEN: "; color_reset; read bot_token
pprint "# create a private group and a rose bot to it and type /id and paste that id here"
pprint "\nPM_LOGGER_GROUP_ID: "; color_reset; read logger
pprint "#create a private group and a rose bot to it and type /id and paste that id here"
pprint "\nPRIVATE_GROUP_BOT_API_ID: "; color_reset; read group_id
pprint "\nSTRING_SESSION: "; color_reset; read string_session
pprint "\nEXTERNAL_REPO:  "; color_reset; write "https://github.com/TgCatUB/CatPlugins"
pprint "\n\nProcessing your vars, Wait a while!" "cgreen"


if [ -f config.py ]; then

echo """from sample_config import Config


class Development(Config):

#get this values from the my.telegram.org
API_ID = $api_id
#get this values from the my.telegram.org
API_HASH = $api_hash
# the name to display in your alive message
ALIVE_NAME = $alive_name
# create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
DB_URI = $database_url
# create a new bot in @botfather and fill the following vales with bottoken
BOT_TOKEN = $bot_token
# create a private group and a rose bot to it and type /id and paste that id here
PM_LOGGER_GROUP_ID = $logger
# create a private group and a rose bot to it and type /id and paste that id here
PRIVATE_GROUP_BOT_API_ID = $group_id
STRING_SESSION = $string_session
# command handler
COMMAND_HAND_LER = "."
# command hanler for sudo
SUDO_COMMAND_HAND_LER = "."
# External plugins repo
EXTERNAL_REPO = 
# if you need badcat plugins set "True"
BADCAT = "False"""" > config.py

fi

clear
pprint "\n\n\nYour Vars have been saved Successfully!, Thanks for using catuserbot var setter
pprint "\n\n\nWant more vars?"
pprint "\nCheckout config.py inside catuserbot folder for setting addtional vars. You can change all images , Thumbs, mode and everything from vars. Have a look towards them\n\n"
