from aiogram.utils.callback_data import CallbackData

game_callback = CallbackData("games", "game_name", "action")
game_info_callback = CallbackData("games", "game_name", "action", "game_id")
other_game_callback = CallbackData("games", "game_name", "action", "game_type")
admin_search_user_callback = CallbackData("admin", "action", "user_id")
