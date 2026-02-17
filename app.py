import gradio as gr
from diffusers import StableDiffusionPipeline
import torch

model_id = "stabilityai/sd-turbo"

# Detect device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model properly depending on device
if device == "cuda":
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16
    )
else:
    pipe = StableDiffusionPipeline.from_pretrained(model_id)

pipe = pipe.to(device)


def outfit_text_and_prompt(gender, occasion, weather, vibe, budget):

    text = f"""
✨ Outfit Suggestion ✨
👤 Gender: {gender}
🎯 Occasion: {occasion}
🌤 Weather: {weather}
🎨 Vibe: {vibe}
💰 Budget: {budget}
👗 Outfit Idea:
• Trendy {vibe} top
• Stylish bottom for {occasion}
• Matching footwear
• Minimal aesthetic accessories
"""

    prompt = f"""
full body fashion model, {gender}, {vibe} style,
outfit for {occasion}, suitable for {weather},
high quality, realistic, pinterest aesthetic
"""

    return text, prompt


def bot(gender, occasion, weather, vibe, budget):
    text, prompt = outfit_text_and_prompt(gender, occasion, weather, vibe, budget)

    image = pipe(
        prompt,
        num_inference_steps=4,
        guidance_scale=0
    ).images[0]

    return text, image


with gr.Blocks(theme=gr.themes.Soft(primary_hue="pink")) as demo:
    gr.Markdown("## 👗✨ AI Outfit Suggestion Bot")

    with gr.Row():
        gender = gr.Dropdown(["female", "male"], value="female", label="Gender")
        budget = gr.Dropdown(["low", "medium", "high"], value="medium", label="Budget")

    occasion = gr.Textbox(label="Occasion (mall, cafe date, college...)")
    weather = gr.Textbox(label="Weather (sunny, rainy, winter...)")
    vibe = gr.Textbox(label="Vibe (soft girl, streetwear, old money...)")

    btn = gr.Button("Generate Outfit 💖")

    out_text = gr.Textbox(label="Outfit Suggestion", lines=8)
    out_img = gr.Image(label="Generated Outfit")

    btn.click(
        bot,
        inputs=[gender, occasion, weather, vibe, budget],
        outputs=[out_text, out_img]
    )

demo.launch()
