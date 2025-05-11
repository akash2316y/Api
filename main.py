from flask import Flask, request, jsonify, redirect
import requests
import urllib.parse

app = Flask(__name__)

BASE_URL = "https://unpleasant-leena-noobx-1206f7ad.koyeb.app/"  # <-- Replace with your Koyeb URL

def format_size(size):
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

@app.route('/')
def home():
    return '''
    <html>
        <head><title>Akash API</title></head>
        <body style="text-align:center; font-family:sans-serif; padding-top:50px;">
            <h1>Welcome to Terabox API</h1>
            <p>By <strong>@Akash_Servers</strong></p>
        </body>
    </html>
    '''

@app.route('/api')
def my_api():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    api_url = f"https://terabox.web.id/url?url={url}&token=88c98289-92ae-4ebf-9751-80b77717ad47_6987158459"

    try:
        r = requests.get(api_url)
        data = r.json()

        for item in data:
            for key in ['direct_link', 'link', 'thumbnail']:
                if key in item:
                    encoded = urllib.parse.quote_plus(item[key])
                    item[key] = f"{BASE_URL}/redirect?target={encoded}"

            if "size" in item:
                item["size"] = format_size(item["size"])

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": "Failed to fetch from source API", "details": str(e)}), 500

@app.route('/redirect')
def redirector():
    target = request.args.get('target')
    if not target:
        return "Missing target", 400
    return redirect(target)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
