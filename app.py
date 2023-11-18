from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
from web3 import Web3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ens_name = request.form.get('ens_name')
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/90a62b0b31bc4303be06952875fde341'))
        address = w3.ens.address(ens_name)
        avatar = w3.ens.get_text(ens_name, "avatar")

        return render_template('hello.html', ens_name=ens_name,address=address, avatar=avatar)

    return render_template('index.html')

@app.route('/qr_code/<ens_name>')
def qr_code(ens_name):

    url = f"https://app.ens.domains/{ens_name}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
