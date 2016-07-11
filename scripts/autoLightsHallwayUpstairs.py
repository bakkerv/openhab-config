import time

class LightHallwayUpstairs(Rule):
    def __init__(self):
        self.logger = oh.getLogger("LightHallwayUpstairs")
        
    def getEventTrigger(self):
        return [
            ChangedEventTrigger("Sunrise_Event"),
            ]

    def execute(self, event):
        self.logger.info("Switching off lights hallway")
        oh.sendCommand("FF_Corridor_Lamp", "OFF")

def getRules():
    return RuleSet([
            LightHallwayUpstairs(),
            ])
