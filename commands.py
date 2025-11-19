# Arquivo simples para adicionar entregas manualmente
import sqlite3

def add_entrega(disciplina, atividade, data_entrega, user_id="karen"):
    conn = sqlite3.connect('entregas.db')
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO entregas (disciplina, atividade, data_entrega, user_id) VALUES (?, ?, ?, ?)',
        (disciplina, atividade, data_entrega, user_id)
    )
    
    conn.commit()
    conn.close()
    print(f"✅ {atividade} adicionada!")

# EXEMPLOS - ADICIONE SUAS MATÉRIAS AQUI:
if __name__ == "__main__":
    add_entrega("Teorias da Criatividade", "Atividades e prova", "2025-12-01")
    add_entrega("Análise de Cenários para Projetos", "Atividades e prova", "2025-12-10")
    add_entrega("História da Arte", "Atividades e prova", "2025-12-10")
    add_entrega("Linguagem e História da Arte", "Atividades e prova", "2025-12-10")
    add_entrega("Gestão e Inovação", "Atividades e prova", "2025-12-10")
    
    print("🎯 Entregas adicionadas com sucesso!")
