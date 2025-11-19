import requests
import json
import sqlite3
from datetime import datetime, date
import os

# Configurações
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def check_entregas():
    # Conectar ao banco (usaremos um arquivo local)
    conn = sqlite3.connect('entregas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Criar tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina TEXT NOT NULL,
            atividade TEXT NOT NULL,
            data_entrega DATE NOT NULL,
            user_id TEXT NOT NULL
        )
    ''')
    
    # VERIFICAR se está vazio e adicionar entregas AUTOMATICAMENTE
    cursor.execute('SELECT COUNT(*) FROM entregas')
    if cursor.fetchone()[0] == 0:
        print("📝 Banco vazio - adicionando entregas automaticamente...")
        entregas_exemplo = [
            ('Teorias da Criatividade', 'Atividades e prova', '2025-12-01', 'karen'),
            ('Análise de Cenários para Projetos', 'Atividades e prova', '2025-12-10', 'karen'),
            ('História da Arte', 'Atividades e prova', '2025-12-10', 'karen'),
            ('Linguagem e História da Arte', 'Atividades e prova', '2025-12-10', 'karen'),
            ('Gestão e Inovação', 'Atividades e prova', '2025-12-10', 'karen')
        ]
        
        cursor.executemany(
            'INSERT INTO entregas (disciplina, atividade, data_entrega, user_id) VALUES (?, ?, ?, ?)',
            entregas_exemplo
        )
        conn.commit()
        print("✅ 5 entregas adicionadas automaticamente!")
    
    # Verificar entregas próximas (5 dias ou menos)
    hoje = date.today()
    cursor.execute(
        'SELECT * FROM entregas WHERE date(data_entrega) >= date(?) ORDER BY data_entrega',
        (hoje.isoformat(),)
    )
    
    entregas = cursor.fetchall()
    conn.close()
    
    mensagens = []
    
    for entrega in entregas:
        data_entrega = datetime.strptime(entrega['data_entrega'], '%Y-%m-%d').date()
        dias_restantes = (data_entrega - hoje).days
        
        if dias_restantes <= 5:  # Alertar para entregas em até 5 dias
            cor = 0xFF0000 if dias_restantes <= 1 else 0xFFA500 if dias_restantes <= 3 else 0xFFFF00
            
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
            # Verifica se é mensagem com fields ou mensagem simples
            if 'fields' in mensagem['embeds'][0]:
                print(f"✅ Lembrete enviado: {mensagem['embeds'][0]['fields'][1]['value']}")
            else:
                print(f"✅ Mensagem de status enviada")
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
        
        # Mensagem de "tudo em dia" - SEM FIELDS
        mensagem_tudo_ok = {
            "embeds": [{
                "title": "🎉 TUDO EM DIA!",
                "color": 0x00FF00,
                "description": "Não há entregas próximas nos próximos 5 dias.",
                "footer": {"text": "Bot de Entregas da Karen"}
            }]
        }
        enviar_webhook([mensagem_tudo_ok])
