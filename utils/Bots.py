import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from utils.utils import Sender


class BasicBot(object):
    HELLO_WORDS = ('start', 'begin', 'начать', 'привет', 'добрый день', 'здравствуйте')
    qa_pairs = {
        "Кто является руководителем кружка?": "Шлапак Никита (ссылка на вк)",
        "Чем занимается кружок?": "Деятельность кружка делится на три основных направления: изучение архитектуры компьютеров, внутренние проекты института и научно-исследовательская деятельность",
        "Какой входной порог?": "Зависит от направления. Для курса Computer Science и внутренних проектов института необходимы базовые знания программирования. Для исследовательского направления уже необходимо уверенно владеть языком программирования",
        "Когда и где проходят занятия?": "Кружок функционирует онлайн. Вся коммуникация (в том числе и актуальное расписание занятий) происходит на дискорд-сервере: ссылка"
    }
    def __init__(self, token):
        self.token = token

    def get_response(self, user_question):
        user_question = user_question.strip().lower()
        if user_question in self.qa_pairs:
            return self.qa_pairs[user_question]
        else:
            return 'Извините, я не понимаю вашего вопроса'
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
                    if answer == 'Извините, я не понимаю вашего вопроса':
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('Привет', color=VkKeyboardColor.SECONDARY)
                        keyboard.add_button('Здравствуйте', color=VkKeyboardColor.NEGATIVE)
                        sender('Привет!',
                               user_id=user_id,
                               keyboard=keyboard.get_keyboard())
