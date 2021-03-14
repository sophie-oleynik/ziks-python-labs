import getpass


ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def generate_password_1(input):
    words = input.split(" ")
    result = []
    # First element
    char_count = len(words[0]) + len(words[2])
    result.append(ALPHABET[(char_count - 1) % len(ALPHABET)])
    # Second element
    last_char = words[1][len(words[1]) - 1].lower()
    last_char_index = ALPHABET.index(last_char)
    second_element_index = last_char_index - 1 if last_char_index > 0 else 25
    result.append(ALPHABET[second_element_index])
    # Third element
    isOdd = len(words[2]) % 2 == 0
    third_element = ""
    if isOdd:
        third_element = words[2][int((len(words[2]) / 2) - 1)]
        third_e_index = ALPHABET.index(third_element)
        third_e_index = third_e_index - 1 if third_e_index > 0 else 25
    else:
        third_element = words[2][int((len(words[2]) - 1) / 2)]
        third_e_index = ALPHABET.index(third_element)
        third_e_index = third_e_index + 1 if third_e_index < 25 else 0
    result.append(ALPHABET[third_e_index])
    # Fourth element
    index_of_fourth = ALPHABET.index(words[0][0].lower())
    fourth_element_index = index_of_fourth + 1 if index_of_fourth < 25 else 0
    result.append(ALPHABET[fourth_element_index])

    # Return generated password
    str = ""
    return str.join(result)


def generate_password_2(input):
    words = input.split(" ")
    result = []
    # First element
    index_of_first_char = ALPHABET.index(words[0][1].lower())
    first_element_index = index_of_first_char + 1 if index_of_first_char < 25 else 0
    result.append(ALPHABET[first_element_index])
    # Second element
    last_char = words[1][len(words[1]) - 1].lower()
    last_char_index = ALPHABET.index(last_char)
    second_element_index = last_char_index - 1 if last_char_index > 0 else 25
    result.append(ALPHABET[second_element_index])
    # Third element
    isOdd = len(words[2]) % 2 == 0
    third_element = ""
    if isOdd:
        third_element = words[2][int((len(words[2]) / 2) - 1)]
        third_e_index = ALPHABET.index(third_element)
        third_e_index = third_e_index - 1 if third_e_index > 0 else 25
    else:
        third_element = words[2][int((len(words[2]) - 1) / 2) - 1]
        third_e_index = ALPHABET.index(third_element)
        third_e_index = third_e_index + 1 if third_e_index < 25 else 0
    result.append(ALPHABET[third_e_index])
    # Fourth element
    char_count = len(words[0]) + len(words[2]) + 1
    result.append(ALPHABET[(char_count - 1) % len(ALPHABET)])

    # Return generated password
    str = ""
    return str.join(result)


def get_password_input():
    password = getpass.getpass(prompt='Enter login password: ', stream=None)
    return password


def main():
    try:
        key = int(input("1. Task 1\n2. Task 2\nEnter: "))
        calculated = None
        if key == 1:
            print("Sony Hewlett Mercedes")
            calculated = generate_password_1("Sony Hewlett Mercedes")
            # CORRECT password is - lsbt
        elif key == 2:
            print("mathematic computer scanner")
            calculated = generate_password_2("mathematic computer scanner")
            # CORRECT password is - bqbr
        else:
            return main()
        entered = get_password_input()
        message = "Correct" if entered == calculated else "InCorrect"
        print(message)
    except:
        return main()


main()
