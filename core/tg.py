import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler

from core.models import Profile, EventType, Slot

TOKEN = os.environ.get('TOKEN')

CHOOSE_EVENT, CHOOSE_SLOT = range(2)


async def start(update: Update, _) -> int:
    profile, created = await Profile.objects.aget_or_create(tg_id=update.effective_user.id)
    print(f'Start for {profile}')

    keyboard = [
        [InlineKeyboardButton(text=event.name, callback_data=event.id), ]
        async for event in EventType.objects.aiterator()
    ]

    text = 'Привет! Выбери услугу:'
    await update.effective_chat.send_message(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_EVENT


async def chosen_event(update: Update, _) -> int:
    profile, created = await Profile.objects.aget_or_create(tg_id=update.effective_user.id)
    print(f'Chosen event for {profile}')

    data = int(update.callback_query.data)

    event = await EventType.objects.aget(pk=data)

    keyboard = [
        [InlineKeyboardButton(text=slot.time_of_event.strftime('%H:%M %d.%m.%Y'), callback_data=slot.id), ]
        async for slot in Slot.objects.filter(type_of_event=event, status=Slot.Status.FREE).aiterator()
    ]

    text = f'{event.name}\n\n{event.description}\n\nВыбери удобное время: '
    await update.effective_message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_SLOT


async def chosen_slot(update: Update, _) -> int:
    profile, created = await Profile.objects.aget_or_create(tg_id=update.effective_user.id)
    print(f'Chosen slot for {profile}')

    data = int(update.callback_query.data)
    slot = await Slot.objects.aget(pk=data)
    slot.reserved_by = profile
    slot.status = slot.Status.RESERVED
    await slot.asave()

    text = (f'Готово! Вы выбрали время: {slot.time_of_event.strftime('%H:%M %d.%m.%Y')}.'
            f' Администратор с вами свяжется. Всего доброго!')
    await update.effective_message.edit_text(text, reply_markup=None)
    return ConversationHandler.END


main_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start), ],
    states={
        CHOOSE_EVENT: [CallbackQueryHandler(chosen_event, pattern=r'\d+')],
        CHOOSE_SLOT: [CallbackQueryHandler(chosen_slot, pattern=r'\d+')]
    },
    fallbacks=[],
    allow_reentry=True,
)


def get_app():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(main_handler)

    return app
