#CONFIG



import discord
from discord.ext import commands
import requests
import re, os
from bs4 import BeautifulSoup
import aiohttp
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
# Global vars
token = os.getenv("bot_token")
bot_name = "ᴋᴇᴇᴘᴇʀ [,]"
cmd_prefix = ","
scammers_filename = "scammers.txt"
scammers_list = [line.strip().lower() for line in open(scammers_filename)]
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
client = commands.Bot(command_prefix=cmd_prefix, intents=intents)
client.remove_command('help')
import datetime
import time
import schedule

#DO NOT MESS WITH ^^^ REQUIRED





















def compare_stats(current_stats, last_stats):
  comparison = {}
  for key in current_stats:
      current_value = current_stats[key]
      last_value = last_stats[key]
      arrow = "⬆️" if current_value > last_value else "⬇️" if current_value < last_value else ""
      comparison[key] = arrow
  return comparison





def is_user_tracked_today(user):
    today = datetime.date.today()
    tracking_filename = f"tracking_data.txt"

    # Check if the tracking file exists for today
    return os.path.isfile(tracking_filename)





def get_last_tracked_data(user):
    today = datetime.date.today()
    tracking_filename = f"tracking_data.txt"

    try:
        # Read the last line from the tracking file for the specified user
        with open(tracking_filename, 'r') as file:
            lines = file.readlines()
            for line in reversed(lines):
                if line.lower().startswith(user.lower()):
                    # Found the user in the tracking file
                    last_data = line.strip().split()[1:]
                    return {key: value for key, value in zip(['LEVEL', 'KILLS', 'ASSISTS', 'DEATHS', 'KADR', 'KDR', 'COINS'], last_data)}
    except FileNotFoundError:
        # If the tracking file doesn't exist, return None
        return None





def append_to_tracking_file(user, stats):
  add_user_to_tracking_list(user)

  today = datetime.date.today()
  timestamp = datetime.datetime.now().strftime("%m%d%Y")
  tracking_filename = f"tracking_data.txt"
  
  #Write the user stats with timestamp to the tracking file
  with open(tracking_filename, 'a') as file:
    file.write(f"{timestamp} {user} {' '.join(stats.values())}\n")





def add_user_to_tracking_list(user):
  tracking_list_filename = "track_these_people.txt"

  # Check if the user is already in the tracking list
  if user.lower() not in [line.strip().lower() for line in open(tracking_list_filename)]:
      # Add the user to the tracking list
      with open(tracking_list_filename, 'a') as file:
          file.write(user.lower() + '\n')





def track_users_hourly():
  # Read the users to track from the file
  users_to_track_filename = "track_these_people.txt"
  with open(users_to_track_filename, 'r') as file:
      users_to_track = [line.strip() for line in file]

  # Check and append tracking data for each user
  today = datetime.date.today()
  timestamp = today.strftime("%m%d%Y")
  print(timestamp)
  tracking_filename = "tracking_data_shared.txt"

  for user in users_to_track:
      # Check if an entry already exists for the user on the same date
      if not is_entry_exists(user, timestamp):
          # Fetch the current data for the user from Bandit.RIP
          current_stats = get_user_stats_from_banditrip(user)

          # Append current data with timestamp to the tracking file
          append_to_tracking_file(user, current_stats)






# ... (existing code)

# Schedule hourly tracking


def create_embed(title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=f"```elixir\n{description}\n```", color=color)
    return embed
def ce(title, description, color=discord.Color.blue()):
  embed = discord.Embed(title=title, description=f"```tex\n{description}\n```", color=color)
  return embed

