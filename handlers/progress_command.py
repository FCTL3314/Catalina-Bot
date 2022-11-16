import aiogram
import utils


async def send_progress_message(message: aiogram.types.Message):
    user_id = message.from_user.id
    achievements_text = await utils.misc.create_achievements_text(message=message)
    with utils.database.postgres_database as db:
        learned_words = await db.get_learned_words(user_id=user_id)
    if learned_words is None:
        await message.answer(text=f'📜Библиотека твоих слов:\n\n'
                                  f'🕸Пытаясь найти твои слова, я сделала вывод, что их нет.',
                             disable_notification=True)
    else:
        await message.answer(text=f'📜Библиотека твоих слов:\n\n{", ".join(sorted(learned_words))}.',
                             disable_notification=True)
    if not achievements_text:
        await message.answer(text=f'🏵Витрина твоих достижений:\n\n'
                                  f'🕸Видимо, в настоящее время твоя витрина достижений пустует.',
                             disable_notification=True)
    else:
        await message.answer(text=f'🏵Витрина твоих достижений:\n\n● {achievements_text}',
                             disable_notification=True)


def register_progress_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=send_progress_message, commands=['progress'])
