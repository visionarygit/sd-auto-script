import base64
import datetime
import os
import random
import time
from io import BytesIO

import requests
from PIL import Image, PngImagePlugin

domain = 'http://localhost:7860'
# txt2img_output = '/content/stable-diffusion-webui/output/txt2image/20230413111'
txt2img_output = 'F:\\SDAI\\stable-diffusion-webui\\outputs\\txt2img-images\\auto'
img2img_output = '/content/stable-diffusion-webui/output/img2image/20230413111'
final_output = '/content/stable-diffusion-webui/output/final/20230413111'
prompt_dir = 'F:\\code\\sd-auto-script\\src\\resource'
chest_prompt_file = 'F:\\code\\sd-auto-script\\src\\resource\\chest_prompt.txt'
clothes_prompt_file = 'F:\\code\\sd-auto-script\\src\\resource\\clothes_prompt.txt'
expression_prompt_file = 'F:\\code\\sd-auto-script\\src\\resource\\expression_prompt.txt'
hair_prompt_file = 'F:\\code\\sd-auto-script\\src\\resource\\hair_prompt.txt'
sock_prompt_file = 'F:\\code\\sd-auto-script\\src\\resource\\sock_prompt.txt'
style_prompt_file = 'F:\\code\\sd-auto-script\\src\\resource\\style_prompt.txt'

start_prompt = 'best quality ,masterpiece, extremely detailed ,CG ,unity ,8k wallpaper, Amazing, finely detail, ' \
               'masterpiece,extremely detailed CG unity 8k wallpaper,absurdres, incredibly absurdres, huge filesize , ' \
               'ultra-detailed, highres, extremely detailed,(1girl_solo),(beautiful detailed girl:1)'
lora_prompt = ' <lora:taiwanDollLikeness_v10:0.3> <lora:koreanDollLikeness_v15:0.4> <lora:japaneseDollLikeness_v10:0.3>'

style_prompt = []
chest_prompt = []
clothes_prompt = []
hair_prompt = []
expression_prompt = []
sock_prompt = []

txt2img_payload = {
    "enable_hr": False,
    "denoising_strength": 0,
    "firstphase_width": 0,
    "firstphase_height": 0,
    "hr_scale": 2,
    "hr_upscaler": "",
    "hr_second_pass_steps": 0,
    "hr_resize_x": 0,
    "hr_resize_y": 0,
    "prompt": "",
    "styles": [
    ],
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 50,
    "cfg_scale": 7,
    "width": 768,
    "height": 1024,
    "restore_faces": True,
    "tiling": False,
    "do_not_save_samples": False,
    "do_not_save_grid": False,
    "negative_prompt": "(((simple background))),monochrome ,lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, lowres, bad anatomy, bad hands, text, error, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, ugly,pregnant,vore,duplicate,morbid,mut ilated,tran nsexual, hermaphrodite,long neck,mutated hands,poorly drawn hands,poorly drawn face,mutation,deformed,blurry,bad anatomy,bad proportions,malformed limbs,extra limbs,cloned face,disfigured,gross proportions, (((missing arms))),(((missing legs))), (((extra arms))),(((extra legs))),pubic hair, plump,bad legs,error legs,username,blurry,bad feet",
    "eta": 0,
    "s_churn": 0,
    "s_tmax": 0,
    "s_tmin": 0,
    "s_noise": 1,
    "override_settings": {},
    "override_settings_restore_afterwards": True,
    "script_args": [],
    "sampler_index": "",
    "script_name": "",
    "send_images": True,
    "save_images": False,
    "alwayson_scripts": {}
}

img2img_payload = {
    "init_images": [
        "string"
    ],
    "resize_mode": 0,
    "denoising_strength": 0.75,
    "image_cfg_scale": 0,
    "mask": "string",
    "mask_blur": 4,
    "inpainting_fill": 0,
    "inpaint_full_res": True,
    "inpaint_full_res_padding": 0,
    "inpainting_mask_invert": 0,
    "initial_noise_multiplier": 0,
    "prompt": "",
    "styles": [
        "string"
    ],
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "sampler_name": "string",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 50,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "restore_faces": True,
    "tiling": False,
    "do_not_save_samples": False,
    "do_not_save_grid": False,
    "negative_prompt": "string",
    "eta": 0,
    "s_churn": 0,
    "s_tmax": 0,
    "s_tmin": 0,
    "s_noise": 1,
    "override_settings": {},
    "override_settings_restore_afterwards": True,
    "script_args": [],
    "sampler_index": "Euler",
    "include_init_images": False,
    "script_name": "string",
    "send_images": True,
    "save_images": False,
    "alwayson_scripts": {}
}

