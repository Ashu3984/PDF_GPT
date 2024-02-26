import gradio as gr
import os

def interface():
    with gr.Blocks(title= " PDF Chatbot",theme = "Soft") as demo:
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=0.8):
                    api_key = gr.Textbox(
                        label='Enter your OpenAI API key',
                    type='password'
                    )
                    
                with gr.Column(scale=0.2):
                    change_api_key = gr.Button('Update API Key')

            with gr.Row():
                chatbot = gr.Chatbot(value=[], elem_id='chatbot', height=500)
                show_img = gr.Image(label='PDF Preview', height=500)

        with gr.Row():
            with gr.Column(scale=0.60):
                text_input = gr.Textbox(
                    show_label=False,
                    placeholder="Ask your pdf?",
                container=False)

            with gr.Column(scale=0.20):
                submit_btn = gr.Button('Send')

            with gr.Column(scale=0.20):
                upload_btn = gr.UploadButton("📁 Upload PDF", file_types=[".pdf"])
                

        return demo, api_key, change_api_key, chatbot, show_img, text_input, submit_btn, upload_btn

if __name__ == '__main__':
    demo, api_key, change_api_key, chatbot, show_img, text_input, submit_btn, upload_btn = interface()
    demo.queue()
    demo.launch()

    