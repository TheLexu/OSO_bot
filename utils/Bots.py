import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
#1
qa_pairs = {
    "Кто является руководителем кружка?": "Шлапак Никита (ссылка на вк)",
    "Чем занимается кружок?": "Деятельность кружка делится на три основных направления: изучение архитектуры компьютеров, внутренние проекты института и научно-исследовательская деятельность",
    "Какой входной порог?": "Зависит от направления. Для курса Computer Science и внутренних проектов института необходимы базовые знания программирования. Для исследовательского направления уже необходимо уверенно владеть языком программирования",
    "Когда и где проходят занятия?": "Кружок функционирует онлайн. Вся коммуникация (в том числе и актуальное расписание занятий) происходит на дискорд-сервере: ссылка"
}


def get_response(user_question):
    user_question = user_question.strip()
    response = qa_pairs.get(user_question, "Извините, я не понимаю вопрос.")
    return response


def main():
    TOKEN = 'vk1.a.twQWhoQKZLg1EGRKrHwX6gyAQTt5FW55JaIE7wTvFWRHa9CWsv9g2HKHhRi9RSZdVR_8UohJ0J-nw1Pma-wekbjojIPkP8w4zSXbRFVmS8UwyMg-jtI-WgH2aJzNBLIImJjPv0Pyz0jf-pYAkye0aoBVFhKK7nRdSPJeR-RGK-cvWan-2hKcn-9BCCAJsRDsaoBjuFOv9OroQmEcITHhtQ'
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_input = event.text
            answer = get_response(user_input)

            vk_session.method('messages.send', {'user_id': event.user_id, 'message': answer,'random_id': 0})


if __name__ == "__main__":
    main()