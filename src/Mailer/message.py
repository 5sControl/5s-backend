# import os
#
# from django.core.mail import EmailMessage
# from django.core.mail.backends.smtp import EmailBackend
#
# from datetime import datetime
# from src.Core.const import SERVER_URL
#
# from src.Mailer.models import SMTPSettings, WorkingTime
# from src.CompanyLicense.models import Company
#
#
# def send_email_to_suppliers(item, image_path):
#     try:
#         work_time = WorkingTime.objects.last()
#         if item.suppliers is None or item.suppliers.contact_email is None:
#             raise ValueError("Missing contact email")
#         my_company = Company.objects.filter(my_company=True).order_by('-id').first()
#         count_order = item.order_quantity
#
#         if item.name is None:
#             raise ValueError("Missing item name")
#         if item.suppliers.name_company is None:
#             raise ValueError("Missing supplier name")
#         if my_company.name_company is None:
#             raise ValueError("Missing my company name")
#         if my_company.country is None:
#             raise ValueError("Missing my company country")
#         if my_company.state is None:
#             raise ValueError("Missing my company state")
#         if my_company.city is None:
#             raise ValueError("Missing my company city")
#         if my_company.first_address is None:
#             raise ValueError("Missing my company first_address")
#         if my_company.contact_phone is None:
#             raise ValueError("Missing my company phone")
#         if my_company.contact_email is None:
#             raise ValueError("Missing my company email")
#
#     except Exception as exc:
#         print(f"Not enough parameters to send notification: {exc}")
#         return
#     address = f"{my_company.country} {my_company.state} {my_company.city} {my_company.first_address}"
#     subject = f"Urgent Reorder Request: Low Stock Level Notification - {item.name}"
#     message = f"Dear {item.suppliers.name_company}!\nBy this message we notify you of our urgent need to reorder a specific item due to its low stock level.\nItem Details:\nItem Name: {item.name},\nQuantity Needed: {count_order}\n\nPlease ensure that the additional order is promptly processed and dispatched to us to avoid any disruptions to our operations. We kindly request your immediate attention to this matter.\n\nCompany Information:\nCompany Name: {my_company.name_company}\nAddress: {address}\nPhone: {my_company.contact_phone}\nEmail: {my_company.contact_email}\n\nPlease note that this message is automatically generated, and there is no need to reply to it. However, if you have any questions or require further information, please feel free to contact us using the provided company details.We appreciate your ongoing partnership and your commitment to providing quality products and services. Thank you for your prompt attention to this matter.\nBest regards, {my_company.name_company}\n"
#
#     image_name = image_path.split('/')[-1]
#
#     recipient_list = [item.suppliers.contact_email]
#     print("все параметры ок")
#     # email service check
#     try:
#         smtp_settings = SMTPSettings.objects.first()
#     except SMTPSettings.DoesNotExist:
#         raise Exception('SMTP configuration is not defined')
#
#     # Check if a message was already
#     today = datetime.now().time()
#     start_time = work_time.time_start
#     end_time = work_time.time_end
#     if start_time < today < end_time:
#         # sending email
#
#         connection = EmailBackend(
#             host=smtp_settings.server,
#             port=smtp_settings.port,
#             username=smtp_settings.username,
#             password=smtp_settings.password,
#             use_tls=smtp_settings.email_use_tls,
#             use_ssl=smtp_settings.email_use_ssl,
#         )
#         # create email message
#         email_message = EmailMessage(
#             subject=subject,
#             body=message,
#             from_email=smtp_settings.username,
#             to=recipient_list
#         )
#         # send image
#         image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', f'{image_path}')
#         with open(image_path, 'rb') as f:
#             image_data = f.read()
#         email_message.attach(filename=f'{image_name}', content=image_data, mimetype='images/jpg')
#
#         # send file
#         file_path = item.suppliers.file
#         if file_path is not None:
#             file_name = file_path.name
#             file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', f'images/{file_name}')
#             if os.path.exists(file_path):
#                 with open(file_path, 'rb') as f:
#                     file_data = f.read()
#                 email_message.attach(file_name, file_data,
#                                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             else:
#                 raise ValueError("File does not exist")
#         else:
#             raise ValueError("File path is not provided")
#
#         # send email
#         connection.send_messages([email_message])
#
#     else:
#         print('Working time limit, message not sent')
