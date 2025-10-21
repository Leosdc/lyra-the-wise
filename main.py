import discord
from discord.ext import commands
import os
from pathlib import Path

# Importa utils PRIMEIRO
from utils import (
    carregar_dados,
    salvar_dados,
    auto_save,
    chamar_groq,
    get_system_prompt
)

# Importa sistemas
from sistemas_rpg import SISTEMAS_DISPONIVEIS

# ==== Configuração do Bot ====
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ==== Estruturas em memória ====
fichas_personagens = {}
sistemas_rpg = {}
sessoes_ativas = {}
conversation_history = {}

DATA_DIR = Path("bot_data")
DATA_DIR.mkdir(exist_ok=True)

# ==== Evento on_ready ====
@bot.event
async def on_ready():
    print(f"🎲 {bot.user} está online!")
    print(f"Conectado a {len(bot.guilds)} servidor(es)")
    
        # Status do bot
    await bot.change_presence(
        activity=discord.Game(name="!rpghelp | 50+ sistemas de RPG")
    )
    
    # Carrega dados salvos
    carregar_dados(fichas_personagens, sistemas_rpg, sessoes_ativas)
    
    # Inicia auto-save
    bot.loop.create_task(auto_save(bot, fichas_personagens, sistemas_rpg, sessoes_ativas))
    print("💾 Auto-save ativado!")

# ==== Comandos básicos ====
@bot.command(name="ping")
async def ping(ctx):
    """Testa se o bot está respondendo."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latência: {latency}ms")

@bot.command(name="testegroq")
async def teste_groq(ctx):
    """Testa a conexão com a API Groq."""
    await ctx.send("🔍 Testando conexão com Groq...")
    
    try:
        mensagens = [
            {"role": "system", "content": "Você é um assistente prestativo."},
            {"role": "user", "content": "Diga apenas: 'Conexão OK!'"}
        ]
        
        resposta = await chamar_groq(mensagens, max_tokens=50)
        
        if "Erro" in resposta or "erro" in resposta:
            await ctx.send(f"❌ Erro na API Groq:\n```{resposta}```")
        else:
            await ctx.send(f"✅ Groq funcionando!\n**Resposta:** {resposta}")
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao testar Groq: {str(e)}")

# ==== REGISTRO DE MÓDULOS ====
print("📦 Carregando módulos...")

try:
    # 1. Comandos de sistemas
    import sistemas_comandos
    sistemas_comandos.register(bot)
    print("✅ sistemas_comandos carregado")
except Exception as e:
    print(f"❌ Erro ao carregar sistemas_comandos: {e}")

try:
    # 2. Core do RPG (dados, mestre, etc)
    import rpg_core
    rpg_core.register(bot)
    print("✅ rpg_core carregado")
except Exception as e:
    print(f"❌ Erro ao carregar rpg_core: {e}")

try:
    # 3. Sistema de fichas
    import fichas
    fichas.register(bot)
    print("✅ fichas carregado")
except Exception as e:
    print(f"❌ Erro ao carregar fichas: {e}")

try:
    # 4. Painel de ajuda
    import help_painel
    help_painel.register(bot)
    print("✅ help_painel carregado")
except Exception as e:
    print(f"❌ Erro ao carregar help_painel: {e}")

try:
    # 5. Documentação
    import documentacao
    documentacao.register(bot)
    print("✅ documentacao carregado")
except Exception as e:
    print(f"❌ Erro ao carregar documentacao: {e}")

try:
    # 6. Utilitários
    import utilidades
    utilidades.register(bot)
    print("✅ utilidades carregado")
except Exception as e:
    print(f"❌ Erro ao carregar utilidades: {e}")

try:
    # 7. Admin
    import admin
    admin.register(bot)
    print("✅ admin carregado")
except Exception as e:
    print(f"❌ Erro ao carregar admin: {e}")

try:
    # 8. Geração de Conteúdo (monstros, NPCs, itens, etc)
    import geracao_conteudo
    geracao_conteudo.register(bot)
    print("✅ geracao_conteudo carregado")
except Exception as e:
    print(f"❌ Erro ao carregar geracao_conteudo: {e}")
    import traceback
    traceback.print_exc()

try:
    # 9. Sistema de sessões (ÚLTIMO, pois depende de tudo)
    from sessoes_rpg import setup_sessoes
    
    # Cria wrapper de salvar_dados compatível com sessões
    def salvar_dados_wrapper():
        salvar_dados(fichas_personagens, sistemas_rpg, sessoes_ativas)
    
    setup_sessoes(
        bot,
        SISTEMAS_DISPONIVEIS,
        fichas_personagens,
        sistemas_rpg,
        sessoes_ativas,
        chamar_groq,
        get_system_prompt,
        salvar_dados_wrapper,
    )
    print("✅ Sistema de sessões carregado")
except Exception as e:
    print(f"❌ Erro ao carregar sistema de sessões: {e}")
    import traceback
    traceback.print_exc()

print("🎲 Todos os módulos carregados!")

# ==== Tratamento de erros ====
@bot.event
async def on_command_error(ctx, error):
    """Tratamento global de erros de comandos."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Comando não encontrado. Use `!rpghelp` para ver a lista de comandos.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Faltam argumentos. Use `!rpghelp` para ver como usar o comando.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"❌ Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"❌ Você não pode usar este comando aqui.")
    else:
        print(f"⚠️ Erro não tratado: {error}")
        await ctx.send(f"⚠️ Ocorreu um erro ao executar o comando. O erro foi registrado.")

# ==== Evento de mensagens (para debug) ====
@bot.event
async def on_message(message):
    """Processa mensagens e comandos."""
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Processa comandos
    await bot.process_commands(message)

# ==== Inicializa bot ====
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("❌ Erro: variável DISCORD_BOT_TOKEN não encontrada no .env")
        print("💡 Crie um arquivo .env com:")
        print("   DISCORD_BOT_TOKEN=seu_token_aqui")
        print("   GROQ_API_KEY=sua_chave_groq_aqui")
    else:
        try:
            print("🚀 Iniciando bot...")
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ Erro ao iniciar o bot: {e}")
            import traceback
            traceback.print_exc()