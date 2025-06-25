from balethon import Client
from balethon.conditions import private, equals
from balethon.objects import InlineKeyboard
from balethon.objects import ReplyKeyboard
from balethon.conditions import new_chat_members
from balethon.conditions import at_state

bot = Client("881675094:7hgLMFULihpqwy5LCHoXG3YAOtX7rpJ7z5etxVhz")  # Replace "TOKEN" with your actual token here



# @bot.on_message()
# async def greet(message):
#     await message.reply("سلام")
#     print(message)
   
@bot.on_message(new_chat_members)
async def welcome_new_chat_members(message):
    members = [member.full_name for member in message.new_chat_members]
    await message.reply(
        f"Hello {', '.join(members)}, welcome to {message.chat.title}!"
    )
       
@bot.on_message(private & equals("Button 1", "Button 2"))
async def answer_buttons(message):
    await message.reply(
        f"Thank you for clicking on button {message.text}"
    )
   
# @bot.on_message(private)
# async def answer_message(message):
#     await message.reply(
#         "Click a button!",
#         ReplyKeyboard(
#             ["Button 1"],
#             ["Button 2"]
#         )
#     )   

# @bot.on_message(private)
# async def answer_message(message):
#     await message.reply(
#         "Click a button!",
#         InlineKeyboard(
#             [("Button 1", "1")],
#             [("Button 2", "2")]
#         )
#     )

@bot.on_callback_query()
async def answer_callback_query(callback_query):
    await callback_query.answer(
        f"Thank you for clicking on button {callback_query.data}"
    )
     
     
@bot.on_message(at_state(None))
async def home_state(message):
    await message.reply(
        "Hello, I'm the conversation bot\nWhat is your name?"
    )
    message.author.set_state("NAME")


@bot.on_message(at_state("NAME"))
async def name_state(message):
    name = message.text
    await message.reply(
        f"Nice to meet you, {name}!\nHow old are you?"
    )
    message.author.set_state("AGE")


@bot.on_message(at_state("AGE"))
async def age_state(message):
    age = message.text
    await message.reply(
        f"You are {age} years old, good for you!\nHave a nice day!"
    )
    message.author.del_state()
    
            
bot.run()






