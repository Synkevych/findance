import constants as keys
from telegram.ext import *
import responses as R
from datetime import datetime


print("Bot started...")

today = datetime.now()

def start_command(update, context):
  update.message.reply_text('Type something to get started!')

def help_command(update, context):
  update.message.reply_text('This bot will help you calculate all your expenses and incomes per month.')
  update.message.reply_text('Example of add a new expense: 20/12/2022 - 200 food,apple ATB')

def expense_command(update, context):
  user_id = update.message.chat.id
  amount = R.get_expenses_by_month(user_id)
  update.message.reply_text(
      'In <b>' + today.strftime("%B %Y") + "</b> you spent <b>₴" + str(int(amount)) + "</b>.", parse_mode='HTML')

def income_command(update, context):
  user_id = update.message.chat.id
  amount = R.get_incomes_by_month(user_id)
  update.message.reply_text(
      'In ' + today.strftime("%B %Y") + " you earned ₴" + str(amount) + ".")
  if amount > 0:
    update.message.reply_text(
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

  dp.add_handler(CommandHandler("start", start_command))
  dp.add_handler(CommandHandler("help", help_command))
  dp.add_handler(CommandHandler("expense", expense_command))
  dp.add_handler(CommandHandler("income", income_command))

  dp.add_handler(MessageHandler(Filters.text, handle_message))

  dp.add_error_handler(error)

  updater.start_polling()
  updater.idle()

main()