extra_img_batch_payload = {
    "resize_mode": 0,
    "show_extras_results": True,
    "gfpgan_visibility": 0,
    "codeformer_visibility": 0,
    "codeformer_weight": 0,
    "upscaling_resize": 2,
    "upscaling_resize_w": 512,
    "upscaling_resize_h": 512,
    "upscaling_crop": True,
    "upscaler_1": "None",
    "upscaler_2": "None",
    "extras_upscaler_2_visibility": 0,
    "upscale_first": False,
    "imageList": [
        {
            "data": "string",
            "name": "string"
        }
    ]
}


def img2base64(path):
    # 批量将指定路径下的图片转为base64
    # Create an empty list to store the base64 encoded strings
    print('=====================begin image to base64===========================')
    base64_list = []
    # Loop through each file in the directory
    i = 0
    for filename in os.listdir(path):
        # Check if the file is an image
        if filename.endswith(".jpg") or filename.endswith(".png"):
            i += 1
            # Open the image file in binary mode
            with open(os.path.join(path, filename), "rb") as image_file:
                # Read the contents of the image file
                image_bytes = image_file.read()
                # Convert the image bytes to base64 encoding
                base64_encoded = base64.b64encode(image_bytes)
                # Append the base64 encoded string to the list
                base64_list.append(base64_encoded)
    # Return the list of base64 encoded strings
    print(f'=====================end image to base64  size：{i}==========================')
    return base64_list


def base642img(base64_string, path):
    # Convert the base64 string to bytes
    img_bytes = base64.b64decode(base64_string)
    # Open the image using PIL
    img = Image.open(BytesIO(img_bytes))
    # Return the PIL image object
    img.save(os.path.join(path, f'{time.time()}.png'))
    return img


def tex2img(prompt, steps, batch_size):
    if prompt:
        txt2img_payload['prompt'] = prompt
    if steps:
        txt2img_payload['steps'] = steps
    if batch_size:
        txt2img_payload['batch_size'] = batch_size

    print('===============================begin txt2img =================================== payload is :',
          txt2img_payload)

    response = requests.post(url=f'{domain}/sdapi/v1/txt2img', json=txt2img_payload, timeout=12000)
    r = response.json()
    print('=============================== txt2img get result,begin save img=================================== ')

    current_path = txt2img_output + '\\' + datetime.date.today().strftime('%Y-%m-%d')

    if not os.path.exists(current_path):
        os.makedirs(current_path)
    for i in r['images']:
        image_info = i.split(",", 1)
        print(image_info)
        image = Image.open(BytesIO(base64.b64decode(image_info[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{domain}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        time_crr = time.time()
        image.save(os.path.join(current_path, f'{time_crr}.png'), pnginfo=pnginfo)
        image.close()

        # image_txt = open(os.path.join(current_path, f'{time_crr}.txt'), 'w')
        # image_txt.write(r['info'])
        # image_txt.close()

    print('===============================txt2img end=================================== output is :', txt2img_output)


def init_prompt():
    print('=============================begin init prompt======================================')
    global style_prompt
    global clothes_prompt
    global chest_prompt
    global expression_prompt
    global hair_prompt
    global sock_prompt
    style_prompt = open(style_prompt_file, 'r', encoding='UTF-8').read().split(',')
    print(f'style_prompt:{len(style_prompt)}')
    clothes_prompt = open(clothes_prompt_file, 'r', encoding='UTF-8').read().split(',')
    print(f'clothes_prompt:{len(clothes_prompt)}')
    chest_prompt = open(chest_prompt_file, 'r', encoding='UTF-8').read().split(',')
    print(f'chest_prompt:{len(chest_prompt)}')
    expression_prompt = open(expression_prompt_file, 'r', encoding='UTF-8').read().split(',')
    print(f'expression_prompt:{len(expression_prompt)}')
    hair_prompt = open(hair_prompt_file, 'r', encoding='UTF-8').read().split(',')
    print(f'hair_prompt:{len(hair_prompt)}')
    sock_prompt = open(sock_prompt_file, 'r', encoding='UTF-8').read().split(',')
    print(f'sock_prompt:{len(sock_prompt)}')


def gen_prompt():
    random_number = random.random()
    print(random_number)
    return start_prompt + ',' \
        + style_prompt[int(random_number * len(style_prompt) - 1)] + ',' \
        + clothes_prompt[int(random_number * len(clothes_prompt) - 1)] + ',' \
        + chest_prompt[int(random_number * len(chest_prompt) - 1)] + ',' \
        + expression_prompt[int(random_number * len(expression_prompt) - 1)] + ',' \
        + hair_prompt[int(random_number * len(hair_prompt) - 1)] + ',' + lora_prompt
        # + sock_prompt[int(random_number * len(sock_prompt) - 1)]



if __name__ == '__main__':
    init_prompt()
    for i in range(30):
        tex2img(gen_prompt(), 20, 3)
        time.sleep(100)
