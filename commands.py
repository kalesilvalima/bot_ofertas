"""
Módulo de handlers de comandos do Telegram.
Gerencia todos os comandos disponíveis para o usuário.
"""
from telethon import events
from telethon.tl.types import User, Channel, Chat
import config


async def handle_start(event: events.NewMessage.Event):
    """Handler para o comando /start."""
    help_text = """
🤖 **Bot Monitor de Ofertas**

Este bot monitora grupos do Telegram e te notifica quando encontrar produtos específicos.

**Comandos disponíveis:**

📝 **Gerenciar Termos:**
`/addterm <termo>` - Adiciona um termo de busca
`/remterm <termo>` - Remove um termo de busca
`/listterms` - Lista todos os termos ativos

👥 **Gerenciar Grupos:**
`/addgroup` - Adiciona o grupo atual ao monitoramento
`/remgroup` - Remove o grupo atual do monitoramento
`/listgroups` - Lista todos os grupos monitorados

ℹ️ **Outros:**
`/help` - Mostra esta mensagem de ajuda

**Como usar:**
1. Use `/addgroup` nos grupos que você quer monitorar
2. Use `/addterm` para adicionar termos de busca (ex: "iPhone", "notebook")
3. O bot encaminhará automaticamente mensagens que contenham esses termos
"""
    await event.respond(help_text, parse_mode='markdown')


async def handle_addterm(event: events.NewMessage.Event):
    """Handler para o comando /addterm."""
    message_text = event.message.text
    parts = message_text.split(maxsplit=1)
    
    if len(parts) < 2:
        await event.respond("❌ Uso: `/addterm <termo>`\nExemplo: `/addterm iPhone`", parse_mode='markdown')
        return
    
    term = parts[1].strip()
    if config.add_search_term(term):
        await event.respond(f"✅ Termo '{term}' adicionado com sucesso!")
    else:
        await event.respond(f"⚠️ O termo '{term}' já existe ou é inválido.")


async def handle_remterm(event: events.NewMessage.Event):
    """Handler para o comando /remterm."""
    message_text = event.message.text
    parts = message_text.split(maxsplit=1)
    
    if len(parts) < 2:
        await event.respond("❌ Uso: `/remterm <termo>`\nExemplo: `/remterm iPhone`", parse_mode='markdown')
        return
    
    term = parts[1].strip()
    if config.remove_search_term(term):
        await event.respond(f"✅ Termo '{term}' removido com sucesso!")
    else:
        await event.respond(f"⚠️ O termo '{term}' não foi encontrado.")


async def handle_listterms(event: events.NewMessage.Event):
    """Handler para o comando /listterms."""
    terms = config.get_search_terms()
    
    if not terms:
        await event.respond("📝 Nenhum termo configurado.\nUse `/addterm <termo>` para adicionar.", parse_mode='markdown')
        return
    
    terms_list = "\n".join([f"• {term}" for term in terms])
    await event.respond(f"📝 **Termos de busca ativos:**\n\n{terms_list}", parse_mode='markdown')


async def handle_addgroup(event: events.NewMessage.Event):
    """Handler para o comando /addgroup."""
    chat = await event.get_chat()
    
    if isinstance(chat, User):
        await event.respond("❌ Este comando só funciona em grupos ou canais.")
        return
    
    group_id = chat.id
    group_title = getattr(chat, 'title', 'Grupo sem título')
    
    if config.add_monitored_group(group_id, group_title):
        await event.respond(f"✅ Grupo '{group_title}' adicionado ao monitoramento!")
    else:
        await event.respond(f"⚠️ O grupo '{group_title}' já está sendo monitorado.")


async def handle_remgroup(event: events.NewMessage.Event):
    """Handler para o comando /remgroup."""
    chat = await event.get_chat()
    
    if isinstance(chat, User):
        await event.respond("❌ Este comando só funciona em grupos ou canais.")
        return
    
    group_id = chat.id
    group_title = getattr(chat, 'title', 'Grupo sem título')
    
    if config.remove_monitored_group(group_id):
        await event.respond(f"✅ Grupo '{group_title}' removido do monitoramento!")
    else:
        await event.respond(f"⚠️ O grupo '{group_title}' não está sendo monitorado.")


async def handle_listgroups(event: events.NewMessage.Event):
    """Handler para o comando /listgroups."""
    groups = config.get_monitored_groups()
    
    if not groups:
        await event.respond("👥 Nenhum grupo sendo monitorado.\nUse `/addgroup` em um grupo para adicioná-lo.", parse_mode='markdown')
        return
    
    groups_list = "\n".join([f"• {g.get('title', 'ID: ' + str(g['id']))}" for g in groups])
    await event.respond(f"👥 **Grupos monitorados:**\n\n{groups_list}", parse_mode='markdown')


async def handle_help(event: events.NewMessage.Event):
    """Handler para o comando /help."""
    await handle_start(event)

