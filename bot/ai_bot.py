import os
from decouple import config
from langchain_groq import ChatGroq
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import  ChatPromptTemplate , MessagesPlaceholder
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.messages import AIMessage , HumanMessage

os.environ["AI_BOT_WPP"] = config("AI_BOT_WPP")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = config("HUGGINGFACEHUB_API_TOKEN")

class AiBot: 
    def __init__(self): 
        self.__chat = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.environ["AI_BOT_WPP"])
        self.__retriver = self.__build_retriver()

    def __build_retriver(self) : 
        persist_dir = '/app/chroma-data'
        embedding = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2", 
                                                  task="feature-extraction",
                                                  huggingfacehub_api_token = os.environ["HUGGINGFACEHUB_API_TOKEN"],
                                                  )

        vector_store = (
            Chroma(embedding_function=embedding, persist_directory=persist_dir)
        )

        return vector_store.as_retriever(search_kwargs={'k': 5})
    
    def __build_message(self, history_message , question): 
        messages = []
        for message in history_message:
           message_class = HumanMessage if message.get('fromMe') else AIMessage
           messages.append(message_class(content=message.get('body')))
        
        messages.append(HumanMessage(content=question,))
        return messages


    def invoke(self, history_message, question): 
        try: 
            SYSTEM_TEMPLATE = """
                Responda às perguntas dos clientes com base no contexto abaixo:
                Você é um assistente especializado em atendimento aos cliente da loja
                de informática e eletrônica Tech Grow.
                Tire as dúvidas sobre produtos, serviços, prazos, garantias e suporte técnico dos clientes
                que entrarem em contato.
                Responda de forma natural, agradável e respeitosa.Seja direto nas respostas, com informações claras
                e diretas, evitando termos técnicos excessivos, explicando de forma simples quando necessário.Foque em ser
                natural e humanizado, como um diálogo comum entre duas pessoas. Leve em conta o historico de 
                mensagens anteriores com o cliente.
                <context>
                    {context}
                </context>
            """
            docs = self.__retriver.invoke(question)
            question_answering_prompt = ChatPromptTemplate.from_messages([
                (
                    'system',
                    SYSTEM_TEMPLATE
                ),
                MessagesPlaceholder(variable_name="message"),
            ])

            document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt)
            response = document_chain.invoke({
                'context': docs,
                'message': self.__build_message(history_message, question)
            })

            return response
        except Exception as e:
            print("Error invoking AI Bot", e)
            return "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde."