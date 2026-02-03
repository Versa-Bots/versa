import discord
from discord import user_command


class UserCommands(discord.Cog, name="user_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @user_command()
    async def avatar(self, ctx: discord.ApplicationContext, member: discord.Member) -> None:
        user = await self.bot.fetch_user(member.id)  # Color attribute is only available via fetch

        avatar_components = [
            discord.MediaGalleryItem(
                url=member.display_avatar.with_size(4096).url,
            )
        ]
        if member.avatar != member.display_avatar:
            avatar_components.append(
                discord.MediaGalleryItem(
                    url=member.avatar.with_size(4096).url,
                )
            )

        container = discord.ui.Container(
            discord.ui.MediaGallery(
                *avatar_components
            ),
            discord.ui.TextDisplay(content="-# Versa"),
            color=user.accent_color
        )

        await ctx.respond(view=discord.ui.DesignerView(container), ephemeral=True)

    @user_command()
    async def banner(self, ctx: discord.ApplicationContext, member: discord.Member) -> None:
        user = await self.bot.fetch_user(member.id)  # Banner and color are only available via fetch
        banner_components = []

        if member.display_banner is None and user.banner is None:
            await ctx.respond("Member has no banner(s) set!", ephemeral=True)
            return
        
        if member.display_banner is not None:
            banner_components.append(
                discord.ui.MediaGallery(
                    discord.MediaGalleryItem(
                        url=member.display_banner.with_size(4096).url,
                    )
                )
            )

        if user.banner is not None:
            banner_components.append(
                discord.ui.MediaGallery(
                    discord.MediaGalleryItem(
                        url=user.banner.with_size(4096).url,
                    )
                )
            )

        container = discord.ui.Container(
            *banner_components,
            discord.ui.TextDisplay(content="-# Versa"),
            color=user.accent_color
        )

        await ctx.respond(view=discord.ui.DesignerView(container), ephemeral=True)


def setup(bot):
    bot.add_cog(UserCommands(bot))
