import json
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
#1
qa_file = 'qa_pairs.json'

class BasicBot(object):
    HELLO_WORDS = ('start', 'begin', 'начать', 'привет', 'добрый день', 'здравствуйте')

    def __init__(self, token, qa_file):
        self.token = token
        self.qa_pairs = self.load_qa_pairs(qa_file)

    def load_qa_pairs(self, qa_file):
        with open(qa_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_response(self, user_question):
        user_question = user_question.strip().lower()
        response = self.qa_pairs.get(user_question, "Извините, я не понимаю вопрос.")
        return response


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
                    answer = self.get_response(text)
                    sender(answer, user_id=user_id)
