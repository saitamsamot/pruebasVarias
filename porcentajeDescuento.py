import requests
from bs4 import BeautifulSoup
import asyncio
import telegram

try:
    import telegram
except ImportError:
    print("La biblioteca de telegram no está instalada en Fastcron.")

try:
    import asyncio
except ImportError:
    print("La biblioteca de asyncio no está instalada en Fastcron.")
# Replace "YOUR_BOT_TOKEN" with your bot token received from BotFather
TOKEN = "6263545478:AAHyfj5peNRfyc9yITcAGPnvE6a4GLkdknw"

# Replace "CHAT_ID" with the chat_id of the chat where you want to send the message
CHAT_ID = "972332354"
bot = telegram.Bot(token=TOKEN)

url = 'https://www.paris.cl/electro/television/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
porcentaje_deseado = 20  # Porcentaje mínimo de descuento deseado
ofertas = soup.find_all('div', {'class': 'h-box-onecolumn'}) #Encontrar todas las ofertas en la págin

for recopilacion in ofertas:
    pD = recopilacion.find('div', {'class': 'price__badge'})
    if pD is not None and int(pD.text.replace('%', '')) >= porcentaje_deseado and int(recopilacion.find('div', {'class': 'price__text'}).text.replace('$', '').replace('.', ''))<200000:
        marca = recopilacion.find('p', {'class': 'brand-product-plp'}).text
        titulo = recopilacion.find('span', {'class': 'ellipsis_text'}).text
        precio_oferta = recopilacion.find('div', {'class': 'price__text'}).text
        precio_normal = recopilacion.find('div', {'class': 'price__text-sm'}).text
        link = recopilacion.find('a', {'class': 'js-product-layer'})
        href_content = link.get('href')
        valor = recopilacion.find('div', {'class': 'price__text'}).text
        mensaje = f"Título: {titulo}\n\nMarca: {marca}\nPrecio oferta: {precio_oferta}\nPrecio normal: {precio_normal}\nDescuento: {pD.text}\nLink: https://www.paris.cl/+{href_content}\n----------------------------------------------------------------------"
        async def send_telegram_message():
            bot = telegram.Bot(token='6263545478:AAHyfj5peNRfyc9yITcAGPnvE6a4GLkdknw')
            chat_id = '972332354'
            message = mensaje
            await bot.send_message(chat_id=chat_id, text=message)

        asyncio.run(send_telegram_message())
