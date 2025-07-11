from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from utils.database import database

import logging
import hashlib

logging.basicConfig(format='[%(asctime)s - %(message)s]', level=logging.INFO)


# Create 1 specific button
async def create_button(text: str, callback: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text=text, callback_data=callback)
    fds = InlineKeyboardButton(text='Mandar se foder!', callback_data=f'fds-{callback}')
    keyboard.add(button)
    keyboard.add(fds)

    return keyboard


# dest[0] == sender
# dest[1] == recipient
async def get_sender_recipient(query: CallbackQuery) -> tuple:
    if type(query) == CallbackQuery:
        sender = query.data.split()[0].strip()
        recipient = query.data.split()[-1].strip()
        return (sender, recipient)
    
    elif type(query) == InlineQuery:
        sender = '@' + query['from']['username']
        recipient = query.query.split()[-1].strip()
        return (sender, recipient)


async def get_username(query: CallbackQuery) -> str:
    user = '@' + query['from']['username']
    return user


# Manages button callback
async def manage_callback(query: CallbackQuery):
    curious_click = await get_username(query)
    print(query)
    q = query.data.split(sep='-')
    print(query.data, query.data.split(sep='-'))

    try:
        if q[0] == 'fds':
            print(q, q[1])
            user = int(query['from']['id'])
            data = database.get_data(int(q[1]))[0][2]
            print(data)
            sender = str(data).split()[0]; print(sender)
            recipient = str(data).split()[-1]; print(recipient)

            if curious_click.strip() == recipient.strip():
                await app.edit_message_text(
                    text=f'Vai se foder, {sender}!',
                    chat_id=query.chat_instance,
                    inline_message_id=query.inline_message_id,
                    
                    )
    
    except IndexError:
        data = database.get_data(query.data)[0][2]
        sender = str(data).split()[0]
        recipient = str(data).split()[-1]


        if curious_click == recipient or curious_click == sender:
            await query.answer(
                data.replace(recipient, '').replace(sender, ''),
                show_alert=True,
                cache_time=1
            )
        else:
            await app.answer_callback_query(
                query.id, 
                "A mensagem não foi para você.", 
                show_alert=False)
    

# Parse the message
async def parse_whisper(sender, recipient, whisper):
    t = f'{sender} {whisper} {recipient}'
    return t


# Get inline user input and processes it
async def get_input(message: InlineQuery):
    dest = await get_sender_recipient(message)
    user = message.from_user.id
    special_id = database.get_new_id()
    recipient = dest[1]
    sender = dest[0]
    whisper = await parse_whisper(sender, recipient, message.query.replace(recipient, ''))

    text = f"Um susurro para {recipient}, só ele/ela pode revelar!"
    button = await create_button('Revelar!', special_id)

    result_id = hashlib.md5(message.query.encode()).hexdigest()

    result = InlineQueryResultArticle(
        id=result_id,
        title=f'Um susurro para {recipient}',
        input_message_content=InputTextMessageContent(text),
        reply_markup=button
    )

    await app.answer_inline_query(message.id, results=[result], cache_time=1)

    database.save_data(special_id, user, whisper)


async def start(message: Message) -> None:
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    bot_username = "@wmmsbot"
    text = f"Olá, {user_name}! Para enviar susurros é muito simples. Escreva o usuário do bot: {bot_username} + sua_mensagem + usuario alvo."

    await app.send_message(
        chat_id=chat_id,
        text=text,
    )


# Handler configuration
def setup_handlers(dispatcher: Dispatcher):
    dispatcher.register_inline_handler(get_input)
    dispatcher.register_callback_query_handler(manage_callback)
    dispatcher.register_message_handler(start, commands=['start'])


if __name__ == '__main__':
    app = Bot('') # INSERT TOKEN
    dp = Dispatcher(app)
    setup_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
