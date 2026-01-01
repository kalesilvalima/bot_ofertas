# Bot Telegram - Monitor de Ofertas

Bot pessoal para monitorar grupos do Telegram e ser notificado quando encontrar produtos específicos em mensagens.

## Funcionalidades

- ✅ Monitora grupos específicos configurados pelo usuário
- ✅ **Funciona mesmo em grupos onde você não pode enviar comandos ou usar bots**
- ✅ Busca termos personalizados nas mensagens (case-insensitive)
- ✅ Encaminha automaticamente mensagens que contêm os termos
- ✅ Gerenciamento via comandos do Telegram
- ✅ Lista todos os grupos/canais disponíveis para facilitar configuração
- ✅ Adiciona grupos por nome ou ID, sem precisar estar no grupo
- ✅ Configuração persistente em arquivo JSON

## Requisitos

- Python 3.7 ou superior
- Conta no Telegram
- Credenciais da API do Telegram (API ID e API Hash)

## Instalação

1. **Clone ou baixe este repositório**

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Obtenha suas credenciais da API do Telegram:**
   - Acesse https://my.telegram.org/apps
   - Faça login com sua conta do Telegram
   - Crie uma nova aplicação (se ainda não tiver)
   - Anote o `api_id` e `api_hash`

4. **Configure as credenciais:**
   - Copie o arquivo `env.example` para `.env`:
     ```bash
     copy env.example .env
     ```
   - Edite o arquivo `.env` e preencha com suas credenciais:
     ```
     API_ID=seu_api_id_aqui
     API_HASH=seu_api_hash_aqui
     ```

## Como Usar

1. **Inicie o bot:**
   ```bash
   python main.py
   ```

2. **Na primeira execução:**
   - Você receberá um código de verificação no Telegram
   - Digite o código no terminal quando solicitado
   - Se necessário, informe sua senha de 2FA

3. **Configure os grupos para monitorar:**
   
   **Opção 1 - Listar e adicionar por nome/ID (recomendado):**
   - Envie `/listallgroups` em uma conversa privada com você mesmo
   - Copie o nome ou ID do grupo desejado
   - Envie `/addgroup <nome>` ou `/addgroup <ID>` para adicionar
   - Exemplo: `/addgroup Ofertas do Dia` ou `/addgroup -1001234567890`
   
   **Opção 2 - Adicionar grupo atual:**
   - Entre no grupo que deseja monitorar
   - Envie o comando `/addgroup` no grupo (só funciona se você tiver permissão)

4. **Adicione termos de busca:**
   - Envie `/addterm <termo>` em qualquer conversa com você mesmo
   - Exemplo: `/addterm iPhone`
   - Exemplo: `/addterm notebook`
   - Você pode adicionar múltiplos termos

5. **Pronto!** O bot começará a monitorar automaticamente e encaminhar mensagens que contenham seus termos.

## Comandos Disponíveis

### Gerenciar Termos de Busca

- `/addterm <termo>` - Adiciona um termo de busca
  - Exemplo: `/addterm iPhone 14`
  
- `/remterm <termo>` - Remove um termo de busca
  - Exemplo: `/remterm iPhone 14`
  
- `/listterms` - Lista todos os termos ativos

### Gerenciar Grupos

- `/listallgroups` - Lista todos os grupos/canais que você participa
  - Mostra nome e ID de cada grupo para facilitar a adição
  - Use este comando primeiro para ver grupos disponíveis
  
- `/addgroup [nome ou ID]` - Adiciona um grupo ao monitoramento
  - **Sem parâmetro:** Adiciona o grupo atual (se você tiver permissão)
  - **Com nome:** `/addgroup Nome do Grupo` - Busca e adiciona pelo nome
  - **Com ID:** `/addgroup -1001234567890` - Adiciona diretamente pelo ID
  - **Funciona mesmo em grupos onde você não pode enviar comandos!**
  
- `/remgroup [nome ou ID]` - Remove um grupo do monitoramento
  - **Sem parâmetro:** Remove o grupo atual
  - **Com nome ou ID:** Remove o grupo especificado
  
- `/listgroups` - Lista todos os grupos monitorados

