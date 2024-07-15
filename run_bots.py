from env import OSO_APP_VK_TOKEN as token

from utils import Bots

if __name__ == '__main__':
    basic_bot = Bots.BasicBot(token=token)

    basic_bot.start()
