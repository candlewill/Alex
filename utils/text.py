'''
使用没用用括号括起来的分隔符号splitter，来分割输入文本text
'''


def split_by(text, splitter,
             opening_parentheses='',
             closing_parentheses='',
             quotes="'\""):
    """
    Splits the input text at each occurrence of the splitter only if it is not
    enclosed in parentheses.

    text - the input text string
    splitter - multi-character string which is used to determine the position
               of splitting of the text
    opening_parentheses - an iterable of opening parentheses that has to be
                          respected when splitting, e.g. "{(" (default: '')
    closing_parentheses - an iterable of closing parentheses that has to be
                          respected when splitting, e.g. "})" (default: '')
    quotes - an iterable of quotes that have to come in pairs, e.g. '"'

    """
    split_list = []

    # Interpret the arguments.
    parentheses_counter = dict((char, 0)
                               for char in opening_parentheses + quotes)
    map_closing_to_opening = dict(zip(closing_parentheses,
                                      opening_parentheses))

    segment_start = 0
    segment_end = 0
    while segment_end < len(text):
        cur_char = text[segment_end]
        if cur_char in opening_parentheses:
            parentheses_counter[cur_char] += 1
        elif cur_char in closing_parentheses:
            parentheses_counter[map_closing_to_opening[cur_char]] -= 1

            if parentheses_counter[map_closing_to_opening[cur_char]] < 0:
                raise ValueError(("Missing an opening parenthesis for: {par} "
                                  "in the text: {text}").format(par=cur_char,
                                                                text=text))
        elif cur_char in quotes:
            parentheses_counter[cur_char] = (
                                                parentheses_counter[cur_char] + 1) % 2
        elif text[segment_end:].startswith(splitter):
            # Test that all parentheses are closed.
            if not any(parentheses_counter.values()):
                split_list.append(text[segment_start:segment_end].strip())
                segment_end += len(splitter)
                segment_start = segment_end

        segment_end += 1
    else:
        split_list.append(text[segment_start:segment_end].strip())

    return split_list

if __name__ == '__main__':
    print(split_by("fewfewafewfe", "f"))