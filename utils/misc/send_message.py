import random
import aiogram
import utils
import keyboards

from data.config import NUMBER_OF_WORDS, CORRECT_ANSWERS_TO_LEARN_WORDS, COUNTER_NUMBERS_TO_SEND_PROGRESS


async def send_words_accepted_message(learning_words, learning_words_translated, message: aiogram.types.Message,
                                      number_of_words=NUMBER_OF_WORDS):
    accepted_words = ''.join(
        f'{learning_words[i]} - {learning_words_translated[i]}\n' for i in range(number_of_words))
    await message.answer(text=f'✅Слова приняты:\n{accepted_words}'
                              f'Изъявив желание прекратить переводить, напиши /stop.',
                         reply_markup=keyboards.default.create_keyboard_markup.create_keyboard_markup(
                             text=learning_words_translated), disable_notification=True)


async def send_words_contains_learned_words_message(message: aiogram.types.Message):
    await message.answer(text='⚠️Некоторые из слов уже находятся в твоей библиотеке. '
                              'Сохранены будут только новые слова.')


async def send_words_not_accepted_message(learning_words, cause: str, message: aiogram.types.Message,
                                          number_of_words=NUMBER_OF_WORDS):
    match cause:
        case 'InvalidNumberOfWords':
            await message.answer(text=f'❗Ой, что-то пошло не так:\nТы ввёл {len(learning_words)} '
                                      f'{"слова" if 4 >= number_of_words > 1 else "слов"}, '
                                      f'в то время, как требуемое кол-во {number_of_words}.',
                                 disable_notification=True)
        case 'WordsContainNumbers':
            await message.answer(text='❗Ой, что-то пошло не так:\nВ твоих словах имеются цифры.',
                                 disable_notification=True)
        case 'WordsContainPunctuation':
            await message.answer(
                text='❗Ой, что-то пошло не так:\nВ твоих словах имеются пунктуационные символы.',
                disable_notification=True)
        case 'WordsRepeated':
            await message.answer(text='❗Ой, что-то пошло не так:\nНекоторые из твоих слов повторяются.')


async def send_random_word_message(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext,
                                   number_of_words=NUMBER_OF_WORDS):
    """Send random generated not previous word message"""
    async with state.proxy() as user_data:
        if 'ran_num' in user_data:
            user_data['ran_num'] = await utils.misc.generate_not_previous_number(previous_number=user_data['ran_num'])
        else:
            user_data['ran_num'] = random.randint(0, number_of_words - 1)
        learning_words = user_data['learning_words']
        ran_num = user_data['ran_num']
    await message.answer(text=f'{learning_words[ran_num]}', disable_notification=True)


async def send_correct_answer_message(user_counter, message: aiogram.types.Message,
                                      answers_to_learn_words=CORRECT_ANSWERS_TO_LEARN_WORDS,
                                      counter_numbers_to_send_progress=COUNTER_NUMBERS_TO_SEND_PROGRESS):
    if user_counter.get_score() in counter_numbers_to_send_progress:
        words_progress = 1.0 / (answers_to_learn_words / user_counter.get_score())
        await message.answer(text=f'🟢Верно!\n⏫Уровень изученности слов повышен до {words_progress:.0%}',
                             disable_notification=True)
    else:
        await message.answer(text=f'🟢Верно!', disable_notification=True)


async def send_words_learned_message(message: aiogram.types.Message):
    await message.answer(text=f'📜Слова выучены и сохранены в твою библиотеку!',
                         reply_markup=aiogram.types.reply_keyboard.ReplyKeyboardRemove(),
                         disable_notification=True)


async def send_scrabble_achievement_received_message(message: aiogram.types.Message):
    await message.answer(text=f"🏵Добавив в библиотеку первые слова, ты награждаешься достижением 🎓Эрудит!",
                         disable_notification=True)


async def send_pioneer_achievement_received_message(message: aiogram.types):
    await message.answer(text='🏵За использование проекта, начиная с его самых ранних дней, '
                              'ты награждаешься достижением 🌄Первопроходец!', disable_notification=True)


async def send_wrong_answer_message(user_counter, message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext,
                                    answers_to_learn_words=CORRECT_ANSWERS_TO_LEARN_WORDS,
                                    counter_numbers_to_send_progress=COUNTER_NUMBERS_TO_SEND_PROGRESS):
    wrong_answer_text = f'🔴Неверно.\nПравильный вариант - {await utils.misc.get_random_translated_word(state=state)}.\n'
    if user_counter.get_score() in counter_numbers_to_send_progress:
        words_progress = 1.0 / (answers_to_learn_words / user_counter.get_score())
        await message.answer(
            text=f'{wrong_answer_text}⏬Уровень изученности слов понижен до {words_progress:.0%}',
            disable_notification=True)
    else:
        await message.answer(text=f'{wrong_answer_text}', disable_notification=True)


async def send_unable_execute_stop_command_message(message: aiogram.types.Message):
    await message.answer(text='❕Мне нечего останавливать. Напиши /set для начала.', disable_notification=True)
