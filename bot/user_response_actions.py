import telegram.ext
import bot
import random


def get_translated_word(update: telegram.Update, context: telegram.ext.CallbackContext) -> str:
    """Gets the translated word from context.user_data['learning_words_translated']"""
    translated_word = context.user_data['learning_words_translated'][
        context.bot_data[f"ran_num: {update.message.chat_id}"]]
    return translated_word


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Checks the translated word entered by the user for correctness"""
    answer = update.message.text
    if answer.lower() == get_translated_word(update=update, context=context).lower():
        correct_answer_response(update=update, context=context)
    else:
        wrong_answer_response(update=update, context=context)


def correct_answer_response(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.user_data[f'user_score: {update.message.chat_id}'].increment()
    if context.user_data[f'user_score: {update.message.chat_id}'].get_score() == 5:
        update.message.reply_text(text=f'🟢5 раз подряд!\nПродолжай в том же духе!',
                                  disable_notification=True)
    elif context.user_data[f'user_score: {update.message.chat_id}'].get_score() == 10:
        update.message.reply_text(text=f'🟢10 раз подряд!\nМожет ты и так знаешь эти слова ?',
                                  disable_notification=True)
    elif context.user_data[f'user_score: {update.message.chat_id}'].get_score() == 20:
        update.message.reply_text(text=f'🟢20 раз подряд!\nТы явно выучил слова.',
                                  disable_notification=True)
    elif context.user_data[f'user_score: {update.message.chat_id}'].get_score() > 20:
        update.message.reply_text(
            text=f'🟢Серия верных ответов: {context.user_data[f"user_score: {update.message.chat_id}"].get_score()}!',
            disable_notification=True)
    else:
        update.message.reply_text(text=f'🟢Верно!', disable_notification=True)
    bot.generate_random_word(update=update, context=context)


def wrong_answer_response(update: telegram.Update, context: telegram.ext.CallbackContext):
    reset_correct_answers_series(update=update, context=context)
    update.message.reply_text(
        text=f'🔴Неверно.\nПравильный вариант - {get_translated_word(update=update, context=context)}',
        disable_notification=True)
    bot.generate_random_word(update=update, context=context)


def reset_correct_answers_series(update: telegram.Update, context: telegram.ext.CallbackContext):
    if context.user_data[f'user_score: {update.message.chat_id}'].get_score() >= 10:
        ran_num = random.randint(0, 2)
        if ran_num == 0:
            update.message.reply_text(text=f'Да, знаю. Обидно терять такую серию правильных ответов.',
                                      disable_notification=True)
        elif ran_num == 1:
            update.message.reply_text(text=f'Ничего, рано или поздно ты бы всё равно обнулил эту серию.',
                                      disable_notification=True)
        elif ran_num == 2:
            update.message.reply_text(text=f'Зато теперь ты точно запомнишь это слово.',
                                      disable_notification=True)
    context.user_data[f'user_score: {update.message.chat_id}'].reset()
