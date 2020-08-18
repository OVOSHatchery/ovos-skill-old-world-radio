from mycroft.skills.common_play_skill import CommonPlaySkill, \
    CPSMatchLevel, CPSMatchType
import youtube_dl
from os.path import join, dirname


class OldWorldRadioSkill(CommonPlaySkill):
    def __init__(self):
        super().__init__()
        self.supported_media = [CPSMatchType.RADIO]

    def initialize(self):
        self.add_event('skill-old-world-radio.jarbasskills.home',
                       self.handle_homescreen)

    def get_intro_message(self):
        self.speak_dialog("intro")
        self.gui.show_image(join(dirname(__file__), "ui", "logo.jpg"))

    # homescreen
    def handle_homescreen(self, message):
        # TODO selection menu
        self.CPS_play("https://www.youtube.com/watch?v=tzBGEqkwCoY",
                      utterance="vlc")

    def CPS_match_query_phrase(self, phrase, media_type):
        match = CPSMatchLevel.GENERIC
        url = "https://www.youtube.com/watch?v=tzBGEqkwCoY"

        if self.voc_match(phrase, "old_world"):
            match = CPSMatchLevel.EXACT
        elif self.voc_match(phrase, "vintage"):
            url = "https://www.youtube.com/watch?v=tb0B3auGbtA"
            match = CPSMatchLevel.TITLE

        return (phrase, match, {"url": url})

    def CPS_start(self, phrase, data):
        ydl_opts = {
            'format': "91",
            "no_color": True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(data["url"],
                                      download=False
                                      # We just want to extract the info
                                      )

            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries'][0]
            else:
                # Just a video
                video = result

        self.CPS_play(video['url'], utterance="vlc")


def create_skill():
    return OldWorldRadioSkill()
