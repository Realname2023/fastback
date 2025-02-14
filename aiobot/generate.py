from g4f.client import AsyncClient, Client
from g4f.Provider import OpenaiChat, Gemini
from foundation import about_products, about_company

client = AsyncClient(
    # provider=OpenaiChat,
    # image_provider=Gemini,
    # proxies="http://Eo3CZe:eZ3wHz@196.18.13.217:8000"
    # Add other parameters as needed
)


async def chat_with_gpt(user_message):
    prompt = f"""Ты виртуальный помощник компании.  Вот информация о компании: {about_company},
    Вот информация о продуктах компании: {about_products}
    Пользователь задал вопрос: "{user_message}".
    Ответь вежливо и профессионально."""
    response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"{prompt}"
        }], 
        # proxy= "http://Eo3CZe:eZ3wHz@196.18.13.217:8000",
        web_search = False)
    print(response)
    return response
