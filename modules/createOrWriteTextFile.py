from datetime import date, datetime
import os


def time_now():
    now = datetime.now()
    return str(now)


def get_current_time():
    now = datetime.now()
    print(now)
    current_time = now.strftime("%H:%M:%S")
    return current_time
    # print("Current Time =", current_time)


def date_now():
    today = date.today()
    Str = date.isoformat(today)
    return Str


def get_visit_id_date(date):
    return "".join(str(date).split("-"))


def parent_dir():
    # print(os.getcwd())
    return os.getcwd()


def request_text_file(user=None, value=None, dir=None):
    if dir:
        file_path = f'{parent_dir()}/logFiles/request/{dir}/{date_now()}.txt'
    else:
        file_path = f'{parent_dir()}/logFiles/request/{date_now()}.txt'
    # print(f'file_path == {file_path}')
    try:
        with open(file_path, "a") as f:
            f.write("\n")
            f.write(time_now())
            f.write("\n")
            f.write(f'user is {str(user)}')
            f.write("\n")
            f.write(str(value))
            f.write("\n")

    except FileNotFoundError:
        print("The 'docs' directory does not exist")


def response_text_file(user=None, value=None, dir=None):
    if dir:
        file_path = f'{parent_dir()}/logFiles/response/{dir}/{date_now()}.txt'
    else:
        file_path = f'{parent_dir()}/logFiles/response/{date_now()}.txt'

    try:
        with open(file_path, "a") as f:
            f.write("\n")
            f.write(time_now())
            f.write("\n")
            f.write(f'user is {str(user)}')
            f.write("\n")
            f.write(str(value))
            f.write("\n")

    except FileNotFoundError:
        print("The 'docs' directory does not exist")
