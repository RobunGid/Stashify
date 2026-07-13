# Naming 

## Handlers

All aiogram message handlers must be named using the `_message_handler` suffix 

Correct:

- `menu_command_message_handler`

Incorrect:

- `handle_menu_command_message`

<hr>

All aiogram callback handlers must be named using the `_callback_handler` suffix 

Correct:

- `menu_callback_handler`

Incorrect:

- `handle_menu_callback`

<hr>

All entry handlers must be named using the `_entry_` prefix

Correct:

- `manage_quizes_entry_callback_handler`

Incorrect:

- `entry_manage_quizes_callback_handler`
- `entry_to_manage_quizes_callback_handler`