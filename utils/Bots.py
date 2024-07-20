import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = 'vk1.a.twQWhoQKZLg1EGRKrHwX6gyAQTt5FW55JaIE7wTvFWRHa9CWsv9g2HKHhRi9RSZdVR_8UohJ0J-nw1Pma-wekbjojIPkP8w4zSXbRFVmS8UwyMg-jtI-WgH2aJzNBLIImJjPv0Pyz0jf-pYAkye0aoBVFhKK7nRdSPJeR-RGK-cvWan-2hKcn-9BCCAJsRDsaoBjuFOv9OroQmEcITHhtQ'

vk_session = vk_api.VkApi(token=TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

scope = ["https://docs.google.com/spreadsheets/d/1s3WEnxUGNOw9CzJc34ohm6F5KIPswM56ABLbihgPO7s/edit?gid=1206327905#gid=1206327905", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(".venv/credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("a").sheet1

def get_qa_pairs():
    data = sheet.get_all_records()
    qa_pairs = {}
    for row in data:
        question = row.get("Вопрос").lower()
        answer = row.get("Ответ")
        qa_pairs[question] = answer
    return qa_pairs

def main():
    qa_pairs = get_qa_pairs()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            message_text = event.text.lower()

            response = qa_pairs.get(message_text, "Извините, я не понимаю вашего вопроса.")

            send_message(user_id, response)

if __name__ == '__main__':
    main()

