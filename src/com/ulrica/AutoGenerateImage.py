import base64
import os
import time
from io import BytesIO

import requests
from PIL import Image

domain = 'http://localhost:7860'
# txt2img_output = '/content/stable-diffusion-webui/output/txt2image/20230413111'
txt2img_output = 'F:\\SDAI\\stable-diffusion-webui\\outputs\\txt2img-images\\auto'
img2img_output = '/content/stable-diffusion-webui/output/img2image/20230413111'
final_output = '/content/stable-diffusion-webui/output/final/20230413111'

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
    "height": 432,
    "restore_faces": True,
    "tiling": False,
    "do_not_save_samples": False,
    "do_not_save_grid": False,
    "negative_prompt": "lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet",
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
    print(r)
    print('=============================== txt2img get result,begin save img=================================== ')

    if not os.path.exists(txt2img_output):
        os.makedirs(txt2img_output)
    for i in r['images']:
        image = Image.open(BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        # response2 = requests.post(url=f'{domain}/sdapi/v1/png-info', json=png_payload)

        # pnginfo = PngImagePlugin.PngInfo()
        # pnginfo.add_text("parameters", response2.json().get("info"))
        # image.save(os.path.join(txt2img_output, f'{time.time()}.png'), pnginfo=pnginfo)
        image.save(os.path.join(txt2img_output, f'{time.time()}.jpg'))

    print('===============================txt2img end=================================== output is :', txt2img_output)


if __name__ == '__main__':
    for i in range(10):
        prompt = '(8k, RAW photo, best quality, masterpiece:1.2), (realistic, photo-realistic:1.37), ultra-detailed, 1 girl,cute, solo,beautiful detailed sky,detailed cafe,night,sitting,dating,(nose blush),(smile:1.1),(closed mouth) medium breasts,beautiful detailed eyes,(collared shirt:1.1), bowtie,pleated skirt,(short hair:1.2),floating hair,<lora:japaneseDollLikeness_v10:0.2>,<lora:koreanDollLikeness_v15:0.3>,<lora:taiwanDollLikeness_v10:0.3>'
        tex2img(prompt, 30, 4)
        time.sleep(300)
