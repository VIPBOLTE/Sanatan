async def harem(update: harem, context: CallbackContext, page=0, mode='all') -> None:
    user_id = update.effective_user.id

    user = await user_collection.find_one({'id': user_id})
    if not user:
        if update.message:
            await update.message.reply_text('You Have Not Guessed any Characters Yet..')
        else:
            await update.callback_query.edit_message_text('You Have Not Guessed any Characters Yet..')
        return

    characters = sorted(user['characters'], key=lambda x: (x['anime'], x['id']))

    character_counts = {k: len(list(v)) for k, v in groupby(characters, key=lambda x: x['id'])}

    unique_characters = list({character['id']: character for character in characters}.values())

    if mode != 'all':
        unique_characters = [character for character in unique_characters if character['rarity'] == mode]

    total_pages = math.ceil(len(unique_characters) / 15)

    if page < 0 or page >= total_pages:
        page = 0  

    harem_message = f"<b>{escape(update.effective_user.first_name)}'s Harem - Page {page+1}/{total_pages}</b>\n"

    current_characters = unique_characters[page*15:(page+1)*15]

    current_grouped_characters = {k: list(v) for k, v in groupby(current_characters, key=lambda x: x['anime'])}

    for anime, characters in current_grouped_characters.items():
        harem_message += f'\n<b>{anime} {len(characters)}/{await collection.count_documents({"anime": anime})}</b>\n'

        for character in characters:
            count = character_counts[character['id']]  
            harem_message += f'{character["id"]} {character["name"]} ×{count}\n'

    total_count = len(user['characters'])

    keyboard = [[InlineKeyboardButton(f"See Collection ({total_count})", switch_inline_query_current_chat=f"collection.{user_id}")]]

    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"harem:{page-1}:{user_id}:{mode}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"harem:{page+1}:{user_id}:{mode}"))
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        callback_query = update.callback_query
    else:
        callback_query = update

    if 'favorites' in user and user['favorites']:
        fav_character_id = user['favorites'][0]
        fav_character = next((c for c in user['characters'] if c['id'] == fav_character_id), None)

        if fav_character and 'img_url' in fav_character:
            await callback_query.message.reply_photo(photo=fav_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
        else:
            await callback_query.message.reply_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
    else:
        if user['characters']:
            random_character = random.choice(user['characters'])
            if 'img_url' in random_character:
                await callback_query.message.reply_photo(photo=random_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
            else:
                await callback_query.message.reply_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
        else:
            await callback_query.message.reply_text("Your List is Empty :)")


async def harem_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    _, page, user_id, mode = data.split(':')

    page = int(page)
    user_id = int(user_id)

    if query.from_user.id != user_id:
        await query.answer("its Not Your Harem", show_alert=True)
        return

    await harem(update, context, page, mode)


application.add_handler(CommandHandler(["harem", "collection"], harem, pass_args=True, pass_job_queue=True, pass_chat_data=True, pass_user_data=True))
harem_handler = CallbackQueryHandler(harem_callback, pattern='^harem', pass_update_queue=True, pass_job_queue=True, pass_chat_data=True, pass_user_data=True)
application.add_handler(harem_handler)
