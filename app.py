import os

import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bs4 import BeautifulSoup

BOT_NAME = '@WebscraperBot'

app = Client(
  BOT_NAME,
  bot_token = os.environ['BOT_TOKEN'],
  api_id = int(os.environ['API_ID']),
  api_hash = os.environ['API_HASH']
  )

# commands

def write_file(filename, data):
  loading_text = 'Processing data for "{}"'.format(filename)
  with open(filename, mode='a+', encoding='utf-8') as f:
    f.write(request.content)    
  await message.reply_document(filename, caption=BOT_NAME, quote=True)
  os.remove(filename)
  await loading_text.delete()

@app.on_message(filters.command['start'])
async def start(_, message: Message):
  intro_text = '''
               Hello {update.from_user.mention}, I am a webscraping robot. \n
               Send me a link to scrape.
               '''
  await message.reply_text(text=intro_text, disable_web_page_preview=True, quote=True)

@app.on_message(filters.regex('https') | filters.regex('http') | filters.regex('www') & filters.private)
async def scrape(bot, message):
  loading_text = await message.reply_text('Validating link...', quote=True)

  # get raw data
  try:
    url = str(message.text)
    request = requests.get(url)
    await loading_text.edit(text='Getting raw data from {}'.format(url), disable_web_page_preview=True)
    raw_filename = ''.join('Raw_data-', message.chat.username, '.txt')
    write_file(raw_filename, request.content)
  except Exception as e:
    print(e)
    await message.reply_text(text=e, disable_web_page_preview=True, quote=True)
    await loading_text.delete()
    return

  # get html data
  try:
    loading_text = await message.reply_text(text='Getting HTML code from {}'.format(url), disable_web_page_preview=True, quote=True)
    soup = BeautifulSoup(request.content, 'html5lib')
    soup_data = soup.prettify()
    html_filename = ''.join('HTML_data-', message.chat.username, '.txt')
    write_file(html_filename, soup_data)
  except Exception as e:
    await message.reply_text(text=e, disable_web_page_preview=True, quote=True)
    await loading_text.delete()

  # get links
  try:
    loading_text = await message.reply_text(text='Getting links from {}'.format(url), disable_web_page_preview=True, quote=True)
    tags = soup.find_all('a')
    link_filename = ''.join('Link_data-', message.chat.username, '.txt')
    for tag in tags:
      link = tag.get('href')
      write_file(link_filename, link)
  except Exception as e:    

app.run()
