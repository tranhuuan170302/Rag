from langchain.chains import ConversationChain

class ReflectionAgentHistory:
    def __init__(self, llm, memory):
        self.conversation_history = ConversationChain(llm=llm, memory=memory)

    def reflection_with_history(self, question):
        response = self.conversation_history.predict(input=question)
        return response
