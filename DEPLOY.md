# Guia de Deploy Remoto

Este guia explica como fazer deploy do bot em plataformas cloud para executar 24/7 sem precisar manter seu computador ligado.

## 📋 Pré-requisitos

- Conta no Telegram com API credentials (API_ID e API_HASH)
- Conta em uma das plataformas cloud (Railway, Render ou Heroku)
- Repositório Git (opcional, mas recomendado)

## 🚀 Plataformas Disponíveis

### 1. Railway (Recomendado) ⭐

**Vantagens:**
- Setup muito simples
- Volumes persistentes gratuitos
- Preço acessível ($5/mês após créditos gratuitos)
- Deploy automático via Git

**Passo a Passo:**

1. **Criar conta e projeto:**
   - Acesse https://railway.app
   - Faça login com GitHub
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo" (ou "Empty Project" para upload manual)

2. **Configurar variáveis de ambiente:**
   - No projeto, vá em "Variables"
   - Adicione:
     - `API_ID`: Seu API ID do Telegram
     - `API_HASH`: Seu API Hash do Telegram

3. **Configurar deploy:**
   - Se conectou via GitHub, o Railway detecta automaticamente
   - Ou configure manualmente:
     - Service Type: "Web Service"
     - Build Command: (deixe vazio, Railway detecta automaticamente)
     - Start Command: `python main.py`

4. **Configurar volume persistente:**
   - Vá em "Settings" > "Volumes"
   - Adicione um volume:
     - Path: `/app/data`
     - Mount Path: `/app`
   - Isso garante que o arquivo `.session` seja mantido

5. **Primeira autenticação:**
   - Após o deploy, acesse "Logs"
   - O bot solicitará código de verificação
   - Digite o código quando solicitado nos logs
   - Se pedir senha 2FA, digite também

6. **Monitoramento:**
   - Acesse "Logs" para ver atividade do bot
   - O bot reinicia automaticamente se cair

**Custo:** $5/mês após $5 de créditos gratuitos

---

### 2. Render

**Vantagens:**
- Plano gratuito disponível (com limitações)
- Fácil setup
- Deploy automático via Git

**Limitações do plano gratuito:**
- Serviço "dorme" após 15 minutos de inatividade
- Pode não ser ideal para bot que precisa estar sempre ativo

**Passo a Passo:**

1. **Criar conta:**
   - Acesse https://render.com
   - Faça login com GitHub

2. **Criar Web Service:**
   - Clique em "New" > "Web Service"
   - Conecte seu repositório GitHub
   - Configure:
     - **Name**: bot-ofertas (ou outro nome)
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`
     - **Plan**: Free (ou Paid para sempre ativo)

3. **Configurar variáveis de ambiente:**
   - Vá em "Environment"
   - Adicione:
     - `API_ID`: Seu API ID
     - `API_HASH`: Seu API Hash

4. **Configurar volume persistente (apenas Paid):**
   - Vá em "Settings" > "Persistent Disk"
   - Adicione disco persistente
   - Mount Path: `/app/data`

5. **Deploy e autenticação:**
   - Clique em "Manual Deploy"
   - Acesse "Logs" para ver código de verificação
   - Autentique quando solicitado

**Custo:** Gratuito (com limitações) ou $7/mês (sempre ativo)

---

### 3. Heroku

**Vantagens:**
- Plataforma estabelecida
- Boa documentação

**Desvantagens:**
- Requer cartão de crédito (mesmo para plano gratuito)
- Plano gratuito foi descontinuado

**Passo a Passo:**

1. **Instalar Heroku CLI:**
   ```bash
   # Windows (com Chocolatey)
   choco install heroku-cli
   
   # Ou baixe de: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login e criar app:**
   ```bash
   heroku login
   heroku create bot-ofertas
   ```

3. **Configurar variáveis:**
   ```bash
   heroku config:set API_ID=seu_api_id
   heroku config:set API_HASH=seu_api_hash
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Ver logs e autenticar:**
   ```bash
   heroku logs --tail
   # Digite código de verificação quando solicitado
   ```

6. **Configurar dyno:**
   - No dashboard do Heroku, vá em "Resources"
   - Certifique-se que o dyno está ativo

**Custo:** $7/mês (Eco Dyno)

---

## 🔐 Configuração de Variáveis de Ambiente

Todas as plataformas precisam das seguintes variáveis:

- `API_ID`: Seu API ID do Telegram (obtenha em https://my.telegram.org/apps)
- `API_HASH`: Seu API Hash do Telegram

**Importante:** NUNCA commite essas credenciais no Git!

---

## 📁 Persistência de Sessão

O arquivo `.session` contém a autenticação do bot. É crucial mantê-lo entre reinicializações:

### Railway
- Configure volume em `/app/data` ou `/app`
- O arquivo será mantido automaticamente

### Render (Paid)
- Use Persistent Disk
- Mount em `/app/data`

### Heroku
- Use Heroku Postgres ou addon de storage
- Ou configure para salvar em diretório persistente

---

## 🔄 Transferir Sessão Existente

Se você já tem uma sessão local e quer usar no servidor remoto:

1. **Copie o arquivo de sessão:**
   - Local: `bot_ofertas_session.session`
   - Copie para o servidor (via SSH ou interface da plataforma)

2. **No servidor remoto:**
   - Coloque o arquivo no diretório de trabalho
   - Certifique-se que tem permissões corretas

3. **Reinicie o serviço**

**Nota:** Algumas plataformas permitem upload via interface web ou CLI.

---

## 📊 Monitoramento e Logs

### Railway
- Acesse "Logs" no dashboard
- Logs em tempo real
- Histórico disponível

### Render
- Acesse "Logs" no dashboard
- Logs em tempo real
- Histórico limitado no plano gratuito

### Heroku
```bash
heroku logs --tail
heroku logs --num 1000  # Últimas 1000 linhas
```

---

## 🐛 Troubleshooting

### Bot não inicia

**Verifique:**
- Variáveis de ambiente estão configuradas corretamente
- Logs mostram algum erro específico
- Dependências foram instaladas corretamente

### Sessão perdida após reiniciar

**Solução:**
- Configure volume persistente
- Certifique-se que o arquivo `.session` está sendo salvo
- Verifique permissões do diretório

### Bot não recebe mensagens

**Verifique:**
- Bot está rodando (veja logs)
- Sessão está autenticada
- Grupos foram adicionados corretamente
- Termos de busca foram configurados

### Erro de autenticação

**Solução:**
- Acesse logs do servidor
- Digite código de verificação quando solicitado
- Se pedir senha 2FA, digite também
- Certifique-se que o terminal/logs aceitam input

### Bot para de funcionar

**Possíveis causas:**
- Servidor reiniciou e sessão foi perdida
- Erro não tratado causou crash
- Limite de recursos atingido

**Solução:**
- Configure auto-restart na plataforma
- Verifique logs para erros
- Configure alertas (se disponível)

---

## 💡 Dicas

1. **Teste localmente primeiro:**
   - Certifique-se que tudo funciona antes de fazer deploy

2. **Use Git:**
   - Facilita deploy e versionamento
   - Railway e Render fazem deploy automático

3. **Monitore logs:**
   - Verifique periodicamente se está funcionando
   - Configure alertas se possível

4. **Backup da sessão:**
   - Faça backup do arquivo `.session` periodicamente
   - Facilita recuperação em caso de problema

5. **Variáveis sensíveis:**
   - Nunca commite `.env` ou arquivos de sessão
   - Use variáveis de ambiente da plataforma

---

## 📝 Checklist de Deploy

- [ ] Conta criada na plataforma escolhida
- [ ] Variáveis de ambiente configuradas (API_ID, API_HASH)
- [ ] Repositório conectado (se usando Git)
- [ ] Volume persistente configurado (para sessão)
- [ ] Deploy realizado
- [ ] Autenticação concluída (código de verificação)
- [ ] Bot está rodando (verificar logs)
- [ ] Grupos adicionados via comandos
- [ ] Termos de busca configurados
- [ ] Teste: enviar mensagem de teste em grupo monitorado
- [ ] Monitoramento configurado

---

## 🔗 Links Úteis

- **Telegram API**: https://my.telegram.org/apps
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Heroku**: https://heroku.com
- **Documentação Telethon**: https://docs.telethon.dev

---

## ❓ Suporte

Se encontrar problemas:

1. Verifique os logs da plataforma
2. Consulte a documentação da plataforma escolhida
3. Verifique se todas as variáveis estão configuradas
4. Teste localmente para isolar o problema

---

**Boa sorte com o deploy! 🚀**

