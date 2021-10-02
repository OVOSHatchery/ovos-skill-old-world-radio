from os.path import join, dirname

from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    MediaType, PlaybackType, \
    ocp_search


class OldWorldRadioSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super().__init__()
        self.supported_media = [MediaType.RADIO, MediaType.GENERIC]
        self.default_bg = join(dirname(__file__), "ui", "logo.png")
        self.default_image = join(dirname(__file__), "ui", "background.jpg")
        self.skill_logo = join(dirname(__file__), "ui", "old-world-radio.png")
        self.skill_icon = join(dirname(__file__), "ui", "old-world-radio.png")

    def get_intro_message(self):
        self.speak_dialog("intro")
        self.gui.show_image(join(dirname(__file__), "ui", "logo.jpg"))

    # better common play
    @ocp_search()
    def search(self, phrase, media_type):
        """Analyze phrase to see if it is a play-able phrase with this skill.

        Arguments:
            phrase (str): User phrase uttered after "Play", e.g. "some music"
            media_type (MediaType): requested CPSMatchType to media for

        Returns:
            search_results (list): list of dictionaries with result entries
            {
                "match_confidence": MatchConfidence.HIGH,
                "media_type":  CPSMatchType.MUSIC,
                "uri": "https://audioservice.or.gui.will.play.this",
                "playback": PlaybackType.VIDEO,
                "image": "http://optional.audioservice.jpg",
                "bg_image": "http://optional.audioservice.background.jpg"
            }
        """
        scores = {"old_world": 0,
                  "storyteller": 0}
        if self.voc_match(phrase, "old_world"):
            scores["old_world"] = 50
            scores["storyteller"] = 20
        if self.voc_match(phrase, "vintage"):
            scores["old_world"] += 40
            scores["storyteller"] += 10
        if self.voc_match(phrase, "storyteller"):
            scores["storyteller"] += 40

        if media_type == MediaType.RADIO:
            scores["storyteller"] += 10
            scores["old_world"] += 30
        elif not self.voc_match(phrase, "radio"):
            scores["old_world"] = 15
            scores["storyteller"] -= 15

        return [
            {
                "match_confidence": min(100, scores["storyteller"]),
                "media_type": MediaType.RADIO,
                "uri": "https://www.youtube.com/watch?v=SWxEH7OcNn8",
                "playback": PlaybackType.AUDIO,
                "image": join(dirname(__file__), "ui", "background3.jpg"),
                "bg_image": self.default_bg,
                "skill_icon": self.skill_icon,
                "skill_logo": self.skill_logo,
                "title": "Storyteller's Old World Tunes and Tales",
                "author": "Old World Radio",
                "album": "Storyteller's Old World Tunes and Tales - Live 24/7",
                'length': 0
            },
            {
                "match_confidence": min(100, scores["old_world"]),
                "media_type": MediaType.RADIO,
                "uri": "https://www.youtube.com/watch?v=Ya3WXzEBL1E",
                "playback": PlaybackType.AUDIO,
                "image": join(dirname(__file__), "ui", "background.jpg"),
                "bg_image": self.default_bg,
                "skill_icon": self.skill_icon,
                "skill_logo": self.skill_logo,
                "title": "Old World Radio",
                "author": "Old World Radio",
                "album": "Fallout Radio - Live 24/7",
                'length': 0

            }]


def create_skill():
    return OldWorldRadioSkill()
