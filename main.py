import constants as keys
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import responses as R
from datetime import datetime, timedelta, date


print("Bot started...")

today = datetime.now()
start_date = today.replace(day=1)
end_date = date(start_date.year + int(start_date.month/12),
                start_date.month % 12+1, 1) - timedelta(days=1)

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
  keyboard = [[InlineKeyboardButton('Expenses', callback_data='expenses'),
              InlineKeyboardButton('Incomes', callback_data='incomes'),
              InlineKeyboardButton('Help', callback_data='help')]]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################

def main_menu_message():
  return 'Choose the option in main menu:'


def help_command(update, context):
  update.message.reply_text("""This bot will help you calculate all your expenses and incomes per month.
Example of adding a new expense in 20 December 2022:
<b>20/12/2022 - 200 food,apple</b>
Example of adding a new income in the current day:
<b>+ 1000 work,olx,repair</b>""", parse_mode='HTML')

def expenses_menu(update, context):
  user_id = update.callback_query.message.chat.id
  expenses = R.get_expenses_by_month(user_id,
                                     start_date.strftime("%Y-%m-%d"),
                                     end_date.strftime("%Y-%m-%d"))
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
  if hasattr(update.message, 'chat'):
    user_id = update.message.chat.id
    expenses = R.get_expenses_by_month(user_id,
                                       start_date.strftime("%Y-%m-%d"),
                                       end_date.strftime("%Y-%m-%d"))
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
  else:
    print("Failed to execute command.")

def prev_expenses_command(update, context):
  if hasattr(update.message, 'chat'):
    user_id = update.message.chat.id
    end_date = today.replace(day=1)-timedelta(days=1)
    start_date = end_date.replace(day=1)
    expenses = R.get_expenses_by_month(user_id,
                                       start_date.strftime("%Y-%m-%d"),
                                       end_date.strftime("%Y-%m-%d"))
    response_message = 'In <b>' + \
        start_date.strftime(
            "%B %Y") + "</b > you spent:\n\n № | day | amount | categories \n"
    sum_amount = 0
    for count, expense in enumerate(expenses, start=1):
      response_message = response_message + \
          ' ' + str(count).ljust(6, ' ') + expense[0].strftime("%-d").ljust(7, ' ') + \
          str(expense[1]).ljust(9, ' ') + ' ' + ', '.join(expense[2]) + ' \n'
      sum_amount += expense[1]
    response_message += "\nThe sum of all expenses <b>₴" + \
        str(sum_amount) + "</b>."
    update.message.reply_text(response_message, parse_mode='HTML')
  else:
    print("Failed to execute command.")

def incomes_menu(update, context):
  if hasattr(update.callback_query.message, 'chat'):
    user_id = update.callback_query.message.chat.id
    incomes = R.get_incomes_by_month(user_id,
                                     start_date.strftime("%Y-%m-%d"),
                                     end_date.strftime("%Y-%m-%d"))
    if not incomes:
      update.callback_query.message.reply_text(
          "You did not earn anything in the current month. Get up your but and make some money!")
    else:
      response_message = 'In <b>' + \
          today.strftime("%B %Y") + \
          "</b > you spent:\n\n № | day | amount | categories \n"
      sum_amount = 0
      for count, income in enumerate(incomes, start=1):
        response_message = response_message + \
            ' ' + str(count).ljust(6, ' ') + income[0].strftime("%-d").ljust(7, ' ') + \
            str(income[1]).ljust(9, ' ') + ' ' + ', '.join(income[2]) + ' \n'
        sum_amount += income[1]
      response_message += "\nThe sum of all incomes <b>₴" + \
          str(sum_amount) + "</b>."
      update.callback_query.message.reply_text(
          response_message, parse_mode='HTML')
      update.callback_query.message.reply_text(
            "Save from this sum <b>10%</b> on the deposit on a rainy day, it\'s <b>₴" + str(int(sum_amount * 0.1)) + "</b>.", parse_mode='HTML')
  else:
     print("Failed to execute "+str(update.message)+" command.")

def incomes_command(update, context):
  if hasattr(update.message, 'chat'):
    user_id = update.message.chat.id
    incomes = R.get_incomes_by_month(user_id,
                                     start_date.strftime("%Y-%m-%d"),
                                     end_date.strftime("%Y-%m-%d"))
    # it could be an empty array if it is a new month
    if not incomes:
      update.message.reply_text(
          "You did not earn anything in the current month. Get up your but and make some money!")
    else:
      sum_amount = 0
      response_message = 'In <b>' + \
          today.strftime("%B %Y") + \
          "</b > you earned:\n\n № | day | amount | categories \n"
      for count, income in enumerate(incomes, start=1):
        response_message = response_message + \
            ' ' + str(count).ljust(6, ' ') + income[0].strftime("%-d").ljust(7, ' ') + \
            str(income[1]).ljust(9, ' ') + ' ' + ', '.join(income[2]) + ' \n'
        sum_amount += income[1]
      response_message += "\nThe sum of all incomes <b>₴" + \
          str(sum_amount) + "</b>."
      update.message.reply_text(response_message, parse_mode='HTML')
      update.message.reply_text(
          "Save from this sum <b>10%</b> on the deposit on a rainy day, it\'s <b>₴" + str(int(sum_amount * 0.1)) + "</b>.", parse_mode='HTML')
  else:
    print("Failed to execute "+update.message+" command.")

def prev_incomes_command(update, context):
  if hasattr(update.message, 'chat'):
    user_id = update.message.chat.id
    end_date = today.replace(day=1)-timedelta(days=1)
    start_date = end_date.replace(day=1)
    incomes = R.get_incomes_by_month(user_id,
                                     start_date.strftime("%Y-%m-%d"),
                                     end_date.strftime("%Y-%m-%d"))

# it could be an empty array if it is a new month
    if not incomes:
      update.message.reply_text(
          "You did not earn anything in the current month. Get up your but and make some money!")
    else:
      sum_amount = 0
      response_message = 'In <b>' + \
          start_date.strftime("%B %Y") + \
          "</b > you earned:\n\n № | day | amount | categories \n"
      for count, income in enumerate(incomes, start=1):
        response_message = response_message + \
            ' ' + str(count).ljust(6, ' ') + income[0].strftime("%-d").ljust(7, ' ') + \
            str(income[1]).ljust(9, ' ') + ' ' + ', '.join(income[2]) + ' \n'
        sum_amount += income[1]
      response_message += "\nThe sum of all incomes <b>₴" + \
          str(sum_amount) + "</b>."
      update.message.reply_text(response_message, parse_mode='HTML')
      update.message.reply_text(
          "You were should save  <b>10%</b> ten percent of this sum on a rainy day, it\'s <b>₴" + str(int(sum_amount * 0.1)) + "</b>.", parse_mode='HTML')
  else:
    print("Failed to execute "+update.message+" command.")

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
  dp.add_handler(CommandHandler("prev_incomes", prev_incomes_command))
  dp.add_handler(CommandHandler("prev_expenses", prev_expenses_command))
  dp.add_handler(CallbackQueryHandler(expenses_menu, pattern="expenses"))
  dp.add_handler(CallbackQueryHandler(incomes_menu, pattern="incomes"))

  dp.add_handler(MessageHandler(Filters.text, handle_message))

  dp.add_error_handler(error)

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
    main()
