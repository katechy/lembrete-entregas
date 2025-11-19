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

# Exemplo de uso:
if __name__ == "__main__":
    add_entrega("Pipeline 3D", "Cena final", "2025-11-25")
