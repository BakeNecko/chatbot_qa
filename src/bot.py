from pandas.errors import DatabaseError
import ollama
from pprint import pprint
from src.utils.dto import State
from src.vanna_train import get_vanna
import os


def generate_prompt(state: 'State'):
    prompt = (
        "Ответь на вопрос пользователя, используя только эти данные"
        f'Вопрос: {state['question']}\n'
        f'Данные: {state['result']}\n\n'
        "Округляй дробные значения"
        "Если вы не знаете ответа, просто скажите «я не знаю». Не пытайтесь что-то выдумать."
    )
    return prompt


if __name__ == '__main__':
    vn = get_vanna()
    os.system('clear')
    err = False
    while True:
        try:
            if err:
                print('Произошла ошибка, попробуйте изменить вопрос')
                err = False
            user_input = input('Введите вопрос: ')
            if user_input == 'exit':
                pprint('Bye!')
                break
            try:
                sql_res = vn.generate_sql(user_input, allow_llm_to_see_data=True)
                sql_fix = False
                db_res = vn.run_sql(sql_res)
            except DatabaseError as e:
                print('DB ERROR: ', e)
                err = True
                break
            state = State(
                question=user_input,
                query=sql_res[0],
                result=db_res,
            )
            query = generate_prompt(state)
            os.system('clear')
            completion = ollama.chat(
                model="deepseek-r1:latest", #llama2 может отвечать лучше но на англ.
                messages=[
                    {"role": "system",
                        "content": "Ты - полезный помощник при поиске работы в IT."},
                    {"role": "user", "content": query}
                ],
            )
            print(f'SQL (fix={sql_fix}): \n', sql_res)
            print('#####')
            print('DATA: \n', db_res)
            print('#####')
            print('OUTPUT:\n ', completion['message']['content'])
            print('#####')
        except DatabaseError as e:
            print('Exc: ', e)
            print('Что-то пошло не так. Попробуйте еще раз:')
