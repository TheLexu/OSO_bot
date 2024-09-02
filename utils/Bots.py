import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from utils.utils import Sender

qa_file = 'qa_pairs.json'
events_file = 'events.json'
class BasicBot(object):
    HELLO_WORDS = ('start', 'begin', 'начать', 'привет', 'добрый день', 'здравствуйте')

    def load_qa_pairs(self, qa_file):
        with open(qa_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def load_events(self, events_file):
        with open(events_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_response(self, user_question):
        user_question = user_question.strip().lower()
        response = self.qa_pairs.get(user_question, "Извините, я не понимаю вопрос.")
        return response

    def get_events_by_community(self, community_name):
        events = []
        for event in self.events:
            if event['Community'].lower() == community_name.lower():
                events.append("Мероприятие: {event['Event']} - Дата: {event['Date']}")
        return events
    def start(self):
        vk_session = vk_api.VkApi(token=self.token)
        longpoll = VkLongPoll(vk_session)
        sender = Sender(vk_session.get_api())

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()
                user_id = event.from_id

                if text in self.HELLO_WORDS:
                    sender(
                        'Привет! Я - ВК бот ОСО, я помогу тебе ответить на твой интересующий вопрос по поводу объединений, а также назвать мероприятия, которые будут у того или иного сообщества.',
                        user_id=user_id)
                else:
                    answer = self.get_response(text)
                    if answer == "Извините, я не понимаю вопрос.":
                        events = self.get_events_by_community(text)
                        if events:
                            response = "\n".join(events)
                        else:
                            response = "Мероприятия не найдены. Пожалуйста, уточните название сообщества."

                        sender(response, user_id=user_id)
                    else:
                        sender(answer, user_id=user_id)

