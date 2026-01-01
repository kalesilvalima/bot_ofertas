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
`/addgroup [nome ou ID]` - Adiciona um grupo ao monitoramento (use sem parâmetro no grupo ou com nome/ID)
`/remgroup [nome ou ID]` - Remove um grupo do monitoramento
`/listgroups` - Lista todos os grupos monitorados
`/listallgroups` - Lista todos os grupos/canais que você participa

ℹ️ **Outros:**
`/help` - Mostra esta mensagem de ajuda

**Como usar:**
1. Use `/listallgroups` para ver todos os grupos disponíveis
2. Use `/addgroup <nome>` ou `/addgroup <ID>` para adicionar grupos ao monitoramento
3. Use `/addterm` para adicionar termos de busca (ex: "iPhone", "notebook")
4. O bot encaminhará automaticamente mensagens que contenham esses termos

**Nota:** Funciona mesmo em grupos onde você não pode enviar comandos!
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
    message_text = event.message.text
    parts = message_text.split(maxsplit=1)
    
    # Se não tiver parâmetro, tenta usar o grupo atual
    if len(parts) < 2:
        chat = await event.get_chat()
        
        if isinstance(chat, User):
            await event.respond("❌ Use: `/addgroup <nome do grupo>` ou `/addgroup <ID>`\nOu use `/listallgroups` para ver grupos disponíveis.", parse_mode='markdown')
            return
        
        group_id = chat.id
        group_title = getattr(chat, 'title', 'Grupo sem título')
        
        if config.add_monitored_group(group_id, group_title):
            await event.respond(f"✅ Grupo '{group_title}' adicionado ao monitoramento!")
        else:
            await event.respond(f"⚠️ O grupo '{group_title}' já está sendo monitorado.")
        return
    
    # Se tiver parâmetro, busca o grupo por nome ou ID
    search_param = parts[1].strip()
    
    try:
        # Tenta como ID primeiro
        group_id = int(search_param)
        # Busca o grupo pelo ID
        try:
            chat = await event.client.get_entity(group_id)
            if isinstance(chat, User):
                await event.respond("❌ O ID fornecido não é de um grupo ou canal.")
                return
            group_title = getattr(chat, 'title', f'ID: {group_id}')
            group_id = chat.id
        except Exception:
            await event.respond(f"❌ Não foi possível encontrar o grupo com ID: {group_id}")
            return
    except ValueError:
        # Não é um ID, busca por nome
        group_title = search_param
        group_id = None
        
        # Busca em todos os diálogos
        async for dialog in event.client.iter_dialogs():
            if not isinstance(dialog.entity, User):
                dialog_title = getattr(dialog.entity, 'title', '')
                if search_param.lower() in dialog_title.lower():
                    group_id = dialog.entity.id
                    group_title = dialog_title
                    break
        
        if group_id is None:
            await event.respond(f"❌ Grupo '{search_param}' não encontrado.\nUse `/listallgroups` para ver grupos disponíveis.", parse_mode='markdown')
            return
    
    # Adiciona o grupo
    if config.add_monitored_group(group_id, group_title):
        await event.respond(f"✅ Grupo '{group_title}' (ID: {group_id}) adicionado ao monitoramento!")
    else:
        await event.respond(f"⚠️ O grupo '{group_title}' já está sendo monitorado.")


async def handle_remgroup(event: events.NewMessage.Event):
    """Handler para o comando /remgroup."""
    message_text = event.message.text
    parts = message_text.split(maxsplit=1)
    
    # Se não tiver parâmetro, tenta usar o grupo atual
    if len(parts) < 2:
        chat = await event.get_chat()
        
        if isinstance(chat, User):
            await event.respond("❌ Use: `/remgroup <nome do grupo>` ou `/remgroup <ID>`\nOu use `/listgroups` para ver grupos monitorados.", parse_mode='markdown')
            return
        
        group_id = chat.id
        group_title = getattr(chat, 'title', 'Grupo sem título')
        
        if config.remove_monitored_group(group_id):
            await event.respond(f"✅ Grupo '{group_title}' removido do monitoramento!")
        else:
            await event.respond(f"⚠️ O grupo '{group_title}' não está sendo monitorado.")
        return
    
    # Se tiver parâmetro, busca o grupo por nome ou ID
    search_param = parts[1].strip()
    
    # Busca nos grupos monitorados
    monitored_groups = config.get_monitored_groups()
    found_group = None
    
    try:
        # Tenta como ID
        search_id = int(search_param)
        for group in monitored_groups:
            if group["id"] == search_id:
                found_group = group
                break
    except ValueError:
        # Busca por nome
        for group in monitored_groups:
            if search_param.lower() in group.get("title", "").lower():
                found_group = group
                break
    
    if not found_group:
        await event.respond(f"❌ Grupo '{search_param}' não encontrado nos grupos monitorados.\nUse `/listgroups` para ver grupos monitorados.", parse_mode='markdown')
        return
    
    if config.remove_monitored_group(found_group["id"]):
        await event.respond(f"✅ Grupo '{found_group.get('title', 'ID: ' + str(found_group['id']))}' removido do monitoramento!")
    else:
        await event.respond(f"⚠️ Erro ao remover o grupo.")


async def handle_listgroups(event: events.NewMessage.Event):
    """Handler para o comando /listgroups."""
    groups = config.get_monitored_groups()
    
    if not groups:
        await event.respond("👥 Nenhum grupo sendo monitorado.\nUse `/addgroup` em um grupo para adicioná-lo.", parse_mode='markdown')
        return
    
    groups_list = "\n".join([f"• {g.get('title', 'ID: ' + str(g['id']))}" for g in groups])
    await event.respond(f"👥 **Grupos monitorados:**\n\n{groups_list}", parse_mode='markdown')


async def handle_listallgroups(event: events.NewMessage.Event):
    """Handler para o comando /listallgroups - lista todos os grupos/canais disponíveis."""
    groups_list = []
    count = 0
    
    try:
        async for dialog in event.client.iter_dialogs(limit=200):
            if not isinstance(dialog.entity, User):
                count += 1
                group_title = getattr(dialog.entity, 'title', f'ID: {dialog.entity.id}')
                group_id = dialog.entity.id
                groups_list.append(f"• {group_title} (ID: {group_id})")
                
                # Limita a 50 grupos na mensagem para não exceder o limite
                if count >= 50:
                    break
        
        if not groups_list:
            await event.respond("👥 Nenhum grupo ou canal encontrado.")
            return
        
        groups_text = "\n".join(groups_list)
        if count >= 50:
            groups_text += f"\n\n⚠️ Mostrando apenas os primeiros 50 grupos de {count} encontrados."
        
        await event.respond(f"👥 **Grupos e Canais disponíveis:**\n\n{groups_text}\n\nUse `/addgroup <nome>` ou `/addgroup <ID>` para adicionar ao monitoramento.", parse_mode='markdown')
        
    except Exception as e:
        await event.respond(f"❌ Erro ao listar grupos: {e}")


async def handle_help(event: events.NewMessage.Event):
    """Handler para o comando /help."""
    await handle_start(event)

