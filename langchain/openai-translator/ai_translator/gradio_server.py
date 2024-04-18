import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, LOG
from translator import PDFTranslator, TranslationConfig


def translation(input_file, style, source_language, target_language):
    LOG.debug(f"[翻译任务]\n源文件: {input_file.name}\n源语言: {source_language}\n目标语言: {target_language}")

    language_options = {
        "英语": "Engliash",
        "中文": "Chinese",
        "日文": "Japanese",
        "韩文": "Korean",
        "法语": "French",
        "德语": "German"
    }
    style_options = {"无": None,
                    "小说": "novel",
                     "新闻稿": "news release",
                     "戏剧": "drama",
                     "喜剧": "comedy"}

    output_file_path = Translator.translate_pdf(
        input_file.name, source_language=language_options[source_language]
        , target_language=language_options[target_language], style=style_options[style])

    return output_file_path

def launch_gradio():
    # 定义选项（显示值与实际值不同）
    language_options = ["英语", "中文", "日文", "韩文", "法语", "德语"]
    style_options = ["无","小说","新闻稿","戏剧","喜剧"]

    iface = gr.Interface(
        fn=translation,
        title="OpenAI-Translator v2.0(PDF 电子书翻译工具)",
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Dropdown(label="翻译风格", choices=style_options, value="无"),
            gr.Dropdown(label="源语言（默认：英文）", choices=language_options, value="英语"),
            gr.Dropdown(label="目标语言（默认：中文）", choices=language_options, value="中文")
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")

def initialize_translator():
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    config = TranslationConfig()
    config.initialize(args)    
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslator(config.model_name)


if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Gradio 服务
    launch_gradio()
