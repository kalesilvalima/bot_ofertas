#!/bin/bash
# Script de setup para Render
# Este script ajuda a configurar o projeto no Render

echo "🎨 Configurando projeto no Render..."
echo ""

# Verifica se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Arquivo main.py não encontrado"
    echo "   Execute este script no diretório do projeto"
    exit 1
fi

echo "✅ Estrutura do projeto verificada"
echo ""

echo "📋 Passos para configurar no Render:"
echo ""
echo "1. Acesse https://render.com e faça login"
echo ""
echo "2. Crie um novo Web Service:"
echo "   - Clique em 'New' > 'Web Service'"
echo "   - Conecte seu repositório GitHub"
echo ""
echo "3. Configure o serviço:"
echo "   - Name: bot-ofertas (ou outro nome)"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python main.py"
echo "   - Plan: Free ou Paid (recomendado Paid para sempre ativo)"
echo ""
echo "4. Configure variáveis de ambiente:"
echo "   - Vá em 'Environment'"
echo "   - Adicione:"
echo "     * API_ID: seu_api_id"
echo "     * API_HASH: seu_api_hash"
echo ""
echo "5. Configure Persistent Disk (apenas Paid):"
echo "   - Vá em 'Settings' > 'Persistent Disk'"
echo "   - Adicione disco persistente"
echo "   - Mount Path: /app/data"
echo ""
echo "6. Faça o deploy:"
echo "   - Clique em 'Manual Deploy'"
echo "   - Aguarde o build completar"
echo ""
echo "7. Autentique o bot:"
echo "   - Acesse 'Logs'"
echo "   - Digite o código de verificação quando solicitado"
echo ""

read -p "Pressione Enter quando tiver concluído os passos acima..."

echo ""
echo "✅ Setup concluído!"
echo "🔗 Dashboard: https://dashboard.render.com"