def get_user_stats_from_banditrip(user):
  url = f"https://bandit.rip/player/@{user}"

  # Send a GET request to the URL
  response = requests.get(url)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Parse the HTML content
      soup = BeautifulSoup(response.text, 'html.parser')

      # Extracting player stats
      player_stats = soup.find_all('div', class_='playerpage-profile-stats')

      # Extract relevant information
      level = player_stats[0].get_text(strip=True).replace("LEVEL: ", "")
      kills = player_stats[1].get_text(strip=True).replace("KILLS: ", "")
      assists = player_stats[2].get_text(strip=True).replace("ASSISTS: ", "")
      deaths = player_stats[3].get_text(strip=True).replace("DEATHS: ", "")
      kadr = player_stats[4].get_text(strip=True).replace("KADR: ", "")
      kdr = player_stats[5].get_text(strip=True).replace("KDR: ", "")
      coins = player_stats[6].get_text(strip=True).replace("COINS: ", "")

      # Return the extracted stats as a dictionary
      return {
          'level': level,
          'kills': kills,
          'assists': assists,
          'deaths': deaths,
          'kadr': kadr,
          'kdr': kdr,
          'coins': coins
      }
  else:
      # Return None if the request was not successful
      return None
def get_user_stats(user):
  return get_user_stats_from_banditrip(user)


def track_users_daily():
  # Read the users to track from the file
  users_to_track_filename = "track_these_people.txt"
  with open(users_to_track_filename, 'r') as file:
      users_to_track = [line.strip() for line in file]

  # Check and append tracking data for each user
  today = datetime.date.today()
  timestamp = today.strftime("%m%d%Y")
  for user in users_to_track:
      # Check if an entry already exists for the user on the same date
      if not is_entry_exists(user, timestamp):
          # Fetch the current data for the user from Bandit.RIP
          current_stats = get_user_stats_from_banditrip(user)

          # Append current data with timestamp to the tracking file
          append_to_tracking_file(user, current_stats)













def is_entry_exists(user, date):
  tracking_filename = f"tracking_data_shared.txt"

  try:
      # Read the tracking file for the specified user and date
      with open(tracking_filename, 'r') as file:
          for line in file:
              if line.lower().startswith(date) and line.lower().find(f' {user.lower()} ') != -1:
                  # Found an existing entry for the user on the specified date
                  return True
  except FileNotFoundError:
      # If the tracking file doesn't exist, return False
      return False





def track_all_users():
  today = datetime.date.today()
  timestamp = today.strftime("%m%d%Y")

  # Write today's date to days_tracked.txt if not already present
  write_today_to_days_tracked(today)

  # Read the users to track from the file
  users_to_track_filename = "track_these_people.txt"
  with open(users_to_track_filename, 'r') as file:
      users_to_track = [line.strip() for line in file]

  # Track each user
  tracking_filename = "tracking_data.txt"

  for user in users_to_track:
      # Remove duplicate entries with the same date and user
      remove_duplicate_entries(user, timestamp)

      # Fetch the current data for the user from Bandit.RIP
      current_stats = get_user_stats_from_banditrip(user)

      # Append current data with timestamp to the tracking file
      append_to_tracking_file(user, current_stats)


def remove_duplicate_entries(user, date):
  tracking_filename = "tracking_data.txt"
  lines_to_keep = []

  try:
      # Read the tracking file and keep only non-duplicate entries
      with open(tracking_filename, 'r') as file:
          for line in file:
              if not (line.lower().startswith(date) and line.lower().find(f' {user.lower()} ') != -1):
                  lines_to_keep.append(line)

      # Write back the non-duplicate entries to the tracking file
      with open(tracking_filename, 'w') as file:
          file.writelines(lines_to_keep)
  except FileNotFoundError:
      # If the tracking file doesn't exist, do nothing
      pass


def write_today_to_days_tracked(today):
  days_tracked_filename = "days_tracked.txt"

  try:
      # Read the content of days_tracked.txt
      with open(days_tracked_filename, 'r') as file:
          content = file.read().strip()

      # Check if today's date is not in the content
      if today.strftime("%m%d%Y") not in content:
          # Write today's date to days_tracked.txt
          with open(days_tracked_filename, 'a') as file:
              file.write(today.strftime("%m%d%Y") + '\n')
  except FileNotFoundError:
      # If days_tracked.txt doesn't exist, create it and write today's date
      with open(days_tracked_filename, 'w') as file:
          file.write(today.strftime("%m%d%Y") + '\n')





