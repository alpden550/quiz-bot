import os


def get_questions_from_text(text):
    questions = {}
    question, answer = None, None

    for contents in text:
        if 'Вопрос' in contents:
            question = ' '.join(contents.strip().splitlines()[1:])
        elif 'Ответ' in contents:
            answer = ' '.join(contents.strip().splitlines()[1:])
        if question and answer:
            questions[question] = answer
    return questions


def get_all_questions(directory='quiz-questions'):
    all_questions = {}
    for file in os.listdir(directory):
        try:
            with open(f'{directory}/{file}', 'r', encoding='KOI8-R') as quiz_file:
                all_text = quiz_file.read().split('\n\n')
        except FileNotFoundError:
            all_text = None
        questions = get_questions_from_text(all_text)
        all_questions.update(questions)
    return all_questions


if __name__ == "__main__":
    all_questions = get_all_questions()
    print(len(all_questions))
