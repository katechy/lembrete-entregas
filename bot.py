import discord
from discord.ext import commands, tasks
import sqlite3
from datetime import datetime, date
import os
from flask import Flask
import threading

# ========== SERVIDOR WEB PARA O RENDER ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot de Entregas da Karen está rodando!"

@app.route('/health')
def health():
    return "✅ Online!"

def run_web():
    app.run(host='0.0.0.0', port=8000)

# ========== CONFIGURAÇÃO DO BOT ==========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# ========== BANCO DE DADOS ==========
def get_db():
    conn = sqlite3.connect('entregas.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina TEXT NOT NULL,
            atividade TEXT NOT NULL,
            data_entrega DATE NOT NULL,
            user_id INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ========== COMANDOS DO BOT ==========
@bot.command()
async def add(ctx, disciplina, atividade, data_entrega):
    try:
        data_obj = datetime.strptime(data_entrega, '%Y-%m-%d').date()
        hoje = date.today()
        
        if data_obj < hoje:
            await ctx.send("❌ Data de entrega já passou! Use uma data futura.")
            return
            
        conn = get_db()
        conn.execute(
            'INSERT INTO entregas (disciplina, atividade, data_entrega, user_id) VALUES (?, ?, ?, ?)',
            (disciplina, atividade, data_entrega, ctx.author.id)
        )
        conn.commit()
        conn.close()
        
        await ctx.send(f"✅ **{atividade}** de **{disciplina}** adicionada para {data_entrega}!")
        
    except ValueError:
        await ctx.send("❌ Formato de data inválido! Use: YYYY-MM-DD")

@bot.command()
async def listar(ctx):
    conn = get_db()
    entregas = conn.execute(
        'SELECT * FROM entregas WHERE user_id = ? ORDER BY data_entrega',
        (ctx.author.id,)
    ).fetchall()
    conn.close()
    
    if not entregas:
        await ctx.send("📝 Nenhuma entrega cadastrada!")
        return
        
    mensagem = "📚 **SUAS ENTREGAS:**\n"
    for entrega in entregas:
        data_obj = datetime.strptime(entrega['data_entrega'], '%Y-%m-%d').date()
        hoje = date.today()
        dias_restantes = (data_obj - hoje).days
        
        mensagem += f"\n**{entrega['atividade']}** - {entrega['disciplina']}"
        mensagem += f"\n📅 {entrega['data_entrega']} | ⏳ {dias_restantes} dias restantes"
        mensagem += f"\n🆔 ID: {entrega['id']}\n"
    
    await ctx.send(mensagem)

@bot.command()
async def entregue(ctx, id_entrega: int):
    conn = get_db()
    entrega = conn.execute(
        'SELECT * FROM entregas WHERE id = ? AND user_id = ?',
        (id_entrega, ctx.author.id)
    ).fetchone()
    
    if entrega:
        conn.execute('DELETE FROM entregas WHERE id = ?', (id_entrega,))
        conn.commit()
        await ctx.send(f"🎉 **{entrega['atividade']}** marcada como ENTREGUE! Parabéns!")
    else:
        await ctx.send("❌ Entrega não encontrada ou não pertence a você!")
    
    conn.close()

# ========== LEMBRETE AUTOMÁTICO ==========
@tasks.loop(hours=24)
async def alerta_diario():
    await bot.wait_until_ready()
    
    conn = get_db()
    entregas = conn.execute(
        'SELECT * FROM entregas ORDER BY data_entrega'
    ).fetchall()
    conn.close()
    
    for entrega in entregas:
        data_obj = datetime.strptime(entrega['data_entrega'], '%Y-%m-%d').date()
        hoje = date.today()
        dias_restantes = (data_obj - hoje).days
        
        if dias_restantes >= 0:
            user = await bot.fetch_user(entrega['user_id'])
            if user:
                await user.send(
                    f"⏰ **LEMBRETE:** Faltam **{dias_restantes} dias** para:\n"
                    f"**{entrega['atividade']}** - {entrega['disciplina']}\n"
                    f"📅 Data: {entrega['data_entrega']}"
                )

# ========== EVENTOS ==========
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    init_db()
    alerta_diario.start()

# ========== INICIAR TUDO ==========
if __name__ == "__main__":
    # Inicia servidor web em thread separada
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    # Inicia o bot Discord
    bot.run(os.getenv('DISCORD_TOKEN'))
