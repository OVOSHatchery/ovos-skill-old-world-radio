from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill
from ovos_workshop.frameworks.playback import CPSMatchType, CPSPlayback, \
    CPSMatchConfidence
from os.path import join, dirname


class OldWorldRadioSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super().__init__()
        self.supported_media = [CPSMatchType.RADIO, CPSMatchType.GENERIC]
        self.default_bg = join(dirname(__file__), "ui", "logo.png")
        self.default_image = join(dirname(__file__), "ui", "background.jpg")
        self.skill_logo = join(dirname(__file__), "ui", "old-world-radio.png")
        self.skill_icon = join(dirname(__file__), "ui", "old-world-radio.png")

    def get_intro_message(self):
        self.speak_dialog("intro")
        self.gui.show_image(join(dirname(__file__), "ui", "logo.jpg"))

    # better common play
    def CPS_search(self, phrase, media_type):
        """Analyze phrase to see if it is a play-able phrase with this skill.

        Arguments:
            phrase (str): User phrase uttered after "Play", e.g. "some music"
            media_type (CPSMatchType): requested CPSMatchType to search for

        Returns:
            search_results (list): list of dictionaries with result entries
            {
                "match_confidence": CPSMatchConfidence.HIGH,
                "media_type":  CPSMatchType.MUSIC,
                "uri": "https://audioservice.or.gui.will.play.this",
                "playback": CPSPlayback.GUI,
                "image": "http://optional.audioservice.jpg",
                "bg_image": "http://optional.audioservice.background.jpg"
            }
        """

        scores = {"old_world": 0,
                  "vintage": 0}
        if self.voc_match(phrase, "old_world"):
            scores["old_world"] = 50
            scores["vintage"] = 10
        if self.voc_match(phrase, "vintage"):
            scores["vintage"] += 50

        if media_type == CPSMatchType.RADIO:
            scores["vintage"] += 30
            scores["old_world"] += 30
        elif not self.voc_match(phrase, "radio"):
            return []
        else:
            scores["vintage"] += 10
            scores["old_world"] += 10

        return [
            {
                "match_confidence": min(100, scores["vintage"]),
                "media_type": CPSMatchType.RADIO,
                "uri": "https://www.youtube.com/watch?v=tb0B3auGbtA",
                "playback": CPSPlayback.AUDIO,
                "image": join(dirname(__file__), "ui", "background2.jpg"),
                "bg_image": self.default_bg,
                "skill_icon": self.skill_icon,
                "skill_logo": self.skill_logo,
                "title": "VINTAGE RADIO",
                "author": "Old World Radio",
                "album": "LIVE OLDIES 24/7!",
                'length': 0
            },
            {
                "match_confidence": min(100, scores["old_world"]),
                "media_type": CPSMatchType.RADIO,
                "uri": "https://www.youtube.com/watch?v=tzBGEqkwCoY",
                "playback": CPSPlayback.AUDIO,
                "image":  join(dirname(__file__), "ui", "background.jpg"),
                "bg_image": self.default_bg,
                "skill_icon": self.skill_icon,
                "skill_logo": self.skill_logo,
                "title": "Old World Radio",
                "author": "Old World Radio",
                "album": "Old World Radio",
                'length': 0

            }]


def create_skill():
    return OldWorldRadioSkill()
