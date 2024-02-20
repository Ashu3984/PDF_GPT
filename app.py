import gradio as gr
import os
from gradio_ import interface
from preprocess_pdf import set_api_key, enable_api_box, add_text, generate_response, render_file

demo, api_key, change_api_key, chatbot, show_img, txt, submit_btn, btn = interface()

with demo:

    api_key.submit(set_api_key, inputs=[api_key], outputs=[api_key])

    change_api_key.click(enable_api_box, outputs=[api_key])

    btn.upload(render_file, inputs=[btn], outputs=[show_img])

    submit_btn.click(add_text, inputs=[chatbot, txt], outputs=[chatbot], queue=False).\
        success(generate_response, inputs=[chatbot, txt, btn], outputs=[chatbot,txt]).\
        success(render_file, inputs=[btn], outputs=[show_img])

if __name__ == "__main__":
    demo.launch()