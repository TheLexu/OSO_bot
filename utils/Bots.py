import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from utils.utils import Sender


class BasicBot(object):
    HELLO_WORDS = ('start', 'begin', 'начать', 'привет', 'добрый день', 'здравствуйте')

    def __init__(self, token):
        self.token = token

    def start(self):

        vk_session = vk_api.VkApi(token=self.token)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        sender = Sender(vk)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()
                user_id = event.user_id

                if text in self.HELLO_WORDS:
                    sender('Добро пожаловать в ОСО!', user_id=user_id)
                else:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Привет', color=VkKeyboardColor.SECONDARY)
                    keyboard.add_button('Здравствуйте', color=VkKeyboardColor.NEGATIVE)
                    sender('Привет!',
                           user_id=user_id,
                           keyboard=keyboard.get_keyboard())
