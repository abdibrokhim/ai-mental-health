


def clean_text(gen_text):
    prompt_list = []
    l = gen_text.split('.')

    for i in l:
        a = i.strip().replace('\n', '')
        b = a.startswith('To find')
        if not b and a != '':
            prompt_list.append(i)

    return prompt_list


def make_text(prompt_list):

    text = ''

    for i in prompt_list:
        text += i + ' '

    return text
