from math import ceil

def build(data, cur_page):
    max_per_page = 3
    max_page = ceil(len(data) / max_per_page)

    cur_first_index = cur_page * max_per_page

    str_data = f"Сторінка {cur_page + 1} з {max_page}\n\n"

    for i in range(cur_first_index, cur_first_index + max_per_page):
        if i < len(data):
            str_data += (
                f"{data[i]['url']} -- "
                f"{data[i]['send_method']} -- "
                f"{data[i]['status']}\n\n"
            )

    return str_data