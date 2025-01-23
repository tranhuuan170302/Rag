from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from Rag.reflection_agent_history import ReflectionAgentHistory
import re
from dotenv import load_dotenv
import os
load_dotenv()
class Model_Chat:

    def __init__(self):
        self.token = os.environ.get("API_TOKEN")
        self.llm = ChatOpenAI(api_key=self.token)
        self.memory = ConversationBufferMemory(memory_key="history")
        self.conversation_history = []

    def model_retrivel(self, user_message: str, results: str) -> str:
        """
            the function retrive knowledge in data store
        """
        if (results == ""):
            prompt_retrive = PromptTemplate(
                input_variables=["user_message"],
                template=f"""Bạn không tìm thấy dữ liệu để trả lời câu hỏi khách hàng. 
                            Hãy tạo một câu trả lời chung và đặt thêm một câu hỏi để thu thập thông tin.  

                            Câu hỏi từ khách hàng:  
                            "{user_message}"  

                            Trả lời: Một câu trả lời chung kèm câu hỏi dẫn dắt."""
            )
        else:
            prompt_retrive = PromptTemplate(
                input_variables=["user_message", "results"],
                template=f"""Bạn là một trợ lý AI thông minh, thân thiện, và chuyên nghiệp. 
                            Dựa trên thông tin truy xuất từ cơ sở dữ liệu, hãy tạo một câu trả lời **hoàn chỉnh, 
                            dễ hiểu, và thân thiện với khách hàng**.  

                            ### Quy tắc:  
                            1. Chỉ sử dụng dữ liệu truy xuất được.  
                            2. Nếu dữ liệu không đủ, hãy đưa ra một câu trả lời chung và đặt một câu hỏi để dẫn dắt khách hàng cung cấp thêm thông tin.  

                            ### Dữ liệu truy xuất:  
                            {results}  

                            ### Câu hỏi từ khách hàng:  
                            "{user_message}"  

                            ### Trả lời:  
                            Hãy cung cấp một câu trả lời rõ ràng, phù hợp với câu hỏi khách hàng và sử dụng thông tin từ dữ liệu trên (luôn phải có đường dẫn đính kèm cho khách hàng).
                        
                        """)

        get_message = self.llm.invoke(prompt_retrive.format(user_message=user_message, results=results))

        # save conversation in history
        data_history = {
            "user": user_message,                           # the question from user
            "assistant": get_message.content                # the answer from model
        }
        self.conversation_history.append(data_history)      # append to history
        return get_message.content
    
    def model_reflection(self, user_message: str) -> str: 
        
        clarification_prompt = PromptTemplate(
            input_variable=["history", "user_message"],
            template="""
                    Bạn là một trợ lý AI thông minh và nhạy bén, 
                    có nhiệm vụ hiểu ngữ cảnh dựa trên toàn bộ cuộc hội thoại trước đó để phản hồi chính xác và tự nhiên.  
                    Dựa trên các tin nhắn trước, hãy xác định ý định hoặc nhu cầu của khách hàng. 
                    Sau đó, đặt một câu hỏi phù hợp để dẫn dắt khách hàng tiếp tục cung cấp thông tin hoặc làm rõ thêm.  

                    Cuộc hội thoại về:  
                    {history}  

                    Tin nhắn cuối cùng từ khách hàng: "{user_message}"  

                    Hãy trả lời bằng cách đặt một câu hỏi phù hợp dựa trên ý định trong ngữ cảnh cuộc hội thoại. Trả lời ngắn gôn, không giải thích.
            """
        )

        # agent = ReflectionAgentHistory(self.llm, self.memory)
        for entry in self.conversation_history:
            self.memory.chat_memory.add_user_message(entry["user"])
            if "assistant" in entry:
                self.memory.chat_memory.add_ai_message(entry["assistant"])
        
        history = self.memory.chat_memory.messages
        history_text = ""
        for msg in history:
            if msg.type == "human":
                history_text += f"User: {msg.content}\n"
            elif msg.type == "ai":
                history_text += f"Assistant: {msg.content}\n"

        prompt = clarification_prompt.format(history=history_text, user_message=user_message)
        clarified_message = self.llm.invoke(prompt)
        return clarified_message.content

    def model_classify(self, user_message: str):
        """
            the function classify the question into one of the following types:
                - Information request (Trả về thông tin)
                - Confirmation (Xác nhận)
                - Descriptive (Mô tả)
                - Request (Yêu cầu)
                - Instruction (Hướng dẫn)
            the output is a json file with the following format:
                {
                    "type": str,
                    "message": str
                }
        """
        prompt_classify = PromptTemplate(
            input_variables=["user_message"],
            template=f"""Bạn là một chuyên gia xử lý ngôn ngữ tự nhiên. 
                        Nhiệm vụ của bạn là **phân loại câu đầu vào của khách hàng vào một trong các chủ đề dưới đây**.  
                        Các chủ đề gồm:  
                            + Thư viện - Sách 
                            + Nhà Cửa - Đời sống
                            + Điện thoại - Máy tính bảng 
                            + Đồ chơi - Trẻ em 
                            + Thiết bị số - Phụ kiện số 
                            + Điện gia dụng 
                            + Làm đẹp - sức khỏe 
                            + Ô Tô - Xe đạp - xe máy 
                            + Thời trang nữ
                            + Bách hóa Online
                            + Thể Thao - Giả ngoại 
                            + Hàng quốc tế 
                            + Laptop - phụ kiện máy tính

                        Đầu vào: "{user_message}"  

                        Hãy trả lời bằng một trong các chủ đề trên. Không cần giải thích.
                        """
        )

        formatted_prompt = prompt_classify.format(user_message=user_message)
        negotiate_classify = self.llm.invoke(formatted_prompt)
        data = {
            "category": negotiate_classify.content,
            "message": user_message
        }
        return data

    def model_generate(self, user_message: dict) -> str:
        """
            the function generate from LLM if the question is not in data store
        """
        prompt_classify = PromptTemplate(
            input_variables=["user_message"],
            template=f"""Bạn là một chuyên gia tư vấn bán hàng. Nhiệm vụ của bạn là 
                        **chỉ đặt một câu hỏi tương tác với khách hàng** để hướng họ về sản phẩm hoặc 
                        loại sản phẩm được chỉ định. Không cần giải thích dài dòng. \n

                        Đầu vào:  
                        - **Câu của khách hàng**: {user_message["message"]}  
                        - **Loại câu**: {user_message["category"]}  

                        Đầu ra:  
                        - Một câu hỏi dẫn dắt khách hàng, ví dụ: "Bạn đang tìm sản phẩm nào cụ thể trong [loại sản phẩm]?"  

                        Lưu ý: Trả lời ngắn gôn, chỉ đặt một câu hỏi phù hợp.

                        """
        )

        formatted_prompt = prompt_classify.format(user_message=user_message)
        negotiate_classify = self.llm.invoke(formatted_prompt)
        data_history = {
            "user": user_message['message'],                           # the question from user
            "assistant": negotiate_classify.content                    # the answer from model
        }
        self.conversation_history.append(data_history)

        return negotiate_classify.content

model_LLM = Model_Chat()

if __name__ == "__main__":
    llm = Model_Chat()

    # while True:

    #     user_input = input("Nhập câu hỏi:")
    #     answer = llm.model_classify(user_input)
    #     print(answer)
    #     if answer['category'] == "normal":
    #         qs = llm.model_generate(answer)
    #         print(qs)
    #     else:
    #         answer = llm.model_retrivel(answer['message'])
    #         print(answer)
    #         reflection = llm.model_reflection(user_input, answer)
    #         print(reflection)
        
    #     if user_input.lower() == "qw":
    #         break
    # print("End of conversation")