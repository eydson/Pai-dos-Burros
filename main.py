import os
import discord
from discord.ext import commands
import re
from collections import defaultdict

# TOKEN do Bot
TOKEN = os.getenv('TOKEN')

# Configure intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print('-------------------')

def simplificar_dados(expressao):
    try:
        dados = defaultdict(int)
        soma_constantes = 0

        # Remove espaços e encontra os termos
        termos = re.findall(r'[+-]?\s*\d*d?\d+', expressao.replace(" ", ""))

        for termo in termos:
            if 'd' in termo:
                match = re.fullmatch(r'([+-]?\d*)d(\d+)', termo)
                if not match:
                    continue

                qtd = match.group(1)
                faces = int(match.group(2))

                # Trata quantidades positivas ou negativas
                qtd = int(qtd) if qtd not in ('', '+', '-') else int(f"{qtd}1")
                dados[faces] += qtd
            else:
                soma_constantes += int(termo)

        partes = []

        # Agrupa e divide se exceder 100 dados por tipo
        for faces in sorted(dados):
            total_qtd = dados[faces]
            if total_qtd == 0:
                continue

            while total_qtd > 100:
                partes.append(f"100d{faces}")
                total_qtd -= 100
            if total_qtd > 0:
                partes.append(f"{total_qtd}d{faces}")

        if soma_constantes != 0:
            partes.append(str(soma_constantes))

        return ' + '.join(partes) if partes else '0'

    except Exception as e:
        print(f"Erro ao simplificar dados: {e}")
        return None

@bot.command(name='simplify')
async def simplify(ctx, *, expr: str):
    try:
        simplificado = simplificar_dados(expr)
        if simplificado:
            await ctx.send(f"Simplificado: `{simplificado}`")
        else:
            await ctx.send("Erro ao simplificar. Verifique a sintaxe da expressão.")
    except Exception as e:
        await ctx.send("Ocorreu um erro ao processar seu comando.")
        print(f"Erro no comando simplify: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltou fornecer argumentos necessários para o comando.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado.")
    else:
        await ctx.send("Ocorreu um erro ao executar o comando.")
        print(f"Erro não tratado: {error}")

# Get token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("Erro: Token do Discord não encontrado nas variáveis de ambiente!")
    exit(1)

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure:
    print("Erro: Token do Discord inválido!")
except Exception as e:
    print(f"Erro ao iniciar o bot: {e}")
