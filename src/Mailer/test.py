import smtplib
import sys


#Параметр, передаваемый при запуске скрипта:
txtparam=sys.argv[1]
#От кого:
fromaddr = 'Mr. Robot <someaccount@gmail.com>'
#Кому:
toaddr = 'Administrator <Dimskay-1988@mail.ru>'
#Тема письма:
subj = 'Notification from system'
#Текст сообщения:
msg_txt = 'Notice:\n\n ' +  txtparam + '\n\nBye!' #
#Создаем письмо (заголовки и текст)
msg = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % ( fromaddr, toaddr, subj, msg_txt)
#Логин gmail аккаунта. Пишем только имя ящика.
#Например, если почтовый ящик someaccount@gmail.com, пишем:
username = 'someaccount'
#Соответственно, пароль от ящика:
password = 'somepassword'
#Инициализируем соединение с сервером gmail по протоколу smtp.
server = smtplib.SMTP('smtp.gmail.com:587')
#Выводим на консоль лог работы с сервером (для отладки)
server.set_debuglevel(1);
#Переводим соединение в защищенный режим (Transport Layer Security)
server.starttls()
#Проводим авторизацию:
server.login(username,password)
#Отправляем письмо:
server.sendmail(fromaddr, toaddr, msg)
#Закрываем соединение с сервером
server.quit()