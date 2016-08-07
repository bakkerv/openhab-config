import time
from threading import Timer

class AutoLightsOffLivingRoom(Rule):
    def __init__(self):
        self.logger = oh.getLogger("AutoLightsOffLivingRoom")
        self.timer = None
        
    def getEventTrigger(self):
        return [
            UpdatedEventTrigger("GF_Living_Motion")
            ]

    def execute(self, event):
        self.logger.info("Motion Living update")
        self.logger.info("Living motion {}", str(ItemRegistry.getItem("GF_Living_Motion").state))
        self.cancelTimer()
        if str(ItemRegistry.getItem("GF_Living_Motion").state) == "OPEN":
            self.logger.info("Open, doing nothing")
            return
        self.cancelTimer()
        if int(str(ItemRegistry.getItem("GF_Living_Lamp_Table").state)) > 0:
            self.logger.info("Set timer to switch off lights after one hour")
            self.timer = Timer(1800, self.switchOffLights)
            self.timer.start()

    def cancelTimer(self):
        if self.timer is not None:
            self.logger.info("Cancelled timer")
            self.timer.cancel()
            self.timer = None
        else:
            self.logger.info("No timer")
        

    def switchOffLights(self):
        self.logger.info("Switching off lights")
        oh.postUpdate("GF_All_lights", "0")
        self.cancelTimer()
        

def getRules():
    return RuleSet([
            AutoLightsOffLivingRoom(),
            ])

