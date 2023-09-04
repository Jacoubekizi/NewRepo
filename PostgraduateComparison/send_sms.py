# import os 
import vonage

# VONAGE_API_KEY = os.environ['VONAGE_API_KEY']
# VONAGE_API_SECRET = os.environ['VONAGE_API_SECRET']

#Create a client instance and then pass the client to the Sms instance
client = vonage.Client(key="4f813a05", secret="AB7Kz4N3ZlcPcQmM")
# sms = vonage.Sms(client)
print(client.account.get_balance())

responseData = client.sms.send_message(
    {
        "from": "Vonage",
        "to": "0957322954",
        "text": "A text message sent using the Vonage SMS API",
    }
)

if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")