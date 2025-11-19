import sqlite3

# Criar banco de dados
conn = sqlite3.connect('entregas.db')
cursor = conn.cursor()

# Criar tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entregas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina TEXT NOT NULL,
        atividade TEXT NOT NULL,
        data_entrega DATE NOT NULL,
        user_id TEXT NOT NULL
    )
''')

# Adicionar entregas de exemplo
entregas = [
    ('Teorias da Criatividade', 'Atividades e prova', '2025-12-01', 'karen'),
    ('Análise de Cenários para Projetos', 'Atividades e prova', '2025-12-10', 'karen'),
    ('História da Arte', 'Atividades e prova', '2025-12-10', 'karen'),
    ('Linguagem e História da Arte', 'Atividades e prova', '2025-12-10', 'karen'),
    ('Gestão e Inovação', 'Atividades e prova', '2025-12-10', 'karen')
]

cursor.executemany(
    'INSERT INTO entregas (disciplina, atividade, data_entrega, user_id) VALUES (?, ?, ?, ?)',
    entregas
)

conn.commit()
conn.close()

print("✅ Banco de dados 'entregas.db' criado com sucesso!")
print("📚 5 entregas adicionadas automaticamente!")
