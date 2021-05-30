from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile
from telebot.types import CallbackQuery
import re
from config import edit_config, link_regex
from data.functions.db import get_user, update_balance, change_spinup_status, get_all_users
from filters.filters import IsAdmin
from keyboards.inline.admin_menu_keyboards import admin_mailing_menu_keyboard, admin_settings_keyboard, \
    admin_back_keyboard, admin_menu_keyboard, admin_search_user_keyboard
from keyboards.inline.callback_datas import admin_search_user_callback
from keyboards.inline.games_keyboard import understand_keyboard
from loader import dp, bot
from states.states import AdminSearchUserState, AdminChangeBalance, AdminChangeComission, AdminPictureMailing, \
    AdminWithoutPictureMailing
from texts import admin_search_user_text, admin_statistic_text


@dp.callback_query_handler(IsAdmin(), text_contains="admin:mailing_menu")
async def admin_mailing_menu(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Управление рассылками",
                                reply_markup=admin_mailing_menu_keyboard())


@dp.callback_query_handler(IsAdmin(), text_contains="admin:statistic")
async def admin_statistic(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=admin_statistic_text(),
                                reply_markup=admin_back_keyboard())


@dp.callback_query_handler(IsAdmin(), text_contains="admin:settings")
async def admin_settings(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Найстройки",
                                reply_markup=admin_settings_keyboard())


@dp.callback_query_handler(IsAdmin(), text_contains="admin:back_to_main")
async def back_to_admin_main(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Админ меню",
                                reply_markup=admin_menu_keyboard())


@dp.callback_query_handler(IsAdmin(), text_contains="admin:search_user")
async def admin_search_user_1(call: CallbackQuery):
    await call.message.answer(text="Введите ID пользователя.")
    await AdminSearchUserState.user_id.set()


@dp.message_handler(IsAdmin(), state=AdminSearchUserState.user_id)
async def admin_search_user_2(message: Message, state: FSMContext):
    if message.text.isdigit():
        if get_user(message.text) != None:
            await message.answer(text=admin_search_user_text(get_user(message.text)),
                                 reply_markup=admin_search_user_keyboard(message.text))
        else:
            await message.answer(text="Пользователь не найден в базе данных.")
    else:
        await message.answer(text="Неверный ввод.")
    await state.finish()


