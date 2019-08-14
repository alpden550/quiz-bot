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
    for file in os.listdir(os.path.abspath(directory)):
        with open(f'{directory}/{file}', 'r', encoding='KOI8-R') as quiz_file:
            text_blocks = quiz_file.read().split('\n\n')
        questions = get_questions_from_text(text_blocks)
        all_questions.update(questions)
    return all_questions


def test_questions():
    with open('1vs1200.txt', 'r') as file:
        text = file.read().split('\n\n')
    questions = get_questions_from_text(text)
    return questions


if __name__ == "__main__":
    all_questions = get_all_questions()
    print(len(all_questions))
