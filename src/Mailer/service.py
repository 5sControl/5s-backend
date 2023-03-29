from django.core.mail import send_mail
from rest_framework.response import Response


def send_message(item, count):

    if item[0].get("email") == None:
        return print(f'We notify you when the minimum balance of the {item[0].get("name")} is reached, the minimum balance is {count} out of {item[0].get("low_stock_level")}.')
    else:
        send_mail(
            'Balance notice',
            f'We notify you when the minimum balance of the {item[0].get("name")} is reached, the minimum balance is {count} out of {item[0].get("low_stock_level")}.',
            'Taqtile@yandex.by',
            [f'{item[0].get("email")}'],
            fail_silently=False,
        )

        return Response({'success': True})
