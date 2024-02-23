# YT-DLP Audio Downloader Bot for Telegram

This Telegram Bot harnesses the power of [yt-dlp](https://github.com/yt-dlp/yt-dlp), an advanced download manager, to fetch and convert video links into audio format directly within your Telegram chats. Whether you're looking to save your favorite music tracks or podcast episodes from video platforms, this bot makes it incredibly easy and efficient, all with a simple command. You can access the bot at [@ytdlpus_bot](https://t.me/@ytdlplus_bot) on Telegram.

## Features

- **Download Audio**: Convert video links to high-quality audio.
- **Thumbnail Support**: Audio files are sent with their respective video thumbnails for easy identification.
- **Simple Commands**: Easy-to-use commands for a seamless user experience.

## Commands

`/start` - Displays a welcome message and brief instructions. \
`/usage` - Provides detailed instructions on how to use the bot.

## Getting Started

### Prerequisites

- Python 3.6+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- A Telegram Bot Token ([How to create a bot](https://core.telegram.org/bots#creating-a-new-bot))

### Installation

1. **Clone the repository**

```sh
git clone https://github.com/ismayilkarimli/YTDLPlus_bot.git
cd YTDLPlus_bot
```

2. **Install the dependencies**

```sh
pip install -r requirements.txt
```

3. **Setup the .env file**  
   Edit the .env file and add your Telegram Bot Token:

```sh
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

4. **Start the bot**

```sh
python ytdlplus_bot.py
```