### Outros

- `/start` ou `/help` - Mostra a mensagem de ajuda

## Como Funciona

1. O bot monitora todos os grupos que você adicionou via `/addgroup` (por nome, ID ou grupo atual)
2. Quando uma nova mensagem é recebida em um grupo monitorado, o bot verifica se o texto contém algum dos termos configurados
3. A busca é **case-insensitive** e **parcial** (procura se o termo está contido no texto)
4. Se encontrar correspondência, a mensagem é automaticamente encaminhada para você (mensagem privada)
5. **O bot funciona mesmo em grupos onde você não tem permissão para enviar comandos** - você só precisa adicionar o grupo usando `/addgroup <nome>` ou `/addgroup <ID>` de uma conversa privada

## Arquivos de Configuração

- `config.json` - Armazena termos de busca, grupos monitorados e ID do usuário (criado automaticamente)
- `.env` - Armazena credenciais da API (não commite este arquivo!)
- `bot_ofertas_session.session` - Arquivo de sessão do Telegram (criado automaticamente)

## Deploy Remoto

Para executar o bot em um servidor remoto (cloud) e mantê-lo rodando 24/7, consulte o arquivo **[DEPLOY.md](DEPLOY.md)** que contém instruções detalhadas sobre:

- **Plataformas suportadas:** Railway (recomendado), Render, Heroku
- Configuração passo a passo para cada plataforma
- Como configurar variáveis de ambiente
- Persistência de sessão (arquivo `.session`)
- Primeira autenticação em ambiente remoto
- Monitoramento e logs remotos
- Troubleshooting comum

**Resumo rápido:**
1. Escolha uma plataforma (Railway é a mais simples)
2. Configure variáveis de ambiente (API_ID, API_HASH)
3. Faça o deploy (via Git ou upload)
4. Autentique na primeira execução (via logs)
5. Configure grupos e termos normalmente

**Vantagens do deploy remoto:**
- ✅ Bot roda 24/7 sem precisar manter computador ligado
- ✅ Acesso aos logs de qualquer lugar
- ✅ Reinicialização automática em caso de erro
- ✅ Mais confiável que execução local

## Notas Importantes

- ⚠️ Este bot usa a **Telegram Client API**, não a Bot API. Ele funciona como uma sessão da sua conta pessoal.
- ⚠️ O bot precisa estar rodando continuamente para monitorar mensagens (pode rodar localmente ou remotamente)
- ⚠️ Mantenha o arquivo `.env` e `*.session` seguros e não os compartilhe
- 💡 **Dica:** Para rodar 24/7, faça deploy em uma plataforma cloud (veja [DEPLOY.md](DEPLOY.md))
- ✅ **Funciona em grupos restritos:** Você pode monitorar grupos mesmo sem poder enviar comandos neles. Use `/listallgroups` e depois `/addgroup <nome>` ou `/addgroup <ID>`.
- ✅ A busca é case-insensitive: "iphone", "iPhone" e "IPHONE" são tratados igualmente
- ✅ A busca é parcial: se você buscar "iPhone", encontrará "iPhone 14", "iPhone 15 Pro", etc.

## Solução de Problemas

**Erro ao conectar:**
- Verifique se `API_ID` e `API_HASH` estão corretos no arquivo `.env`
- Certifique-se de que tem conexão com a internet

**Bot não encontra termos:**
- Verifique se os grupos foram adicionados com `/addgroup` (use `/listgroups` para confirmar)
- Verifique se os termos foram adicionados com `/listterms`
- Lembre-se que a busca é case-insensitive mas precisa estar contida no texto

**Não consigo adicionar um grupo:**
- Use `/listallgroups` para ver todos os grupos disponíveis
- Use `/addgroup <nome>` ou `/addgroup <ID>` de uma conversa privada
- O nome deve corresponder exatamente ou parcialmente ao nome do grupo
- Você pode adicionar grupos mesmo sem poder enviar comandos neles

**Mensagens não são encaminhadas:**
- Verifique se o bot está rodando
- Verifique os logs para erros
- Certifique-se de que você tem permissão para receber mensagens privadas

## Licença

Este projeto é para uso pessoal.

