from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import yt_dlp
import logging
import os
import fnmatch
import shutil
from dotenv import load_dotenv

load_dotenv()  # This loads variables from .env into the environment

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_markdown_v2("I am a bot that uses [yt\-dlp](https://github.com/yt\-dlp/yt\-dlp) to download video links in audio format", reply_markup=ForceReply(selective=True))


async def usage_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /usage is issued."""
    await update.message.reply_text("Send a single or list of video links to be converted. Use playlist command to download a playlist")

def get_title(url):
	"""get the title from the video url"""
	with yt_dlp.YoutubeDL({}) as ydl: 
		info_dict = ydl.extract_info(url, download=False)
		video_title = info_dict.get('title', None)
		return video_title


def find_thumbnail(path):
    """find the thumbnail associated with the downloaded audio file"""
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', "*webp"]
    for file in os.listdir(f"./{path}"):
        if any(fnmatch.fnmatch(file, ext) for ext in image_extensions):
            return os.path.join(path, file)
    
def find_mp3(path):
    """find the mp3 file"""
    for file in os.listdir(f"./{path}"):
        if fnmatch.fnmatch(file, '*.mp3'):
            return os.path.join(path, file)

def download_audio(url, downloads_path) -> str:
    """Download audio from the given link."""
    ytdlp_audio_opts = {
      'writethumbnail': True,
      'outtmpl': f"./{downloads_path}/%(title)s.%(ext)s",
    	'format': 'bestaudio/best',
      'postprocessors': [
      	{
        	'key': 'FFmpegExtractAudio',
        	'preferredcodec': 'mp3'
				}
      ]
		}
    
    with yt_dlp.YoutubeDL(ytdlp_audio_opts) as ydl:
          ydl.download(url)
    return (find_mp3(downloads_path), find_thumbnail(downloads_path))

def delete_files(downloads_path):
  """remove the folder containing downloaded files"""
  os.remove(downloads_path)
     

async def send_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     """Send the downloaded audio."""
     urls = update.message.text.split(" ")    
     for url in urls:
        video_url = url.split("&")[0] # in case video link contains playlist
        downloads_path = get_title(video_url)
        audio_path, thumbnail_path = download_audio(video_url, downloads_path)
        with open(audio_path, "rb") as audio, open(thumbnail_path, "rb") as thumbnail:
          await update.message.reply_audio(audio, thumbnail=thumbnail, reply_to_message_id=update.message.id)
          shutil.rmtree(f"./{downloads_path}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("usage", usage_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_audio))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
