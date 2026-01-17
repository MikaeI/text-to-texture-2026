import json
import base64
import quart
import quart_cors
from quart import request
import urllib.parse

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.post("/generate")
async def generate():
    request = await quart.request.get_json(force=True)
    a = str(request["a"])

    print(a)

    return quart.Response(
        response=json.dumps({
            "result":
                (
                    '![](http://localhost:5004/t.svg' +
                        '?a=' + urllib.parse.quote(a.split(",")[0]) +
                        '&b=' + urllib.parse.quote(a.split(",")[1]) +
                        '&c=' + urllib.parse.quote(a.split(",")[2]) +
                        '&d=' + urllib.parse.quote(a.split(",")[3]) +
                        '&e=' + urllib.parse.quote(a.split(",")[4]) +
                        '&f=' + urllib.parse.quote(a.split(",")[5]) +
                        '&g=' + urllib.parse.quote(a.split(",")[6]) +
                        '&h=' + urllib.parse.quote(a.split(",")[7]) +
                        '&i=' + urllib.parse.quote(a.split(",")[8]) +
                    ')'
                )
            }),
        status=200
    )

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'

    return await quart.send_file(filename, mimetype='image/png')

@app.get("/t.svg")
async def plugin_svg():
    a = quart.request.args.get("a").strip().replace("'", "")
    b = quart.request.args.get("b").strip().replace("'", "")
    c = quart.request.args.get("c").strip().replace("'", "")
    d = quart.request.args.get("d").strip().replace("'", "")
    e = quart.request.args.get("e").strip().replace("'", "")
    f = quart.request.args.get("f").strip().replace("'", "")
    g = quart.request.args.get("g").strip().replace("'", "")
    h = quart.request.args.get("h").strip().replace("'", "")
    i = quart.request.args.get("i").strip().replace("'", "")
    markup = '''<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
        <filter id="filter" x="-20%" y="-20%" width="140%" height="140%" filterUnits="objectBoundingBox" primitiveUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
            <feTurbulence type="''' + a + '''" baseFrequency="''' + b + ''' ''' + c + '''" numOctaves="''' + d + '''" />
            <feColorMatrix type="saturate" values="0" />
            <feDiffuseLighting surfaceScale="''' + e + '''" diffuseConstant="''' + f + '''" lighting-color="#808080" in="turbulence" result="diffuseLighting">
                <feDistantLight azimuth="''' + g + '''" elevation="''' + h + '''" />
            </feDiffuseLighting>
        </filter>
        <rect width="512" height="512" fill="''' + i + '''" />
        <rect width="512" height="512" filter="url(#filter)" style="mix-blend-mode: luminosity" />
    </svg>'''

    return quart.Response(markup, mimetype='image/svg+xml')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()

        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()

        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5004)

if __name__ == "__main__":
    main()
