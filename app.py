from flask import Flask, render_template, request, send_from_directory
import requests, shutil, time, string, random, os, urllib.parse, openai

app = Flask(__name__)

STATIC_FOLDER = os.path.join(app.root_path, 'static')
IMAGES_FOLDER = os.path.join(STATIC_FOLDER, 'images')

PRODIA_KEY = os.environ.get("X_PRODIA_KEY")
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_prompt_suggestions(keyword):
    prompt = f""" I want you to help me make requests (prompts) for the Stable Diffusion neural network.

                    Stable diffusion is a text-based image generation model that can create diverse and high-quality images based on your requests. In order to get the best results from Stable diffusion, you need to follow some guidelines when composing prompts.

                    Here are some tips for writing prompts for Stable diffusion1:

                    1) Be as specific as possible in your requests. Stable diffusion handles concrete prompts better than abstract or ambiguous ones. For example, instead of “portrait of a woman” it is better to write “portrait of a woman with brown eyes and red hair in Renaissance style”.
                    2) Specify specific art styles or materials. If you want to get an image in a certain style or with a certain texture, then specify this in your request. For example, instead of “landscape” it is better to write “watercolor landscape with mountains and lake".
                    3) Specify specific artists for reference. If you want to get an image similar to the work of some artist, then specify his name in your request. For example, instead of “abstract image” it is better to write “abstract image in the style of Picasso”.
                    4) Weigh your keywords. You can use token:1.3 to specify the weight of keywords in your query. The greater the weight of the keyword, the more it will affect the result. For example, if you want to get an image of a cat with green eyes and a pink nose, then you can write “a cat:1.5, green eyes:1.3,pink nose:1”. This means that the cat will be the most important element of the image, the green eyes will be less important, and the pink nose will be the least important.
                    Another way to adjust the strength of a keyword is to use () and []. (keyword) increases the strength of the keyword by 1.1 times and is equivalent to (keyword:1.1). [keyword] reduces the strength of the keyword by 0.9 times and corresponds to (keyword:0.9).

                    You can use several of them, as in algebra... The effect is multiplicative.

                    (keyword): 1.1
                    ((keyword)): 1.21
                    (((keyword))): 1.33

                    Similarly, the effects of using multiple [] are as follows

                    [keyword]: 0.9
                    [[keyword]]: 0.81
                    [[[keyword]]]: 0.73


                    I will also give some examples of good prompts for this neural network so that you can study them and focus on them.

                    Examples:

                    a cute kitten made out of metal, (cyborg:1.1), ([tail | detailed wire]:1.3), (intricate details), hdr, (intricate details, hyperdetailed:1.2), cinematic shot, vignette, centered

                    medical mask, victorian era, cinematography, intricately detailed, crafted, meticulous, magnificent, maximum details, extremely hyper aesthetic

                    a girl, wearing a tie, cupcake in her hands, school, indoors, (soothing tones:1.25), (hdr:1.25), (artstation:1.2), dramatic, (intricate details:1.14), (hyperrealistic 3d render:1.16), (filmic:0.55), (rutkowski:1.1), (faded:1.3)

                    Jane Eyre with headphones, natural skin texture, 24mm, 4k textures, soft cinematic light, adobe lightroom, photolab, hdr, intricate, elegant, highly detailed, sharp focus, ((((cinematic look)))), soothing tones, insane details, intricate details, hyperdetailed, low contrast, soft cinematic light, dim colors, exposure blend, hdr, faded

                    a portrait of a laughing, toxic, muscle, god, elder, (hdr:1.28), bald, hyperdetailed, cinematic, warm lights, intricate details, hyperrealistic, dark radial background, (muted colors:1.38), (neutral colors:1.2)

                    My query may be in other languages. In that case, translate it into English. Your answer is exclusively in English (IMPORTANT!!!), since the model only understands it.
                    Also, you should not copy my request directly in your response, you should compose a new one, observing the format given in the examples.
                    Don't add your comments, but answer right away.

                    My first request is - {keyword}. """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role" : "user", "content" : f" {prompt} "}, 
            {"role" : "assistant", "content" : "Assistant : '  "}
                ],
                n=1,
                stop=None, 
                temperature=0.4,
            )
    response = completion['choices'][0]['message']['content']
    return response

@app.route("/suggest", methods=["POST"])
def suggest():
    keyword = request.form["keyword"]
    suggestions = get_prompt_suggestions(keyword)

    prompt = request.form.get("prompt", "")

    prompt += f"{suggestions}"

    return render_template("index.html", prompt=prompt)

def generate_filename():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"generated_image_{random_string}.png"

def gt(prompt, model, aspect_ratio, upscale):
    file_path = os.path.join(app.root_path, 'negative_prompts.txt')
    with open(file_path, 'r') as file:
        negative_prompts = file.read().splitlines()
    
    neg_prompt = ', '.join(negative_prompts)

    url = "https://api.prodia.com/v1/job"
    payload = {
        "negative_prompt": neg_prompt,
        "prompt": f"{prompt}, high-resolution, maximum detailed, ultra-realistic, 4k, HD, HQ",
        "model": f"{model}",
        "steps": 25,
        "cfg_scale": 7,
        "seed": -1,
        "sampler": "DPM++ 2M Karras",
        "aspect_ratio": f"{aspect_ratio}",
        "upscale": upscale
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": PRODIA_KEY
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

def ret(jid):
    url = f"https://api.prodia.com/v1/job/{jid}"
    headers = {
        "accept": "application/json",
        "X-Prodia-Key": PRODIA_KEY
    }
    response = requests.get(url, headers=headers)
    return response
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        model = request.form.get("model")
        aspect_ratio = request.form.get("aspect_ratio")
        checkbox_value = request.form.get('upscale')
        if checkbox_value:
            upscale = True
        else:
            upscale = False

        job_ids = []
        for i in range(4):
            job = gt(prompt, model, aspect_ratio, upscale)
            if job.status_code == 200:
                job_id = job.json()["job"]
                time.sleep(5)
                job_ids.append(job_id)
            else:
                return render_template("index.html", message=f"Error creating jobs. Status code: {job.status_code}")
        images = []
        for jid in job_ids:
            response = ret(jid)
            if response.status_code == 200:
                response_json = response.json()
                status = response_json.get("status")
                image_url = response_json.get("imageUrl")
                if status == "succeeded" and image_url is not None:
                    parsed_url = urllib.parse.urlparse(image_url)
                    filename = generate_filename()
                    filepath = os.path.join(app.static_folder, 'images', filename)
                    image_response= requests.get(image_url, stream=True)
                    if image_response.status_code == 200:
                        with open(filepath,'wb') as f1: 
                            shutil.copyfileobj(image_response.raw,f1) 
                        images.append(filename)
        return render_template("index.html", images=images)
    else: 
        images = []
        for filename in os.listdir(IMAGES_FOLDER):
            if filename.endswith(".png"):
                images.append(filename)
        return render_template("index.html", images=images)

@app.route("/static/<path:filename>")
def static_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/static/images/<path:filename>")
def static_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

if __name__ == "__main__":
    app.run()
