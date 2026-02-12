import requests
import json
import os
from datetime import datetime, date

# Configurações
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# LISTA DIRETA das suas entregas - EDITAVE AQUI! ✏️
ENTREGAS = [
    {"disciplina": "Gestão de Projetos", "atividade": "Atividades e prova", "data_entrega": "2026-03-01"},
    {"disciplina": "Tópicos Especiais em Design de Animação I", "atividade": "Atividades e prova", "data_entrega": "2026-06-01"},
    {"disciplina": "Temas Transversais", "atividade": "Atividades e prova", "data_entrega": "2026-06-16"},
    {"disciplina": "Projeto Integrado em Design de Animação Game", "atividade": "Projeto", "data_entrega": "2026-05-25"},
    {"disciplina": "Design de Cenários e Personagens", "atividade": "Atividades e Prova", "data_entrega": "2026-04-01"},
    {"disciplina": "Motion Design", "atividade": "Atividades e Prova", "data_entrega": "2026-05-01"},
    {"disciplina": "Linguagem Fotográfica", "atividade": "Atividades e Prova", "data_entrega": "2026-06-01"},
    {"disciplina": "Design Sustentável e Responsabilidade Social", "atividade": "Atividades e Prova", "data_entrega": "2026-06-01"},
    {"disciplina": "Estética e Linguagem Audiovisual", "atividade": "Atividades e Prova", "data_entrega": "2026-06-01"},
]


def check_entregas():
    mensagens = []
    hoje = date.today()
    
    for entrega in ENTREGAS:
        data_entrega = datetime.strptime(entrega['data_entrega'], '%Y-%m-%d').date()
        dias_restantes = (data_entrega - hoje).days
        
        if dias_restantes <= 14:  # Alertar para entregas em até 14 dias
            cor = 0xFF0000 if dias_restantes <= 2 else 0xFFA500 if dias_restantes <= 7 else 0xFFFF00
            
            mensagem = {
                "embeds": [{
                    "title": "📚 LEMBRETE DE ENTREGA",
                    "color": cor,
                    "fields": [
                        {"name": "Disciplina", "value": entrega['disciplina'], "inline": True},
                        {"name": "Atividade", "value": entrega['atividade'], "inline": True},
                        {"name": "Data de Entrega", "value": entrega['data_entrega'], "inline": True},
                        {"name": "Dias Restantes", "value": f"⏳ {dias_restantes} dias", "inline": True}
                    ],
                    "footer": {"text": "Bot de Entregas da Karen"}
                }]
            }
            mensagens.append(mensagem)
    
    return mensagens

def enviar_webhook(mensagens):
    if not WEBHOOK_URL:
        print("❌ URL do webhook não configurada!")
        return
    
    for mensagem in mensagens:
        response = requests.post(
            WEBHOOK_URL,
            data=json.dumps(mensagem),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 204:
            print(f"✅ Lembrete enviado: {mensagem['embeds'][0]['fields'][1]['value']}")
        else:
            print(f"❌ Erro ao enviar: {response.status_code}")

if __name__ == "__main__":
    print("🔍 Verificando entregas...")
    mensagens = check_entregas()
    
    if mensagens:
        print(f"📨 Enviando {len(mensagens)} lembretes...")
        enviar_webhook(mensagens)
    else:
        print("✅ Nenhuma entrega próxima encontrada.")
        
        # Mensagem de "tudo em dia"
        mensagem_tudo_ok = {
            "embeds": [{
                "title": "🎉 TUDO EM DIA!",
                "color": 0x00FF00,
                "description": "Não há entregas próximas nos próximos 14 dias.",
                "footer": {"text": "Bot de Entregas da Karen"}
            }]
        }
        enviar_webhook([mensagem_tudo_ok])
