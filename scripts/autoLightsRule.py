import time

class DarkRule(Rule):
    def __init__(self):
        self.logger = oh.getLogger("DarkRule")
        self.isDark = self.determineIsDark()
        self.logger.info("Initialized. isDark: {0}".format(self.isDark))
        self.sendUpdate(self.isDark)
        

    def determineIsDark(self):
        return not self.isWithinDaylightTime() or self.tooDarkAccordingToSensor()

    def tooDarkAccordingToSensor(self):
        luminance = ItemRegistry.getItem("GF_Living_Luminance")
        if luminance.state == None or str(luminance.state == "Unitialized"):
            return False
        return luminance.state.intValue() < 50
                                              

    def isWithinDaylightTime(self):
        dlStart = ItemRegistry.getItem("Daylight_Start_Time")
        dlEnd   = ItemRegistry.getItem("Daylight_End_Time")
        if dlStart.state == None or str(dlStart.state) == "Uninitialized" or dlEnd.state == None or str(dlEnd.state) == "Unitialized":
            self.logger.info("Not iniatialized, return False")
            return False
        startInMs = dlStart.state.calendar.getTimeInMillis()
        endInMs = dlEnd.state.calendar.getTimeInMillis()
        now = long(time.time())*1000
        #self.logger.info("{} {}", startInMs)
        #self.logger.info("startInMs:  {0} endInMs: {1} now: {2}".format(startInMs, endInMs, now))
        if now >= startInMs and now <= endInMs:
            return True
        else:
            return False
        

    def getEventTrigger(self):
        return [
            #ChangedEventTrigger("GF_Living_Motion", None, OpenClosedType.OPEN),
            #ChangedEventTrigger("GF_Living_Luminance"),
            ChangedEventTrigger("Daylight_Start_Event"),
            ChangedEventTrigger("Daylight_End_Event"),
            ChangedEventTrigger("GF_Living_Luminance"),
            ChangedEventTrigger("Sunrise_Event"),
            #ChangedEventTrigger("GF_Light_switch_allowed", None, OnOffType.ON),
            ChangedEventTrigger("IsDark"),
            #TimerTrigger("0/15 * * * * ?")
            ]

    def sendUpdate(self, value):
        oh.sendCommand("IsDark","ON" if value else "OFF")

    def execute(self, event):
        self.logger.info("event {}", event)
        newIsDark = self.determineIsDark()
        if event.item is not None and event.item.name == "IsDark":
            self.isDark = str(event.newState) == "ON"
        if self.isDark != newIsDark:
            self.logger.info("Sending isDark to {0}".format(newIsDark))
            self.isDark = newIsDark
            self.sendUpdate(newIsDark)

class AutoLightRule(Rule):
    def __init__(self):
        self.logger = oh.getLogger("AutoLightRule")
        self.prowl = oh.getAction("Prowl")

    def lightsAreOn(self):
        lightsAreOn = False
        for l in ["GF_Living_Lamp_TV","GF_Living_Lamp_Bank","GF_Kitchen_Lamp"]:
            #self.logger.info("Item {0} state {1}".format(l, ItemRegistry.getItem(l)))
            lightsAreOn |= ItemRegistry.getItem(l).state.intValue() > 0
        return lightsAreOn

    def getEventTrigger(self):
        return [
            ChangedEventTrigger("GF_Living_Motion")
            ChangedEventTrigger("GF_Light_switch_allowed", None, OnOffType.ON),
            ChangedEventTrigger("IsDark"),
            #TimerTrigger("0/20 * * * * ?")
            ]

    def hasItemState(self, item, state):
        return str(ItemRegistry.getItem(item).state) == state

    def itIsDark(self):
        return self.hasItemState("IsDark", "ON")

    def isSwitchingAllowed(self):
        return self.hasItemState("GF_Light_switch_allowed", "ON")

    def isSomeonePresent(self):
        return self.hasItemState("GF_Living_Motion","OPEN")

    def switchLights(self, lightsOn):
        self.logger.info("Lights switch to {0}".format(lightsOn))
        oh.postUpdate("GF_Living_Last_Autoswitch", DateTimeType().toString())
        oh.sendCommand("GF_All_lights", "1" if lightsOn else "0")

    def execute(self, event):
        #self.logger.info("Lights are on {0}".format(self.lightsAreOn()))
        #self.logger.info("Is it dark? {0}".format(self.itIsDark()))
        #self.logger.info("Is switching allowed? {0}".format(self.isSwitchingAllowed()))
        #self.logger.info("Is someone present? {0}".format(self.isSomeonePresent()))
        if not self.isSwitchingAllowed():
            return
        if self.itIsDark() and not self.lightsAreOn() and self.isSomeonePresent():
            self.prowl.pushNotification("Lights","Lights are switched on")
            self.switchLights(True)
        if self.lightsAreOn() and (not self.itIsDark() or not self.isSomeonePresent()):
            self.prowl.pushNotification("Lights","Lights are switched off")
            self.switchLights(False)


def getRules():
    return RuleSet([
            DarkRule(),
            AutoLightRule()
            ])
