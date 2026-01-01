"""
Bot Telegram para Monitoramento de Produtos
Monitora grupos específicos e notifica quando encontra termos de busca.
"""
import asyncio
import logging
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import User

import config
import commands
import monitor

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Credenciais da API do Telegram
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

if not API_ID or not API_HASH:
    logger.error("API_ID e API_HASH devem ser configurados no arquivo .env")
    exit(1)

# Nome da sessão (arquivo .session será criado automaticamente)
SESSION_NAME = 'bot_ofertas_session'


async def setup_user_id(client: TelegramClient):
    """Configura o ID do usuário se ainda não estiver configurado."""
    user_id = config.get_user_id()
    if not user_id:
        me = await client.get_me()
        config.set_user_id(me.id)
        logger.info(f"ID do usuário configurado: {me.id}")


async def main():
    """Função principal do bot."""
    # Cria cliente Telegram
    client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)
    
    try:
        # Conecta ao Telegram
        await client.start()
        logger.info("Conectado ao Telegram com sucesso!")
        
        # Configura ID do usuário
        await setup_user_id(client)
        
        # Registra handlers de comandos
        @client.on(events.NewMessage(pattern=r'^/start'))
        async def start_handler(event):
            await commands.handle_start(event)
        
        @client.on(events.NewMessage(pattern=r'^/addterm'))
        async def addterm_handler(event):
            await commands.handle_addterm(event)
        
        @client.on(events.NewMessage(pattern=r'^/remterm'))
        async def remterm_handler(event):
            await commands.handle_remterm(event)
        
        @client.on(events.NewMessage(pattern=r'^/listterms'))
        async def listterms_handler(event):
            await commands.handle_listterms(event)
        
        @client.on(events.NewMessage(pattern=r'^/addgroup'))
        async def addgroup_handler(event):
            await commands.handle_addgroup(event)
        
        @client.on(events.NewMessage(pattern=r'^/remgroup'))
        async def remgroup_handler(event):
            await commands.handle_remgroup(event)
        
        @client.on(events.NewMessage(pattern=r'^/listgroups'))
        async def listgroups_handler(event):
            await commands.handle_listgroups(event)
        
        @client.on(events.NewMessage(pattern=r'^/help'))
        async def help_handler(event):
            await commands.handle_help(event)
        
        # Registra handler de monitoramento de mensagens
        @client.on(events.NewMessage)
        async def message_handler(event):
            await monitor.handle_new_message(event)
        
        logger.info("Bot iniciado e pronto para monitorar!")
        logger.info(f"Termos ativos: {len(config.get_search_terms())}")
        logger.info(f"Grupos monitorados: {len(config.get_monitored_groups())}")
        
        # Mantém o bot rodando
        await client.run_until_disconnected()
        
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
    finally:
        await client.disconnect()
        logger.info("Desconectado do Telegram")


if __name__ == '__main__':
    asyncio.run(main())

