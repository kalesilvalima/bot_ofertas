"""
Módulo de monitoramento de mensagens.
Filtra mensagens dos grupos monitorados e verifica termos de busca.
"""
from telethon import events
from telethon.tl.types import User, Channel, Chat
import config
import logging

logger = logging.getLogger(__name__)


def contains_search_term(text: str, terms: list) -> bool:
    """
    Verifica se o texto contém algum dos termos de busca.
    Busca é case-insensitive e parcial.
    """
    if not text or not terms:
        return False
    
    text_lower = text.lower()
    for term in terms:
        if term.lower() in text_lower:
            return True
    return False


async def handle_new_message(event: events.NewMessage.Event):
    """
    Handler para novas mensagens.
    Verifica se a mensagem é de um grupo monitorado e contém termos de busca.
    """
    # Ignora mensagens próprias
    if event.message.out:
        return
    
    # Obtém informações do chat
    chat = await event.get_chat()
    
    # Ignora mensagens de conversas privadas (apenas grupos/canais)
    if isinstance(chat, User):
        return
    
    # Verifica se o grupo está sendo monitorado
    monitored_ids = config.get_monitored_group_ids()
    if chat.id not in monitored_ids:
        return
    
    # Obtém o texto da mensagem
    message_text = event.message.text or event.message.raw_text or ""
    
    # Se não houver texto, ignora (pode ser mídia sem legenda)
    if not message_text.strip():
        return
    
    # Verifica se contém algum termo de busca
    search_terms = config.get_search_terms()
    if not search_terms:
        return
    
    if contains_search_term(message_text, search_terms):
        # Obtém ID do usuário para encaminhar
        user_id = config.get_user_id()
        if not user_id:
            # Se não tiver user_id configurado, usa o próprio remetente
            user_id = event.client.get_me().id
            config.set_user_id(user_id)
        
        try:
            # Encaminha a mensagem para o usuário
            await event.client.forward_messages(user_id, event.message)
            
            # Log para debug
            group_title = getattr(chat, 'title', f'ID: {chat.id}')
            logger.info(f"Termo encontrado! Mensagem encaminhada do grupo: {group_title}")
            
        except Exception as e:
            logger.error(f"Erro ao encaminhar mensagem: {e}")

