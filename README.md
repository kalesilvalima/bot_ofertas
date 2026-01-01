# Bot Telegram - Monitor de Ofertas

Bot pessoal para monitorar grupos do Telegram e ser notificado quando encontrar produtos específicos em mensagens.

## Funcionalidades

- ✅ Monitora grupos específicos configurados pelo usuário
- ✅ Busca termos personalizados nas mensagens (case-insensitive)
- ✅ Encaminha automaticamente mensagens que contêm os termos
- ✅ Gerenciamento via comandos do Telegram
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
   - Entre no grupo que deseja monitorar
   - Envie o comando `/addgroup` no grupo
   - Repita para cada grupo que deseja monitorar

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

- `/addgroup` - Adiciona o grupo atual ao monitoramento
  - Use este comando dentro do grupo que deseja monitorar
  
- `/remgroup` - Remove o grupo atual do monitoramento
  
- `/listgroups` - Lista todos os grupos monitorados

### Outros

- `/start` ou `/help` - Mostra a mensagem de ajuda

## Como Funciona

1. O bot monitora todos os grupos que você adicionou via `/addgroup`
2. Quando uma nova mensagem é recebida em um grupo monitorado, o bot verifica se o texto contém algum dos termos configurados
3. A busca é **case-insensitive** e **parcial** (procura se o termo está contido no texto)
4. Se encontrar correspondência, a mensagem é automaticamente encaminhada para você (mensagem privada)

## Arquivos de Configuração

- `config.json` - Armazena termos de busca, grupos monitorados e ID do usuário (criado automaticamente)
- `.env` - Armazena credenciais da API (não commite este arquivo!)
- `bot_ofertas_session.session` - Arquivo de sessão do Telegram (criado automaticamente)

## Notas Importantes

- ⚠️ Este bot usa a **Telegram Client API**, não a Bot API. Ele funciona como uma sessão da sua conta pessoal.
- ⚠️ O bot precisa estar rodando para monitorar mensagens (não funciona como um serviço em nuvem)
- ⚠️ Mantenha o arquivo `.env` e `*.session` seguros e não os compartilhe
- ✅ A busca é case-insensitive: "iphone", "iPhone" e "IPHONE" são tratados igualmente
- ✅ A busca é parcial: se você buscar "iPhone", encontrará "iPhone 14", "iPhone 15 Pro", etc.

## Solução de Problemas

**Erro ao conectar:**
- Verifique se `API_ID` e `API_HASH` estão corretos no arquivo `.env`
- Certifique-se de que tem conexão com a internet

**Bot não encontra termos:**
- Verifique se os grupos foram adicionados com `/addgroup`
- Verifique se os termos foram adicionados com `/listterms`
- Lembre-se que a busca é case-insensitive mas precisa estar contida no texto

**Mensagens não são encaminhadas:**
- Verifique se o bot está rodando
- Verifique os logs para erros
- Certifique-se de que você tem permissão para receber mensagens privadas

## Licença

Este projeto é para uso pessoal.

