import datetime
import sqlite3

import discord
from discord import app_commands
from discord.ext import commands


@commands.guild_only()
class Info(commands.GroupCog, group_name="info"):
    def __init__(self, bot):
        self.bot = bot

    # ---------------------------comandos---------------------------#
    @app_commands.command(
        name="servidor", description="[útilidades] Veja as informações sobre o servidor atual"
    )
    async def serverinfo(self, interaction: discord.Interaction):
        server = interaction.guild
        embed = discord.Embed(title=f"INFORMAÇÕES DO SERVIDOR", color=0x7575FF)
        if server.icon.url is not None:
            embed.set_author(name=server.name, icon_url=server.icon.url)
        else:
            embed.set_author(name=server.name)
        criacao = int(server.created_at.timestamp())
        embed.add_field(
            name="<:grupo:1107282332647440424> SERVIDOR",
            value=f"**Nome:** {server.name}\n**ID:** {server.id}\n**Data de criação:** <t:{criacao}:f> (<t:{criacao}:R>)\n<:coroa:1107279166925189130> **Dono:** {server.owner} - {server.owner_id}",
            inline=False,
        )
        embed.add_field(
            name=f"<:chat:1107281985161928745> CANAIS {len(server.channels)}",
            value=f"{len(server.text_channels)} canais de texto\n{len(server.voice_channels)} canais de voz\n{len(server.forums)} canais de fóruns\n{len(server.stage_channels)} canais de palco",
        )
        embed.add_field(
            name="<:member:1107279287268151356> MEMBROS",
            value=f"**{len(server.members)} membros**",
            inline=False,
        )

        embed.add_field(
            name="<:level:1107279028433457343> IMPULSOS",
            value=f"**nivel:** {server.premium_tier}\n**Quantidade de impulsos:** {server.premium_subscription_count}",
            inline=False,
        )
        if server.max_presences is None:
            presenca = "Desativado"
        else:
            presenca = server.max_presences

        if server.default_notifications == discord.NotificationLevel.only_mentions:
            notifications = "somente menções"

        if server.default_notifications == discord.NotificationLevel.all_messages:
            notifications = "todas as mensagens "

        if server.default_notifications is None:
            notifications = "sem notificações"

        if server.mfa_level == discord.MFALevel.require_2fa:
            verifi = "ativado"

        if server.mfa_level == discord.MFALevel.disabled:
            verifi = "desativado"
        if server.verification_level == discord.VerificationLevel.none:
            verifi_level = "sem verificação"

        if server.verification_level == discord.VerificationLevel.low:
            verifi_level = "baixo"

        if server.verification_level == discord.VerificationLevel.medium:
            verifi_level = "médio"

        if server.verification_level == discord.VerificationLevel.high:
            verifi_level = "alto"

        if server.verification_level == discord.VerificationLevel.highest:
            verifi_level = "altíssimo"

        if server.explicit_content_filter == discord.ContentFilter.disabled:
            conteudo_explicito = "desativado"

        if server.explicit_content_filter == discord.ContentFilter.no_role:
            conteudo_explicito = "somente membros sem cargos"
        if server.explicit_content_filter == discord.ContentFilter.all_members:
            conteudo_explicito = "todos os membros"

        if server.nsfw_level == discord.NSFWLevel.default:
            nsfw_nivel = "nível padrão(canais permitidos)"

        if server.nsfw_level == discord.NSFWLevel.explicit:
            nsfw_nivel = "nível explícito(todo o servidor)"

        if server.nsfw_level == discord.NSFWLevel.safe:
            nsfw_nivel = "nível seguro(não permitido)"
        embed.add_field(
            name="<:mod:1107281737735745637> MODERAÇÃO",
            value=f"**V2E:** {verifi}\n**Nível de verificação:** {verifi_level}\n**NSFW level:** {nsfw_nivel}\n**Limite de menbros:** {server.max_members}\n**Limite de presença:** {presenca}\n**Idioma preferido:** {server.preferred_locale}\n**Filtro de conteúdo explícito:** {conteudo_explicito}\n**Notificações:** {notifications}",
            inline=False,
        )
        taxa_bits = server.bitrate_limit / 1000
        arquivo = server.filesize_limit / 1048576
        embed.add_field(
            name="<:features:1107283826360733786> RECURSOS",
            value=f"**emojis:** possui {len(server.emojis)} de um limite de {server.emoji_limit}\n**figurinhas:** possui {len(server.stickers)} de um limite de {server.sticker_limit}\n**cargos:** {len(server.roles)}\n**taxa de bits:** {taxa_bits:.0f}kbps\n**tamanhos dos arquivos:** {arquivo:.0f}MB",
        )
        await interaction.response.send_message(embed=embed, view=BotaoView(server))

    # -------------------------------------------------------------#
    @app_commands.command(
        name="usuário",
        description="[útilidades] Veja as informações sobre um membro ou de si próprio ",
    )
    async def userinfo(self, interaction: discord.Interaction, membro: discord.User = None):
        if membro is None:
            membro = interaction.user
        embed = discord.Embed(
            title="<:grupo:1107282332647440424> INFORMAÇÕES DO MEMBRO", color=0x7575FF
        )
        if membro.avatar:
            embed.set_author(name=membro.name, icon_url=membro.avatar.url)
        else:
            embed.set_author(name=membro.name)
        criacao = int(membro.created_at.timestamp())

        membro_desde = int(membro.joined_at.timestamp())
        embed.add_field(
            name="<:conta:1107765359467044925> CONTA",
            value=f"**Nome:** {membro.name}\n**ID:** {membro.id}\n**Menção:** {membro.mention}\n**Entrou para o discord em:** <t:{criacao}:f> (<t:{criacao}:R>)\n**Entrou para o servidor em:** <t:{membro_desde}:f> (<t:{membro_desde}:R>)",
            inline=False,
        )
        embed.add_field(name=f"MAIOR CARGO", value=f"{membro.top_role.mention}")
        emblemas = {
            "active_developer": "<:activedev:1107728660733100184>",
            "bot_http_interactions": "<:slash:1107760971075813467>",
            "bug_hunter": "<:bug_hunter:1107749795776446524>",
            "bug_hunter_level_2": "<:bug_hunter_2:1107749887837212790>",
            "bug_hunter_level_3": "<:bug_hunter_3:1107750321167552532>",
            "discord_certified_moderator": "<:moderador:1107750609987317790>",
            "early_supporter": "<:early_supp:1107758921655001178>",
            "early_verified_bot_developer": "<:bot_dev:1107751061294432386>",
            "hypesquad": "<:hypesquad:1107753551826001971>",
            "hypesquad_balance": "<:banlance:1107754614905897082>",
            "hypesquad_bravery": "<:bravery:1107728568793976902>",
            "hypesquad_brilliance": "<:brilance:1107754254061539338>",
            "partner": "<:partner:1107752151138173140>",
            "spammer": "",
            "staff": "",
            "system": "",
            "team_user": "",
            "value": "",
            "verified_bot": "",
            "verified_bot_developer": "",
        }
        emoji = []
        for flag in membro.public_flags.all():
            try:
                emoji.append(emblemas[flag.name])
            except:
                emoji.append(flag.name)
        emoji_string = " ".join(emoji)
        embed.add_field(
            name="<a:emoji_2:1103831035478802512> EMBLEMAS", value=emoji_string, inline=False
        )
        await interaction.response.send_message(embed=embed, view=BotaoUserView(membro, self.bot))


