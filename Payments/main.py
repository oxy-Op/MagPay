import discord
import json
from discord.ext import commands


with open('config.json','r') as c:
    config = json.load(c)

bot = commands.Bot(command_prefix=config['prefix'],intents=discord.Intents.all())
owner = 'MムǤͶUM ♛ IAMOXY#0786'


def run():
    bot.run(config['token'])


@bot.event
async def on_connect():
    print('Logged as {}'.format(bot.user.name))

methods = ['googlepay','paytm','paypal','phonepe','mobiqwik']

@bot.command()
async def payment(ctx,method,id):
    if method and id is not None:
        if method in methods:
            with open(f'database/{ctx.author.id}.json','w') as db:
                data = {
                    ctx.author.id:{
                        'method':method,
                        'payid':id
                    }
                }
                json.dump(data,db,indent=2)
                embed = discord.Embed(description=':white_check_mark: Successfully added payment method',color=0x33ffee)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="No methods found",description=f'No methods found name {method} ',color=0xff4eff)
            embed.add_field(name='Current Methods',value=[m for m in methods])
            await ctx.send(embed=embed)

@payment.error
async def error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f':x: Please type method and id as an argument')


@bot.command()
async def getmethod(ctx,ids:discord.User):
    try:
        with open(f'database/{ids.id}.json','r') as x:
            db = json.load(x)
            data = db[f'{ids.id}']['method']
            payid = db[f'{ids.id}']['payid']
        user = await bot.fetch_user(ids.id)
        embed = discord.Embed(title='Payment Methods For {}'.format(user.name),color=0xff8eff)
        embed.add_field(name='Method',value=data)
        embed.add_field(name='Number',value=payid)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send('User has not registered payment method yet')
    except FileNotFoundError:
        embed = discord.Embed(description=":x: User hasn\'t registered payment method yet")
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)

@getmethod.error
async def eor(ctx,error):
    if isinstance(error,commands.UserNotFound):
        await ctx.send('User not found')
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send('Please Mention Member to found info with')

@bot.command()
async def invite(ctx):
    embed = discord.Embed(description='This bot is only created for {} , If you want these kind\'s of bot then contact bot owner '.format(ctx.guild.name),color=0x5ee499)
    embed.set_footer(text='To get bot owner and more info use {}info'.format(bot.command_prefix))
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title='Information about bot',color=0x55eeff)
    embed.add_field(name='Name',value=bot.user.name)
    embed.add_field(name='ID',value=bot.user.id)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name='Owner',value=owner)
    embed.add_field(name='Programmer',value=owner)
    embed.add_field(name='Developer',value=owner)
    embed.add_field(name='Programming Language',value='Python | Version: 3.8.10')
    embed.add_field(name='API Wrapper',value='discord {}'.format(discord.__version__))
    await ctx.send(embed=embed)

@bot.command()
async def method(ctx):
    embed = discord.Embed(title='Methods',description=[m for m in methods],color=0xf494dd)
    await ctx.send(embed=embed)


if __name__ == '__main__':
    run()