from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

def create_user_info_canvas(member) -> BytesIO:
    # Configurações da imagem
    width, height = 800, 400
    background_color = (255, 255, 255)  # Branco
    text_color = (0, 0, 0)  # Preto

    # Criar imagem em branco
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Fonte para o texto
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Caminho para a fonte TTF
    font = ImageFont.truetype(font_path, 20)

    # Foto de Perfil (posição fixa)
    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)
    profile_image = Image.open(BytesIO(response.content))
    profile_image = profile_image.resize((100, 100))
    image.paste(profile_image, (50, 50))

    # Mention e ID
    draw.text((200, 50), f"Mention: {member.mention}", fill=text_color, font=font)
    draw.text((200, 80), f"ID: {member.id}", fill=text_color, font=font)

    # Badges (Exemplo fictício)
    badges = "🎉 🛡️ 🌟"
    draw.text((200, 110), f"Badges: {badges}", fill=text_color, font=font)

    # Conta Criada em e Ingressou no Servidor em
    draw.text((200, 140), f"Conta Criada em: {member.created_at.strftime('%d/%m/%Y')}", fill=text_color, font=font)
    draw.text((200, 170), f"Ingressou no Servidor em: {member.joined_at.strftime('%d/%m/%Y')}", fill=text_color, font=font)

    # Atualmente em Chamada / Último Canal Conectado
    voice_state = member.voice
    voice_channel = voice_state.channel.name if voice_state and voice_state.channel else "Não está em chamada no momento"
    draw.text((200, 200), f"Atualmente em Chamada em: {voice_channel}", fill=text_color, font=font)

    # Cargos
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    draw.text((200, 230), f"Cargos: {', '.join(roles)}", fill=text_color, font=font)

    # Salvar a imagem em um buffer
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
