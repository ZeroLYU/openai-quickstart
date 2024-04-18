from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class QuestionCreateorChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", verbose: bool = True):
        # 生成问答任务指令始终由 System 角色承担
        template = (
            """你是一个专业的客服，我将以以下格式提供关键字以及回复内容，请思考理解并整理出10条相关客户问题，客户问题可以包含一个或多个关键字。
        【关键字】：
        【自动回复】："""
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        # 待翻译文本由 Human 角色输入
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        #
        chat = ChatOpenAI(model_name=model_name, temperature=0.2, verbose=verbose)
        self.chain = LLMChain(llm=chat, prompt=chat_prompt_template, verbose=verbose)
    def run(self, text: str) -> (str, bool):
        result = ""
        try:
            result = self.chain.run({
                "text": text
            })
        except Exception as e:
            return result, False
        return result, True

    def out_parase(self, text: str, other: str = ""):
        # 将文本按行分割
        lines = text.strip().split("\n")
        # 格式化问题并保存到一个list中
        formatted_questions = ["【客户问题】：" + line.split("：", 1)[1].strip() for line in lines]
        context = ""
        # 打印结果
        for question in formatted_questions:
            print(question + "\n" + other)
            context += question + "\n" + ((other + '\n\n') if other else "")
        return context

if __name__ == "__main__":
    qwChain = QuestionCreateorChain()
    result = qwChain.run('''
    【关键字】：账单
    【自动回复】：您好，您可以微信关注公众号'大家服务大厅'（微信号：djfwdt），首页选择：服务大厅→查询→账单查询 进行查询
    ''')
    if result[1]:
        print(result[0])
        print(qwChain.out_parase(text=result[0], other="【自动回复】：您好，您可以微信关注公众号'大家服务大厅'（微信号：djfwdt），首页选择：服务大厅→话费→电子发票 进行查询"))
