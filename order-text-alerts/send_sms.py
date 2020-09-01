

from twilio.rest import Client

account_sid = 'AC38f904b840b582da820a4e18edef1ebc'
auth_token = '90b64384f9581fd86ae04071be727484'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Thanks for choosing Andover Pizza Ranch!",
                     messaging_service_sid='MG869564792f35036a37ca76441f47f632',
                     to='+17637725690'
                 )

print(message.sid)
