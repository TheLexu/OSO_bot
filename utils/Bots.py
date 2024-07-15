import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType


from utils.handlers import HelloHandler, MenuHandler, BasicHandler, CommandHandler
from utils.utils import Sender


class BasicBot(object):
    HELLO_WORDS = ['start', 'begin', 'начать', 'привет', 'добрый день', 'здравствуйте']

    def __init__(self, token):
        self.token = token
        self.handlers = [
            HelloHandler( trigger_phrases=self.HELLO_WORDS),
        ]
        self.default_handler = MenuHandler()

        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Привет', color=VkKeyboardColor.SECONDARY)
        self.basic_keyboard = keyboard

        vk_session = vk_api.VkApi(token=self.token)
        vk = vk_session.get_api()
        self.longpoll = VkLongPoll(vk_session)

        self.sender = Sender(vk)
        print('Connection established!')

    def start(self):

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()
                user_id = event.user_id
                resp_dict = {}
                for handler in self.handlers:
                    if isinstance(handler, BasicHandler) and text in handler.trigger_phrases:
                        resp_dict = handler.react(text)
                        break
                    if isinstance(handler, CommandHandler) and text in handler.commands:
                        resp_dict = handler.react(text)
                        break
                else:
                    resp_dict = self.default_handler.react(text, kb=self.basic_keyboard)
                print(resp_dict)
                self.sender(**resp_dict, user_id=user_id)