@dp.callback_query_handler(IsAdmin(), admin_search_user_callback.filter(action="change_balance"))
async def admin_change_balance(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data["user_id"]
    async with state.proxy() as data:
        data["user_id"] = user_id
    await call.message.answer("Введите сумму на которую хотите изменить баланс")
    await AdminChangeBalance.amount.set()


@dp.message_handler(IsAdmin(), state=AdminChangeBalance.amount)
async def admin_admin_change_balance_2(message: Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            user_id = data["user_id"]
            data["amount"] = int(message.text)
        await message.answer(text=f"Баланс пользователя <b>{user_id}</b> изменится на <b>{message.text} RUB</b>\n\n"
                                  f"Для подтвреждения действия отправьте <b>+</b>", )
        await AdminChangeBalance.next()
    else:
        await message.answer(text="Неверный ввод.")
        await state.finish()


@dp.message_handler(IsAdmin(), state=AdminChangeBalance.confitm)
async def admin_admin_change_balance_2(message: Message, state: FSMContext):
    if message.text == "+":
        async with state.proxy() as data:
            user_id = data["user_id"]
            amount = data["amount"]
        update_balance(user_id, amount, add=False)
        await message.answer(text="✅ Баланс успешно изменён.")
    else:
        await message.answer(text="Смена баланса отменена.")
    await state.finish()


@dp.callback_query_handler(IsAdmin(), admin_search_user_callback.filter(action="on_spinup"))
async def admin_change_balance(call: CallbackQuery, callback_data: dict):
    user_id = callback_data["user_id"]
    if get_user(user_id)[2] == "False":
        change_spinup_status(user_id, "True")
        await call.message.answer("✅ Подкуртка успешно включена.")
    else:
        await call.message.answer("Подкуртка уже включена.")


@dp.callback_query_handler(IsAdmin(), admin_search_user_callback.filter(action="off_spinup"))
async def admin_change_balance(call: CallbackQuery, callback_data: dict):
    user_id = callback_data["user_id"]
    if get_user(user_id)[2] == "True":
        change_spinup_status(user_id, "False")
        await call.message.answer("✅ Подкуртка успешно выключена.")
    else:
        await call.message.answer("Подкуртка уже выключена.")


@dp.callback_query_handler(IsAdmin(), text_contains="admin:change_markup_percent")
async def admin_change_markup_percent(call: CallbackQuery):
    await call.message.answer(text="Введите новый процент комиссии с игр.")
    await AdminChangeComission.percent.set()


@dp.message_handler(IsAdmin(), state=AdminChangeComission.percent)
async def admin_change_markup_percent_2(message: Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) >= 0:
            async with state.proxy() as data:
                data["percent"] = int(message.text)
            await message.answer(text=f"Процент комисси изменится на <b>{message.text}%</b>\n\n"
                                      f"Для подтвреждения действия отправьте <b>+</b>", )
            await AdminChangeComission.next()
        else:
            await message.answer(text="Процент не может быть отрицательным.")
            await state.finish()
    else:
        await message.answer(text="Неверный ввод.")
        await state.finish()


@dp.message_handler(IsAdmin(), state=AdminChangeComission.confitm)
async def admin_admin_change_balance_2(message: Message, state: FSMContext):
    if message.text == "+":
        async with state.proxy() as data:
            percent = data["percent"]
        edit_config("game_percent", str(percent))
        await message.answer(text="✅ Процент комиссии успешно изменён.")
    else:
        await message.answer(text="Смена процента комиссии отменена.")
    await state.finish()


@dp.callback_query_handler(IsAdmin(), text_contains="admin:mailing_with_picture")
async def mailing_with_picture(call: CallbackQuery):
    await call.message.answer(text="Введите текст рассылки.")
    await AdminPictureMailing.text.set()


@dp.callback_query_handler(IsAdmin(), text_contains="admin:mailing_without_picture")
async def mailing_without_picture(call: CallbackQuery):
    await call.message.answer(text="Введите текст рассылки.")
    await AdminWithoutPictureMailing.text.set()


@dp.message_handler(IsAdmin(), state=AdminWithoutPictureMailing.text)
async def mailing_without_picture_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await bot.send_message(chat_id=message.chat.id,
                           text="<i>Введите <b>+</b> для запуска рассылки!</i>")

    await AdminWithoutPictureMailing.next()


@dp.message_handler(IsAdmin(), state=AdminWithoutPictureMailing.confirm)
async def mailing_without_picture_2(message: Message, state: FSMContext):
    answer = message.text
    if answer == "+":
        async with state.proxy() as data:
            text = data["text"]
        await state.finish()
        await bot.send_message(chat_id=message.chat.id,
                               text="<b>Рассылка запущена!</b>")
        errors = 0
        good = 0
        users = get_all_users()
        for user in users:
            try:
                await bot.send_message(chat_id=user[0],
                                       text=text,
                                       reply_markup=understand_keyboard(),
                                       disable_web_page_preview=True)
                good += 1
            except:
                errors += 1
        await bot.send_message(chat_id=message.chat.id,
                               text="✅ Рассылка завершена!\n\n"
                                    f"❗️ Отправлено: {good}\n"
                                    f"❗️ Не отправлено: {errors}\n")
    else:
        await bot.send_message(chat_id=message.chat.id, text="<b>❗️Рассылка отменена.</b>")
        await state.finish()


@dp.message_handler(IsAdmin(), state=AdminPictureMailing.text)
async def mailing_with_picture(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await bot.send_message(chat_id=message.chat.id,
                           text="<i>Отправтьте ссылку на фотографию которую хотите отправить. Загрузить фото можно тут @imgurbot_bot!</i>")

    await AdminPictureMailing.next()


@dp.message_handler(IsAdmin(), state=AdminPictureMailing.picture)
async def mailing_with_picture_2(message: Message, state: FSMContext):
    answer = re.search(link_regex, message.text)
    if answer:
        async with state.proxy() as data:
            data["picture"] = message.text
        await bot.send_message(chat_id=message.chat.id,
                         text="<i>Введите <b>+</b> для запуска рассылки!</i>")

        await AdminPictureMailing.next()
    else:
        await bot.send_message(chat_id=message.chat.id,
                         text="<b>Вы не отправили ссылку. Рассылка отменена.</b>")
        await state.finish()


@dp.message_handler(IsAdmin(), state=AdminPictureMailing.confirm)
async def mailing_with_picture_3(message: Message, state: FSMContext):
    async with state.proxy() as data:
        text = data["text"]
        picture = data["picture"]
    await state.finish()
    answer = message.text
    if answer == "+":
        await bot.send_message(chat_id=message.chat.id,
                               text="<b>Рассылка запущена!</b>")
        errors = 0
        good = 0
        users = get_all_users()
        for user in users:
            try:
                await bot.send_photo(chat_id=user[0],
                                     photo=InputFile.from_url(picture),
                                     caption=text,
                                     reply_markup=understand_keyboard())
                good += 1
            except Exception as e:
                errors += 1
        await bot.send_message(chat_id=message.chat.id,
                               text="✅Рассылка завершена!\n\n"
                                    f"❗️Отправлено: {good}\n"
                                    f"❗️Не отправлено: {errors}\n")
    else:
        await bot.send_message(chat_id=message.chat.id, text="<b>❗ Рассылка отменена</b>")
