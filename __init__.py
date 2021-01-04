from ovos_utils.skills.templates.media_player import MediaSkill, \
    CPSMatchType, CPSMatchLevel, CPSTrackStatus
from os.path import join, dirname
import pyvod


class OldWorldRadioSkill(MediaSkill):
    def __init__(self):
        super().__init__()
        self.settings["audio_only"] = True
        self.supported_media = [CPSMatchType.RADIO]
        self.default_bg = join(dirname(__file__), "ui", "logo.png")
        self.default_image = join(dirname(__file__), "ui", "background.jpg")
        self.message_namespace = 'skill-old-world-radio.jarbasskills.home'
        self.bootstrap_list = ["https://www.youtube.com/watch?v=tzBGEqkwCoY"]

    def get_intro_message(self):
        self.speak_dialog("intro")
        self.gui.show_image(join(dirname(__file__), "ui", "logo.jpg"))

    def CPS_match_query_phrase(self, phrase, media_type):
        match = CPSMatchLevel.GENERIC
        url = "https://www.youtube.com/watch?v=tzBGEqkwCoY"
        image = join(dirname(__file__), "ui", "background.jpg")

        if self.voc_match(phrase, "old_world"):
            match = CPSMatchLevel.EXACT
        elif self.voc_match(phrase, "vintage"):
            url = "https://www.youtube.com/watch?v=tb0B3auGbtA"
            match = CPSMatchLevel.TITLE
            image = join(dirname(__file__), "ui", "background2.jpg")

        if match is not None:
            return (phrase, match,
                    {"media_type": media_type, "query": phrase,
                     "image": image, "background": self.default_bg,
                     "stream": url})
        return None

    def CPS_start(self, phrase, data):
        bg = data.get("background") or self.default_bg
        image = data.get("image") or self.default_image
        url = pyvod.utils.get_video_stream(data["stream"])
        self.CPS_send_status(uri=url,
                             image=image,
                             background_image=bg,
                             playlist_position=0,
                             status=CPSTrackStatus.PLAYING_AUDIOSERVICE)
        self.audioservice.play(url, utterance=self.play_service_string)


def create_skill():
    return OldWorldRadioSkill()
