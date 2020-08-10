from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.messagebus import Message
import youtube_dl
from os.path import join, dirname


class OldWorldRadioSkill(CommonPlaySkill):
    vintage = "https://www.youtube.com/watch?v=tb0B3auGbtA"
    old_world = "https://www.youtube.com/watch?v=tzBGEqkwCoY"
    logo = join(dirname(__file__), "ui", "logo.jpg")

    def initialize(self):
        self.add_event('skill-old-world-radio.jarbasskills.home',
                       self.handle_homescreen)

    def get_intro_message(self):
        self.speak_dialog("intro")
        self.gui.show_image(self.logo)

    # homescreen
    def handle_homescreen(self, message):
        self.CPS_start("play old world radio",
                       {"url": self.old_world})

    def CPS_match_query_phrase(self, phrase):
        match = None
        url = self.old_world

        if self.voc_match(phrase, "old_world"):
            if self.voc_match(phrase, "radio"):
                match = CPSMatchLevel.EXACT
            else:
                match = CPSMatchLevel.TITLE
        elif self.voc_match(phrase, "vintage"):
            url = self.vintage
            if self.voc_match(phrase, "radio"):
                match = CPSMatchLevel.EXACT
            else:
                match = CPSMatchLevel.TITLE
        elif self.voc_match(phrase, "radio"):
            match = CPSMatchLevel.GENERIC

        if match is not None:
            return (phrase, match, {"url": url})
        return None

    def CPS_start(self, phrase, data):
        url = self.get_stream(data["url"])
        self.audioservice.play(url, utterance="vlc")
        self.CPS_send_status()

    def CPS_send_status(self, artist='', track='', image='', genre="",
                        album=""):
        data = {'skill': self.name,
                'artist': artist or "old world radio",
                'track': track or "old world radio",
                'image': image or self.logo,
                'genre': genre or "vintage radio",
                "album": album or "old world radio",
                'status': None  # TODO Add status system
                }
        self.bus.emit(Message('play:status', data))

    def get_stream(self, url):

        ydl_opts = {
            "no_color": True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url,
                                      download=False
                                      # We just want to extract the info
                                      )

            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries'][0]
            else:
                # Just a video
                video = result

            return video['url']


def create_skill():
    return OldWorldRadioSkill()

