import os
import pychromecast

class VoiceText:

    def __init__(self, device):
        self.root = './static/data/voice'
        self.device = device

    def main(self, text, server_host):
        os.makedirs(self.root, exist_ok=True)
        path = os.path.join(self.root, text+'.mp3')
        if not os.path.exists(path):
            cmd = "curl 'https://api.voicetext.jp/v1/tts' \
                    -o '{file}' \
                    -u '11a7lw7bvjukcsxn:' \
                    -d 'text={text}' \
                    -d 'speaker=hikari'".format(file=path, text=text)
            req = os.system(cmd)
        mc = self.device.media_controller
        mc.play_media(f"http://{server_host}:5000{self.root.replace('.','')}/"+text+".mp3", "audio/mp3")
        mc.block_until_active()