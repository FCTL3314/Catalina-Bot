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
    user_score = context.user_data[f'user_score: {update.message.chat_id}']
    user_score.increment()
    match user_score.get_score():
        case 5:
            update.message.reply_text(text=f'🟢5 раз подряд!\nПродолжай в том же духе!',
                                      disable_notification=True)
        case 10:
            update.message.reply_text(text=f'🟢10 раз подряд!\nТы уже на половине пути, осталось совсем ничего!',
                                      disable_notification=True)
        case 15:
            update.message.reply_text(text=f'🟢15 раз подряд!\nЕщё чуть-чуть и ты их выучишь! Я в тебя верю!',
                                      disable_notification=True)
        case 20:
            update.message.reply_text(text=f'🟢20 раз подряд!\nПоздравляю! Ты выучил слова!',
                                      disable_notification=True)
        case _ if user_score.get_score() > 20:
            update.message.reply_text(
                text=f'🟢Серия верных ответов:'
                     f' {context.user_data[f"user_score: {update.message.chat_id}"].get_score()}!',
                disable_notification=True)
        case _:
            update.message.reply_text(text=f'🟢Верно!', disable_notification=True)
    bot.generate_random_word(update=update, context=context)


def wrong_answer_response(update: telegram.Update, context: telegram.ext.CallbackContext):
    reset_correct_answers_series(update=update, context=context)
    update.message.reply_text(
        text=f'🔴Неверно.\nПравильный вариант - {get_translated_word(update=update, context=context)}',
        disable_notification=True)
    bot.generate_random_word(update=update, context=context)


def reset_correct_answers_series(update: telegram.Update, context: telegram.ext.CallbackContext):
    user_score = context.user_data[f'user_score: {update.message.chat_id}']
    if 10 <= user_score.get_score() < 15:
        ran_num = random.randint(0, 2)
        match ran_num:
            case 0:
                update.message.reply_text(text=f'Да, знаю. Обидно терять такую серию правильных ответов.',
                                          disable_notification=True)
            case 1:
                update.message.reply_text(text=f'Не переживай. Без ошибок эти слова явно не выучить.',
                                          disable_notification=True)
            case 2:
                update.message.reply_text(text=f'Зато теперь ты точно запомнишь это слово.',
                                          disable_notification=True)
    elif 15 <= user_score.get_score() < 20:
        update.message.reply_text(text=f'Главное не останавливайся, у тебя всё получится! Ты почти у цели!.',
                                  disable_notification=True)

    context.user_data[f'user_score: {update.message.chat_id}'].reset()
