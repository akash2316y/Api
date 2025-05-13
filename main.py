from flask import Flask, request, jsonify, redirect
import requests
import urllib.parse

app = Flask(__name__)

BASE_URL = "https://unpleasant-leena-noobx-1206f7ad.koyeb.app/"  # Replace with your actual deployed Koyeb URL

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

    api_url = f"https://terabox.web.id/url?url={url}&token=184db604-9f21-4591-b510-5bdddec4a90c_6987158459"

    try:
        r = requests.get(api_url)
        data = r.json()

        for item in data:
            for key in ['direct_link', 'link', 'thumbnail']:
                if key in item:
                    encoded = urllib.parse.quote_plus(item[key])
                    item[key] = f"{BASE_URL}/redirect?target={encoded}"

            if "direct_link" in item:
                # Add a streaming URL too
                encoded_stream = urllib.parse.quote_plus(item["direct_link"])
                item["stream_url"] = f"{BASE_URL}/redirect?target={encoded_stream}&video=true"

            if "size" in item:
                item["size"] = format_size(item["size"])

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": "Failed to fetch from source API", "details": str(e)}), 500

@app.route('/redirect')
def redirector():
    target = request.args.get('target')
    video = request.args.get('video')

    if not target:
        return "Missing target", 400

    decoded_target = urllib.parse.unquote_plus(target)

    if video == 'true':
        return f'''
        <html>
            <head>
                <title>Stream Video</title>
                <style>
                    body {{
                        background-color: #000;
                        color: #fff;
                        text-align: center;
                        padding: 20px;
                        font-family: sans-serif;
                    }}
                    video {{
                        width: 90%;
                        height: auto;
                        max-width: 800px;
                        margin-top: 20px;
                        border: 2px solid #fff;
                        border-radius: 10px;
                    }}
                </style>
            </head>
            <body>
                <h1>Streaming from Akash API</h1>
                <video controls autoplay>
                    <source src="{decoded_target}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </body>
        </html>
        '''
    else:
        return redirect(decoded_target)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