def main():
    @client.event
    async def on_ready():
        track_all_users()
        print("User tracking completed.")
        await client.change_presence(activity=discord.Game(name=f"{cmd_prefix}help"))
        print("Bot Online")
        channel = client.get_channel(1197400807725862994)  # Replace CHANNEL_ID with the actual channel ID
        embed = create_embed("Bot Restarted", f"{bot_name} has been restarted.")
        await channel.send(embed=embed)
    @client.command()
    async def ping(ctx):
        embed = create_embed("Pong!", f'Latency: {round(client.latency * 1000)}ms')
        await ctx.send(embed=embed)
    @client.command(name='scam')
    async def scam(ctx, user):
        # Fetch the user object from ID

        # Check if the user is in the list of scammers
        if user.lower() in scammers_list:
            embed = create_embed("Scammer Check", f"{user} is a scammer!")
        else:
            embed = create_embed("Scammer Check", f"{user} is probably not a scammer.")

        await ctx.send(embed=embed)
    @client.command(name='hi')
    async def hi(ctx):
        embed = create_embed("Greetings", "Hey!")
        await ctx.send(embed=embed)
    @client.command(name='profile')
    async def profile(ctx, player_name):
        print(player_name)
        url = f"https://bandit.rip/player/@{player_name}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting player stats
            try:
                player_stats = soup.find('div', class_='player-stats')
                player_username_element = soup.find('div', class_='playerpage-profile-stats-2')
                player_username = player_username_element.get_text(strip=True)


                # Use regular expression to add a space before any clan tag
                player_username = re.sub(r'(\[.*?\])', r' \1', player_username)

                # Find all elements under the specified div class
                stats_elements = soup.find_all('div', class_='playerpage-profile-stats')

                # Accumulate information in a variable
                profile_info = f"{player_username}\n"
                if player_name.lower() in scammers_list:
                  profile_info = f"{player_username}\n⚠️ Scammer ⚠️\n"
                # Append everything under the <div class="playerpage-profile-stats"> tags to the variable
                for stat_element in stats_elements:
                    profile_info += stat_element.get_text(strip=True) + "\n"

                # Send the accumulated information in an embed
                embed = create_embed("Player Profile", profile_info)
                await ctx.send(embed=embed)
            except AttributeError:
              embed = ce("Error", "Player not found.")
              await ctx.send(embed=embed)

        else:
            embed = create_embed("Error", "Packet sent, but no response received.")
            await ctx.send(embed=embed)
    @client.command(name='stats')
    async def stats(ctx, player_name):
      print(player_name)
      url = f"https://bandit.rip/player/@{player_name}"

      # Send a GET request to the URL
      response = requests.get(url)

      # Check if the request was successful (status code 200)
      if response.status_code == 200:
          # Parse the HTML content
          soup = BeautifulSoup(response.text, 'html.parser')

          # Extracting player stats
          try:
              player_stats = soup.find('div', class_='player-stats')
              player_username_element = soup.find('div', class_='playerpage-profile-stats-2')
              player_username = player_username_element.get_text(strip=True)


              # Use regular expression to add a space before any clan tag
              player_username = re.sub(r'(\[.*?\])', r' \1', player_username)

              # Find all elements under the specified div class
              stats_elements = soup.find_all('div', class_='playerpage-profile-stats')

              # Accumulate information in a variable
              profile_info = f"{player_username}\n"
              if player_name.lower() in scammers_list:
                profile_info = f"{player_username}\n⚠️ Scammer ⚠️\n"
              # Append everything under the <div class="playerpage-profile-stats"> tags to the variable
              for stat_element in stats_elements:
                  profile_info += stat_element.get_text(strip=True) + "\n"

              # Send the accumulated information in an embed
              embed = create_embed("Player Profile", profile_info)
              await ctx.send(embed=embed)
          except AttributeError:
            embed = ce("Error", "Player not found.")
            await ctx.send(embed=embed)

      else:
          embed = create_embed("Error", "Packet sent, but no response received.")
          await ctx.send(embed=embed)






    @client.command(name='clan')
    async def clan_profile(ctx, clan_name):
        print(clan_name)
        url = f"https://bandit.rip/clan/{clan_name}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting clan information
            total_members = soup.find('div', class_='clanpage-member-total').get_text(strip=True)

            # Find all elements under the specified div class
            clan_members = soup.find_all('a', class_='clanpage-member')

            # Check if there are members in the clan
            if clan_members:
                # Get the first member's name
                first_member = clan_members[0].get_text(strip=True)

                # Replace the last character with " 👑"
                first_member_modified = first_member[:-1] + " 👑"

                # Modify the string attribute directly
                clan_members[0].string = first_member_modified

            # Accumulate information in a variable
            clan_info = f"{total_members}\n"

            # Append information about each clan member
            for member in clan_members:
                # Replace "Lv." with " - Level "
                member_text = member.get_text(strip=True).replace("Lv.", " - Level ")
                clan_info += f"{member_text}\n"

            # Extracting clan description
            clan_description_elem = soup.find('div', class_='clanpage-text clanpage-text-public')
            clan_description = ''.join(clan_description_elem.stripped_strings)

            # Check if the description exceeds 2000 characters
            max_length = 1997
            if len(clan_description) > max_length:
                clan_info += f"\nDescription:\nThe clan description is too long to display."
            else:
                clan_info += f"\nDescription:\n{clan_description}\n"

            # Send the accumulated information in an embed
            embed = create_embed("Clan Profile", clan_info)
            await ctx.send(embed=embed)

        else:
            embed = create_embed("Error", "Clan does not exist.")
            await ctx.send(embed=embed)

    @client.command(name='help')
    async def help_command(ctx):
        help_message = (
            "Command List:\n\n"
            f"{cmd_prefix}ping: Check the bot's latency.\n"
            f"{cmd_prefix}scam <user>: Check if a user is a scammer.\n"
            f"{cmd_prefix}hi: Greet the bot.\n"
            f"{cmd_prefix}profile <user>: Get information about a player's profile.\n"
            f"{cmd_prefix}clan <clan>: Get information about a clan's profile.\n"
            f"{cmd_prefix}top <bandits/clans (optional)> <number (optional)>: View the global leaderboards."
            f"{cmd_prefix}track user : Begin tracking a user's progress."
        )

        embed = ce("Command List", help_message)
        await ctx.send(embed=embed)
    @client.command(name='stat')
    async def stat(ctx, player_name):
      print(player_name)
      url = f"https://bandit.rip/player/@{player_name}"

      # Send a GET request to the URL
      response = requests.get(url)

      # Check if the request was successful (status code 200)
      if response.status_code == 200:
          # Parse the HTML content
          soup = BeautifulSoup(response.text, 'html.parser')

          # Extracting player stats
          try:
              player_stats = soup.find('div', class_='player-stats')
              player_username_element = soup.find('div', class_='playerpage-profile-stats-2')
              player_username = player_username_element.get_text(strip=True)


              # Use regular expression to add a space before any clan tag
              player_username = re.sub(r'(\[.*?\])', r' \1', player_username)

              # Find all elements under the specified div class
              stats_elements = soup.find_all('div', class_='playerpage-profile-stats')

              # Accumulate information in a variable
              profile_info = f"{player_username}\n"
              if player_name.lower() in scammers_list:
                profile_info = f"{player_username}\n⚠️ Scammer ⚠️\n"
              # Append everything under the <div class="playerpage-profile-stats"> tags to the variable
              for stat_element in stats_elements:
                  profile_info += stat_element.get_text(strip=True) + "\n"

              # Send the accumulated information in an embed
              embed = create_embed("Player Profile", profile_info)
              await ctx.send(embed=embed)
          except AttributeError:
            embed = ce("Error", "Player not found.")
            await ctx.send(embed=embed)

      else:
          embed = create_embed("Error", "Packet sent, but no response received.")
          await ctx.send(embed=embed)
    @client.command(name='top')
    async def top_command(ctx, type='bandits', num=10):
        # Validate num to ensure it's within the range [1, 40]
        num = max(1, min(num, 40))

        # Validate type to ensure it's either 'bandits' or 'clans'
        valid_types = ['bandits', 'clans']
        type = type.lower()
        if type not in valid_types:
            embed = ce("Error", "Invalid type. Type must be 'bandits' or 'clans'.")
            await ctx.send(embed=embed)
            return

        url = "https://bandit.rip/leaderboards"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting top players or clans based on the specified type
            if type == 'bandits':
                top_elements = soup.find_all('div', class_='leaderboard-entry')
            else:
                # Start scraping from the "Strongest Clans" section
                strongest_clans_title = soup.find('div', class_='f2 leaderboard-title', text='Strongest Clans')
                strongest_clans_div = strongest_clans_title.find_next('div', class_='leaderboard-entries')
                top_elements = strongest_clans_div.find_all('div', class_='leaderboard-entry')

            # Extract the top information based on the specified num
            top_info = [
                {
                    'rank': element.find('span', class_='leaderboard-entry-position').get_text(strip=True),
                    'name': element.find('a', class_='leaderboard-entry-username').get_text(strip=True),
                    'level': element.find('div', class_='leaderboard-entry-biglevel').get_text(strip=True),
                    'clan': element.find('a', class_='leaderboard-entry-clan').get_text(strip=True)[1:-1]
                    if element.find('a', class_='leaderboard-entry-clan') else None
                }
                for element in top_elements[:num]
            ]

            # Create and send the embed
            embed_title = f"Top {num} {type.capitalize()}"
            embed = create_embed(embed_title, "\n".join([f"{info['rank']}. {info['name']}" +
                                              (f" [{info['clan']}]" if info['clan'] else "") +
                                              f" - Level {info['level']}" for info in top_info]), color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            embed = ce("Error", "Unable to fetch leaderboard data.")
            await ctx.send(embed=embed)
    @client.command(name='track')
    async def track(ctx, user, start=None, end=None):
        # ... (existing code)
  
        # Fetch the current data for the user from Bandit.RIP
        current_stats = get_user_stats_from_banditrip(user)
  
        # Check if start and end dates are provided
        if start and end:
            start_date = datetime.datetime.strptime(start, "%m%d%Y").date()
            end_date = datetime.datetime.strptime(end, "%m%d%Y").date()
  
            # Fetch stats for the specified date range
            stats_for_range = fetch_stats_for_date_range(user, start_date, end_date)
  
            # Compare the stats for the specified date range
            stats_comparison = compare_stats(current_stats, stats_for_range)
  
            # Output the comparison result for the specified date range
            result_message = f"Comparison result between {start} and {end} for {user}:\n"
            for key, value in stats_for_range.items():
                result_message += f"{key.upper()}: {value} => {current_stats[key]} {stats_comparison[key]}\n"
        else:
            # Read the last tracked data from the file
            last_data = get_last_tracked_data(user)
  
            # Check if the user has been tracked before
            if last_data:
                # Compare the stats
                stats_comparison = compare_stats(current_stats, last_data)
            else:
                # If it's the first tracking, assume all stats increased
                stats_comparison = {key: "⬆️" for key in current_stats}
  
            # Append current data with timestamp to the tracking file
            append_to_tracking_file(user, current_stats)
  
            # Output the second user data with arrows
            result_message = f"Tracking data for {user} ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):\n"
            for key, value in current_stats.items():
                result_message += f"{key.upper()}: {value} {stats_comparison[key]}\n"
  
        # Send the result message in an embed
        embed = create_embed("Tracking Result", result_message)
        await ctx.send(embed=embed)
    @client.event
    async def on_disconnect():
        # This event is triggered when the bot disconnects from Discord
        channel = client.get_channel(1197400807725862994)  # Replace CHANNEL_ID with the actual channel ID
        embed = create_embed("Bot Offline", f"{bot_name} is being turned off.")
        await channel.send(embed=embed)














































    client.run(token)





































from flask import Flask
import threading

app = Flask(__name__)


@app.route('/')
def home():
    return f'Server for {bot_name}'


def run():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    # Start the Flask app in a separate thread
    server_thread = threading.Thread(target=run)
    server_thread.start()
    import asyncio

    asyncio.run(main())

    @app.route('/uptime-robot')
    def uptime_robot():
        return 'Uptime Robot - Keep alive!'
    while True:
      print("Keepalive check.")
      time.sleep(60)
