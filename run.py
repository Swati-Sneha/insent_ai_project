
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the
bot.
"""


from configparser import ConfigParser
import time
import logging
from telegram.ext import Filters, Updater, CommandHandler, InlineQueryHandler, ConversationHandler, RegexHandler, MessageHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
from intents import intents
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

CHOOSING_START, SUBSCRIBE, COMPANY, TYPING_REPLY  = range(4)

'''Reading config details'''
config = ConfigParser()
config.readfp(open('intents.config'))
token = config.get('settings', 'token')
typing_time = config.getint('settings', 'typing_time')
db_url=config.get('settings', 'DB_URL')

print(token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


meta = MetaData()
engine=create_engine(db_url, echo=True)

'''Initialising table'''
users = Table(
   'users', meta, 
   Column('email_id', String, primary_key = True), 
   Column('company_name', String), 
)



def start(update, context):

    '''starts the conversation with /start -- trigger point of chat'''

    welcome = intents['welcome']
    markup = [[_ans['answer'] for _ans in welcome['answers']]]  
    update.message.reply_text(
        welcome['bot'][0],
        reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))

    return CHOOSING_START

def know_more(update, context):

    '''fetches description from intents and displays and gives further options to user'''
    
    intent_description = intents['insent_description']
    msgs = intent_description['bot']
    for _msg in msgs:
        context.bot.send_chat_action(chat_id=update.message.chat_id ,action = ChatAction.TYPING) #typing_action shown
        time.sleep(typing_time)
        update.message.reply_text(_msg)

    markup = [[_ans['answer'] for _ans in intent_description['answers']]]    

    update.message.reply_text(
        'Please choose',
        reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))

    return SUBSCRIBE

def talk_to_team(update, context):

    '''fetches the messges for connect_insent_team and displays the options accordingly'''

    subscribe = intents['connect_insent_team']
    msgs = subscribe['bot']
    for _msg in msgs:
        context.bot.send_chat_action(chat_id=update.message.chat_id ,action = ChatAction.TYPING)
        time.sleep(typing_time)
        update.message.reply_text(_msg)


    markup = [[_ans['answer'] for _ans in subscribe['answers']]]

    update.message.reply_text(
        'Please choose',
        reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))

    return SUBSCRIBE


def email(update, context):
    context.user_data['choice'] = 'email' 
    subscribe = intents['subscribe_insent']
    msgs = subscribe['bot']
    update.message.reply_text(msgs[0])
    return TYPING_REPLY

def company(update, context):
    context.user_data['choice'] = 'company'
    subscribe = intents['company']
    msgs = subscribe['bot']
    update.message.reply_text(msgs[0])
    return TYPING_REPLY


def received_information(update, context):
    '''saves the data -company and email to the context'''
    user_data = context.user_data
    text = update.message.text
    category = user_data.get('choice', '')
    user_data[category] = text
    if category:
        del user_data['choice']
    if category == 'email':
        company(update, context)
    else:
        good_for_now(update, context)

def good_for_now(update, context):
    subscribe = intents['good_for_now']
    msgs = subscribe['bot']
    update.message.reply_text(msgs[0])
    done(update, context)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def done(update, context):
    try:
        update.message.reply_text("Thanks")
        user_data = context.user_data
        '''saving the details to database before deleting'''
        ins=users.insert()
        ins = users.insert().values(email_id=context.user_data['email'], company_name=context.user_data['company'])
        conn = engine.connect()
        result = conn.execute(ins)
        user_data.clear()

        return ConversationHandler.END
    except:
        return ConversationHandler.END


def main():
    try:
        #Create the Updater and pass it your bot's token.s
        updater = Updater(token, use_context=True)
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],

            states={
                CHOOSING_START: [
                                        RegexHandler('^(Know more about Insent.ai)$',
                                                        know_more,
                                                        pass_user_data=True),

                                        RegexHandler('^(Keep me posted. I want to subscribe)$',
                                                        email,
                                                        pass_user_data=True),

                                        RegexHandler('^(Talk to Insent.ai team)$',
                                                        talk_to_team,
                                                        pass_user_data=True),

                                        RegexHandler('^(Just Browsing)$',
                                                        good_for_now,
                                                        pass_user_data=True),
                           ],
                SUBSCRIBE: [RegexHandler('^(Yes, I want to subscribe)$',
                                            email,
                                            pass_user_data=True),
                            RegexHandler('^(No, I am good for now)$',
                                            done,
                                            pass_user_data=True)],

                TYPING_REPLY: [MessageHandler(Filters.text,
                                              received_information,
                                              pass_user_data=True),
                               ],
            },

            fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)],
            allow_reentry= True
        )

        #handler to hold a conversation with a single user
        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(error)

        # Start the bot
        updater.start_polling()



        # Run the bot until Ctrl-C is pressed 
        # start_polling() is non-blocking
        updater.idle()
    except:
        return ConversationHandler.END

if __name__ == '__main__':
    main()
