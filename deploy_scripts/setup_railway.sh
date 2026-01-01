#!/bin/bash
# Script de setup para Railway
# Este script ajuda a configurar o projeto no Railway

echo "🚂 Configurando projeto no Railway..."
echo ""

# Verifica se Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "⚠️  Railway CLI não encontrado."
    echo "📥 Instale com: npm i -g @railway/cli"
    echo "   Ou configure manualmente no dashboard: https://railway.app"
    exit 1
fi

echo "✅ Railway CLI encontrado"
echo ""

# Verifica variáveis de ambiente
if [ -z "$API_ID" ] || [ -z "$API_HASH" ]; then
    echo "⚠️  Variáveis de ambiente não encontradas"
    echo ""
    echo "Configure as variáveis no Railway:"
    echo "  1. Acesse seu projeto no Railway"
    echo "  2. Vá em 'Variables'"
    echo "  3. Adicione:"
    echo "     - API_ID: seu_api_id"
    echo "     - API_HASH: seu_api_hash"
    echo ""
    read -p "Pressione Enter quando tiver configurado as variáveis..."
fi

echo ""
echo "📋 Checklist de configuração:"
echo "  [ ] Variáveis API_ID e API_HASH configuradas"
echo "  [ ] Deploy realizado"
echo "  [ ] Autenticação concluída (ver logs)"
echo ""
echo "ℹ️  Nota: A persistência de arquivos é automática no Railway."
echo "   O arquivo .session será mantido entre reinicializações."
echo ""
echo "🔗 Dashboard: https://railway.app"
echo ""
echo "✅ Setup concluído!"

