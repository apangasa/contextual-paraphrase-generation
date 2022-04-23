import os
import json
import language_tool_python
from tqdm import tqdm
import autocorrect

tool = language_tool_python.LanguageTool('en-US')
speller = autocorrect.Speller()


def correct_errors(text):
    update_length = 0
    broken_rules = tool.check(text)
    for rule in broken_rules:
        if rule.category != 'TYPOS':
            continue

        if len(rule.replacements):
            if rule.replacements[0] == '':
                continue

            error_index = rule.offset
            error_length = rule.errorLength

            text = text[:error_index + update_length] + rule.replacements[0] + \
                text[error_index + error_length + update_length:]
            update_length += len(rule.replacements[0]) - error_length
    return text


def construct_data_dict():
    phrase_paraphrase_map: dict = {}

    wa_path = './data/wa/'
    wa_fnames = os.listdir(wa_path)
    for fname in wa_fnames:
        if not fname.endswith('.data'):
            continue

        with open(os.path.join(wa_path, fname), 'r', encoding='utf8') as wa_file:
            for line in tqdm(wa_file.readlines()):

                if 'a:' in line:  # remove answer
                    line = line[line.find('q:'):]

                questions = {q.strip()
                             for q in line.split('q:')}  # create question set

                if '' in questions:  # remove empty string element
                    questions.remove('')

                if len(questions) < 2:  # check we have at least a phrase and paraphrase
                    continue

                # extract phrase and paraphrase
                key = questions.pop()
                val = questions.pop()

                # key = speller(key)
                # val = speller(val)

                # key = correct_errors(key)
                # val = correct_errors(val)

                # add phrase: paraphrase to dictionary
                phrase_paraphrase_map[key] = val

        # update json file regularly
        with open(os.path.join(wa_path, 'wa_dict.json'), 'w') as map_file:
            json.dump(phrase_paraphrase_map, map_file)


def main():
    construct_data_dict()
    # with open('./data/wa/wa_dict.json', 'r') as map_file:
    #     mappy = json.load(map_file)
    #     print(len(mappy))


if __name__ == '__main__':
    main()
