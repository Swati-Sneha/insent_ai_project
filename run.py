# from telegram.ext import Updater, CommandHandler


# def hello(bot, update):
#
#     update.message.reply_text(
#         'Hello {}'.format(update.message.from_user.first_name))


token = "890443159:AAEVeJJY-0puigHnIAO6_IxXmO9VIfwJcc0"
typing_time = 3 # seconds

import time
import logging
from telegram.ext import (Filters, Updater, CommandHandler, InlineQueryHandler, ConversationHandler, RegexHandler, MessageHandler )
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
from intents import intents

CHOOSING_START, SUBSCRIBE, COMPANY, TYPING_REPLY  = range(4)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    welcome = intents['welcome']
    markup = [[_ans['answer'] for _ans in welcome['answers']]]
    update.message.reply_text(
        welcome['bot'][0],
        reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))

    return CHOOSING_START

def know_more(update, context):
    intent_description = intents['insent_description']
    msgs = intent_description['bot']
    for _msg in msgs:
        context.bot.send_chat_action(chat_id=update.message.chat_id ,action = ChatAction.TYPING)
        time.sleep(typing_time)
        update.message.reply_text(_msg)
    markup = [[_ans['answer'] for _ans in intent_description['answers']]]

    update.message.reply_text(
        'Please choose',
        reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))

    return SUBSCRIBE

def talk_to_team(update, context):
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

def facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def received_information(update, context):
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
        user_data.clear()
        return ConversationHandler.END
    except:
        return ConversationHandler.END


def main():
    try:
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

        dp.add_handler(conv_handler)

        dp.add_error_handler(error)

        updater.start_polling()

        updater.idle()
    except:
        return ConversationHandler.END

if __name__ == '__main__':
    main()
