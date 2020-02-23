from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel
import yaml
import sys
import logging
import socks

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(config):
    client = TelegramClient(config["session_name"], 
                            config["api_id"], 
                            config["api_hash"],
                            proxy=None
                            #proxy=(socks.HTTP, '127.0.0.1', 1087)
                            )
    client.start()

    input_channels_entities = []
    output_channel_entity = None
    for d in client.iter_dialogs():
        if d.name in config["input_channel_names"]:
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
        if d.name == config["output_channel_name"]:
            output_channel_entity = InputChannel(d.entity.id, d.entity.access_hash)
            
    if output_channel_entity is None:
        logger.error(f"Could not find the channel \"{config['output_channel_name']}\" in the user's dialogs")
        sys.exit(1)
    logging.info(f"Listening on {len(input_channels_entities)} channels. Forwarding messages to {config['output_channel_name']}.")
    
    @client.on(events.NewMessage(chats=input_channels_entities, pattern=r'([\s\S]*)#福建([\s\S]*)'))
    async def handler(event):
        await client.forward_messages(output_channel_entity, event.message)

    client.run_until_disconnected()

if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print(f"Usage: {sys.argv[0]} CONFIG_PATH")
    #    sys.exit(1)
    with open('/home/mr_chen001tools/easonTest/config.yml', 'rb') as f:
    #with open('/Users/zzj/Downloads/forwardgram-master/config.yml', 'rb') as f:
        config = yaml.load(f)
    start(config)
