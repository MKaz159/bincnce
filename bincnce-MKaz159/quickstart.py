from os.path import exists
from datetime import date


def SendEmailToMKAZ(message):
    today_date = date.today()
    if exists('./script_results.txt'):
        print('file exists')
        with open('script_results.txt', '+a') as file:
            file.write(f'\nScript ran on {today_date} with the following results:\n')
            file.write(message + '\n')
    else:
        with open('script_results.txt', 'w') as f:
            f.write(f'Script ran on {today_date} with the following results:\n')
            f.write(message)


def main():
    mes = 'Test (quickstart performed RUN operation)'
    SendEmailToMKAZ(mes)



if __name__ == '__main__':
    main()