# -------------------------------------------------------------#
# -------------------------------------------------------------#


class BotaoUserView(discord.ui.View):
    def __init__(self, membro, bot):
        self.membro = membro
        self.bot = bot
        super().__init__(timeout=300)

    @discord.ui.button(
        label="icone",
        style=discord.ButtonStyle.grey,
        emoji="<:icone:1107285800552513546>",
        custom_id="button_avatar",
        row=0,
    )
    async def on_icone(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.membro.avatar is not None:
            embed = discord.Embed(title="Avatar do usuário", color=0x7575FF)
            embed.set_image(url=self.membro.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                "me desculpe, não consegui encontrar nenhum avatar", ephemeral=True
            )

    @discord.ui.button(
        label="banner do perfil",
        style=discord.ButtonStyle.grey,
        emoji="<:banner:1107290001034727554>",
        custom_id="button_banner",
        row=0,
    )
    async def on_banner(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = await self.bot.fetch_user(self.membro.id)
        banner = user.banner
        if banner is not None:
            embed = discord.Embed(title="banner do perfil do usuário", color=0x7575FF)
            embed.set_image(url=banner.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                "me desculpe, não consegui encontrar nenhum banner pra esse usuário", ephemeral=True
            )

    @discord.ui.button(
        label="cargos",
        style=discord.ButtonStyle.grey,
        emoji="<a:roles:1107286628688466020>",
        custom_id="Button_cargos",
        row=1,
    )
    async def on_cargos(self, interaction: discord.Interaction, Button: discord.ui.Button):
        mencao = []
        for role in self.membro.roles:
            mencao.append(role.mention)

        cargo_string = "\n".join(mencao)
        embed = discord.Embed(
            title="todos os cargos do usuário", description=cargo_string, color=0x7575FF
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=300)

    @discord.ui.button(
        label="permissões",
        style=discord.ButtonStyle.grey,
        emoji="<a:warn:1103459839075688589>",
        custom_id="button_featu",
        row=1,
    )
    async def on_perms(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.membro.guild_permissions.create_instant_invite:
            convite = "sim"
        else:
            convite = "não"

        if self.membro.guild_permissions.kick_members:
            kick = "sim"
        else:
            kick = "não"

        if self.membro.guild_permissions.ban_members:
            ban = "sim"
        else:
            ban = "não"
        if self.membro.guild_permissions.administrator:
            adm = "sim"
        else:
            adm = "não"
        if self.membro.guild_permissions.manage_channels:
            chats = "sim"
        else:
            chats = "não"

        if self.membro.guild_permissions.manage_guild:
            guild = "sim"
        else:
            guild = "não"

        if self.membro.guild_permissions.add_reactions:
            reacoes = "sim"
        else:
            reacoes = "não"

        if self.membro.guild_permissions.view_audit_log:
            log = "sim"
        else:
            log = "não"

        if self.membro.guild_permissions.priority_speaker:
            speak = "sim"
        else:
            speak = "não"

        if self.membro.guild_permissions.stream:
            stream = "sim"
        else:
            stream = "não"

        if self.membro.guild_permissions.read_messages:
            read = "sim"
        else:
            read = "não"

        if self.membro.guild_permissions.send_messages:
            send = "sim"
        else:
            send = "não"

        if self.membro.guild_permissions.send_tts_messages:
            tts = "sim"
        else:
            tts = "não"

        if self.membro.guild_permissions.manage_messages:
            msm = "sim"
        else:
            msm = "não"

        if self.membro.guild_permissions.embed_links:
            links = "sim"
        else:
            links = "não"

        if self.membro.guild_permissions.attach_files:
            files = "sim"
        else:
            files = "não"

        if self.membro.guild_permissions.read_message_history:
            read_his = "sim"
        else:
            read_his = "não"

        if self.membro.guild_permissions.mention_everyone:
            mention = "sim"
        else:
            mention = "não"

        if self.membro.guild_permissions.external_emojis:
            ex_emoji = "sim"
        else:
            ex_emoji = "não"

        if self.membro.guild_permissions.view_guild_insights:
            insights = "sim"
        else:
            insights = "não"

        if self.membro.guild_permissions.connect:
            connect = "sim"
        else:
            connect = "não"

        if self.membro.guild_permissions.speak:
            falar = "sim"
        else:
            falar = "não"

        if self.membro.guild_permissions.mute_members:
            mute = "sim"
        else:
            mute = "não"
        if self.membro.guild_permissions.deafen_members:
            deafen = "sim"
        else:
            deafen = "não"

        if self.membro.guild_permissions.move_members:
            move = "sim"
        else:
            move = "não"

        if self.membro.guild_permissions.use_voice_activation:
            uva = "sim"
        else:
            uva = "não"

        if self.membro.guild_permissions.change_nickname:
            mudar_apelido = "sim"
        else:
            mudar_apelido = "não"

        if self.membro.guild_permissions.manage_nicknames:
            gere_nic = "sim"
        else:
            gere_nic = "não"

        if self.membro.guild_permissions.manage_roles:
            gere_roles = "sim"
        else:
            gere_roles = "não"

        if self.membro.guild_permissions.manage_webhooks:
            webhook = "sim"
        else:
            webhook = "não"

        if self.membro.guild_permissions.manage_emojis:
            man_roles = "sim"
        else:
            man_roles = "não"

        if self.membro.guild_permissions.use_application_commands:
            app_com = "sim"
        else:
            app_com = "não"

        if self.membro.guild_permissions.request_to_speak:
            pedir_falar = "sim"
        else:
            pedir_falar = "não"

        if self.membro.guild_permissions.manage_events:
            man_events = "sim"
        else:
            man_events = "não"

        if self.membro.guild_permissions.manage_threads:
            man_threads = "sim"
        else:
            man_threads = "não"

        if self.membro.guild_permissions.create_public_threads:
            cre_plu_thre = "sim"
        else:
            cre_plu_thre = "não"

        if self.membro.guild_permissions.create_private_threads:
            cre_pri_thre = "sim"
        else:
            cre_pri_thre = "não"

        if self.membro.guild_permissions.external_stickers:
            ex_fig = "sim"
        else:
            ex_fig = "não"

        if self.membro.guild_permissions.send_messages_in_threads:
            send_msm_thre = "sim"
        else:
            send_msm_thre = "não"

        if self.membro.guild_permissions.use_embedded_activities:
            embed_atv = "sim"
        else:
            embed_atv = "não"

        if self.membro.guild_permissions.moderate_members:
            mod_member = "sim"
        else:
            mod_member = "não"
        #
        # ('moderate_members', True)
        embed = discord.Embed(
            title="PERMISSÕES DO MEMBRO",
            description=f"""
                    Criar convite: {convite}\nExpulsar membros: {kick}\nBanir membros: {ban}\nAdministrador: {adm}\nGerenciar canais: {chats}\nGerenciar servidor: {guild}\nAdcionar reações: {reacoes}\nVer registro de auditoria: {log}\nVoz prioritária: {speak}\nCompartilhamento de tela: {stream}\nLer mensagens: {read}\nEnviar mensagens: {send}\nEnviar mensagens de texto-para-voz: {tts}\nGerenciar mensagens: {msm}\nMostrar conteudo de links: {links}\nAnexar arquivos: {files}\nLer histórico de mensagens: {read_his}\nMencionar everyone: {mention}\nUsar emojis externos: {ex_emoji}\nVer o insights do servidor: {insights}\nSe conectar: {connect}\nFalar: {falar}\nMutar membros: {mute}\nEnsurdecer membros: {deafen}\nMover membros: {move}\nUsar ativação de voz: {uva}\nMudar apelido: {mudar_apelido}\nGerenciar apelidos: {gere_nic}\nGerenciar cargos: {gere_roles}\nGerenciar webhooks: {webhook}\nGerenciar emojis: {man_roles}\nUsar comandos de aplicativo: {app_com}\nPedir pra falar: {pedir_falar}\nGerenciar eventos: {man_events}\nGerenciar tópicos: {man_threads}\nCriar tópicos públicos: {cre_plu_thre}\nCriar tópicos privados: {cre_pri_thre}\nUsar figurinhas externas: {ex_fig}\nEnviar mensagens em tópicos: {send_msm_thre}\nUsar atividades: {embed_atv}\nModerar membros: {mod_member}""",
            color=0x7575FF,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=300)


# -------------------------------------------------------------#
class BotaoView(discord.ui.View):
    def __init__(self, server):
        self.server = server
        super().__init__(timeout=300)

    @discord.ui.button(
        label="icone",
        style=discord.ButtonStyle.grey,
        emoji="<:icone:1107285800552513546>",
        custom_id="button_icon",
        row=0,
    )
    async def on_icone(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.server.icon is not None:
            embed = discord.Embed(title="Icone do servidor", color=0x7575FF)
            embed.set_image(url=self.server.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                "me desculpe, não consegui encontrar nenhum icone", ephemeral=True
            )

    @discord.ui.button(
        label="banner",
        style=discord.ButtonStyle.grey,
        emoji="<:banner:1107290001034727554>",
        custom_id="button_banner",
        row=0,
    )
    async def on_banner(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.server.banner is not None:
            embed = discord.Embed(title="banner do servidor", color=0x7575FF)
            embed.set_image(url=self.server.banner.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                "me desculpe, não consegui encontrar nenhum banner", ephemeral=True
            )

    @discord.ui.button(
        label="Descobrir",
        style=discord.ButtonStyle.grey,
        emoji="<:spash:1107285997173100544>",
        custom_id="Button_splash",
        row=0,
    )
    async def on_splash(self, interaction: discord.Interaction, button: discord.ui.Button):
        embeds = []

        if self.server.description is not None:
            embed = discord.Embed(
                title="Descrição do servidor", color=0x7575FF, description=self.server.description
            )
            embeds.append(embed)
        else:
            embed = discord.Embed(
                title="Descrição do servidor",
                description="não consegui encontrar a descrição do servidor",
                color=0x7575FF,
            )
            embeds.append(embed)
        if self.server.splash is not None:
            embed1 = discord.Embed(title="imagem do convite do servidor", color=0x7575FF)
            embed1.set_image(url=self.server.splash.url)
            embeds.append(embed1)
        else:
            embed1 = discord.Embed(
                title="imagem do convite do servidor",
                description="não consegui encontrar a imagem do convite do servidor",
                color=0x7575FF,
            )
            embeds.append(embed1)
        if self.server.discovery_splash is not None:
            embed2 = discord.Embed(title="imagem do descobrir do servidor", color=0x7575FF)
            embed2.set_image(url=self.server.discovery_splash)
            embeds.append(embed2)
        else:
            embed2 = discord.Embed(
                title="imagem do descobrir do servidor",
                description="não consegui encontrar a imagem do descobrir do servidor",
                color=0x7575FF,
            )
            embeds.append(embed2)
        await interaction.response.send_message(embeds=embeds, ephemeral=True, delete_after=300)

    @discord.ui.button(
        label="cargos",
        style=discord.ButtonStyle.grey,
        emoji="<a:roles:1107286628688466020>",
        custom_id="button_cargos",
        row=1,
    )
    async def on_cargos(self, interaction: discord.Interaction, Button: discord.ui.Button):
        mencao = []
        for role in self.server.roles:
            mencao.append(role.mention)

        cargo_string = "\n".join(mencao)
        embed = discord.Embed(title="todos os cargos", description=cargo_string, color=0x7575FF)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=300)

    @discord.ui.button(
        label="Recursos extras (beta)",
        style=discord.ButtonStyle.grey,
        emoji="<:extras:1107286925129289798>",
        custom_id="button_featu",
        row=1,
    )
    async def on_extras(self, interaction: discord.Interaction, Button: discord.ui.Button):
        recursos = {
            "ANIMATED_BANNER": "Banner animado",
            "ANIMATED_ICON": "Icone animado",
            "APPLICATION_COMMAND_PERMISSIONS_V2": "Comando de aplicativo V2",
            "AUTO_MODERATION": "Moderação automática",
            "BANNER": "Banner",
            "COMMUNITY": "Comunidade ativada",
            "CREATOR_MONETIZABLE_PROVISIONAL": "Monetização do criador ativada",
            "CREATOR_STORE_PAGE": "Página da loja do criador",
            "DEVELOPER_SUPPORT_SERVER": "Servidor com suporte de desenvolvimento",
            "DISCOVERABLE": "Discobrir ativado",
            "FEATURABLE": "Recursos",
            "INVITES_DISABLED": "Convites desabilitados",
            "INVITE_SPLASH": "Banner de convite",
            "MEMBER_VERIFICATION_GATE_ENABLED": "Botão de verificar membro",
            "MORE_STICKERS": "Mais adesivos",
            "NEWS": "Novidades ou avisos ativo",
            "PARTNERED": "Servidor parceiro",
            "PREVIEW_ENABLED": "Servidor pode ser previsionado",
            "RAID_ALERTS_DISABLED": "Alerta de invasão desativada",
            "ROLE_ICONS": "Icones nos cargos",
            "ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE": "Descrição nos cargos disponível",
            "ROLE_SUBSCRIPTIONS_ENABLED": "Descrição nos cargos ativa",
            "TICKETED_EVENTS_ENABLED": "Eventos ativados",
            "VANITY_URL": "Url personalizado por padrão",
            "VERIFIED": "Servidor verificado",
            "VIP_REGIONS": "Servidor tem acesso a 384kbps nos canais de voz",
            "WELCOME_SCREEN_ENABLED": "Tela de boas vindas",
            "GUILD_ONBOARDING_HAS_PROMPTS": "Acolhimento com prompts",
            "GUILD_ONBOARDING_EVER_ENABLED": "Acolhimentodisponível más desativado",
            "SOUNDBOARD": "Soundboard ativado",
            "GUILD_ONBOARDING": "Acolhimento disponivel",
        }

        recurso = []
        for feature in self.server.features:
            try:
                recurso.append(recursos[feature])
            except:
                recurso.append(feature)
        recursos_string = "\n".join(recurso)
        embed = discord.Embed(title="Recursos extras", description=recursos_string, color=0x7575FF)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=300)


# -------------------------------------------------------------#


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
