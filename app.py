import replicate
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    resp = MessagingResponse()
    media_url = request.form.get('MediaUrl0')
    if media_url:
        r = requests.get(media_url)
        filename = request.values['MessageSid'] + '.jpg'
       
        with open(filename, 'wb') as f:
            f.write(r.content)
        msg = resp.message("Got your image!")
        output = replicate.run(
            #"sdxl-emoji:4d2c2e5e40a5cad182e5729b49a08247c22a5954ae20356592caaada42dc8985",
            "sanzgiri/cartoonify:a6f24cf966b84dc3959b9c84f6f5739287b243bc85d5d2f5fb0a9ca9eb6a0f0a",
            input={"infile": open(filename, "rb")}
        )
        print(output)
        msg.media(output)
    else:
        resp.message('Please send an image!')
    return str(resp)

    

if __name__ == "__main__":
    app.run(debug=True)