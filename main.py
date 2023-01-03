# -*- coding: utf-8 -*-

import constants as keys
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import responses as R
from datetime import datetime


print("Bot started...")

today = datetime.now()

def start_command(update, context):
  update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())


def main_menu(update, context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
      text=main_menu_message(),
      reply_markup=main_menu_keyboard())

############################ Keyboards #########################################

def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Expenses', callback_data='expense'),
              InlineKeyboardButton('Incomes', callback_data='income'),
              InlineKeyboardButton('Help', callback_data='help')]]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################

def main_menu_message():
  return 'Choose the option in main menu:'


def help_command(update, context):
  update.message.reply_text('This bot will help you calculate all your expenses and incomes per month.')
  update.message.reply_text('Example of add a new expense: 20/12/2022 - 200 food,apple')

def expenses_menu(update, context):
  user_id = update.callback_query.message.chat.id
  expenses = R.get_expenses_by_month(user_id)
  response_message = 'In <b>' + today.strftime("%B %Y") + "</b > you earned:\n\n № | day | amount | categories \n"
  sum_amount = 0
  for count, expense in enumerate(expenses, start=1):
    response_message = response_message + \
        ' ' + str(count).ljust(6, ' ') + expense[0].strftime("%-d").ljust(7, ' ') + \
        str(expense[1]).ljust(9, ' ') + ' ' + ', '.join(expense[2]) + ' \n'
    sum_amount += expense[1]
  response_message += "\nThe sum of all expenses <b>₴" + \
      str(sum_amount) + "</b>."
  update.callback_query.message.reply_text(response_message, parse_mode='HTML')

def expenses_command(update, context):
  user_id = update.message.chat.id
  expenses = R.get_expenses_by_month(user_id)
  response_message = 'In <b>' + today.strftime("%B %Y") + "</b > you spent:\n\n № | day | amount | categories \n"
  sum_amount = 0
  for count, expense in enumerate(expenses, start=1):
    response_message = response_message + \
        ' ' + str(count).ljust(6, ' ') + expense[0].strftime("%-d").ljust(7, ' ') + \
        str(expense[1]).ljust(9, ' ') + ' ' + ', '.join(expense[2]) + ' \n'
    sum_amount += expense[1]
  response_message += "\nThe sum of all expenses <b>₴" + \
      str(sum_amount) + "</b>."
  update.message.reply_text(response_message, parse_mode='HTML')

def incomes_menu(update, context):
  if hasattr(update.message, 'chat'):
    user_id = update.message.chat.id
    amount = R.get_incomes_by_month(user_id)
    update.callback_query.message.reply_text(
        'In ' + today.strftime("%B %Y") + " you earned ₴" + str(amount) + ".")
    if amount > 0:
      update.callback_query.message.reply_text(
          "Save from this sum <b>10%</b> on the deposit on a rainy day, it\'s <b>₴" + str(int(amount * 0.1)) + "</b>.", parse_mode='HTML')
  else:
     print("Failed to execute command")

def incomes_command(update, context):
  print('context',context)
  if hasattr(update.message, 'chat'):
    user_id = update.message.chat.id
  else: #hasattr(update.callback_query.message, 'chat'):
    user_id = update.callback_query.message.chat.id
  amount = R.get_incomes_by_month(user_id)
  update.callback_query.message.reply_text(
      'In ' + today.strftime("%B %Y") + " you earned ₴" + str(amount) + ".")
  if amount > 0:
    update.callback_query.message.reply_text(
        "Save from this sum <b>10%</b> on the deposit on a rainy day, it\'s <b>₴" + str(int(amount * 0.1)) + "</b>.", parse_mode='HTML')

def handle_message(update, context):
  text = str(update.message.text).lower()
  user_id = update.message.chat.id
  response = R.sample_responses(text, user_id)
  update.message.reply_text(response, parse_mode='HTML')

def error(update, context):
  print(f"Update {update} caused error {context.error}")

def main():
  updater = Updater(keys.API_KEY, use_context=True)
  dp = updater.dispatcher
  dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
  dp.add_handler(CommandHandler("start", start_command))
  dp.add_handler(CommandHandler("help", help_command))
  dp.add_handler(CommandHandler("expenses", expenses_command))
  dp.add_handler(CommandHandler("incomes", incomes_command))
  dp.add_handler(CallbackQueryHandler(expenses_menu, pattern="expense"))
  dp.add_handler(CallbackQueryHandler(incomes_command, pattern="income"))

  dp.add_handler(MessageHandler(Filters.text, handle_message))

  dp.add_error_handler(error)

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
    main()
