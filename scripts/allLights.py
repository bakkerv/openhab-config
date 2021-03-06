from org.openhab.core.library.types import PercentType
from org.openhab.core.library.types import OnOffType

class AllLightsRule(Rule):
    def getEventTrigger(self):
        return [ StartupTrigger(), 
           ChangedEventTrigger("GF_Living_Lamp_TV", None, None),
           ChangedEventTrigger("GF_Living_Lamp_Bank", None, None),
           ChangedEventTrigger("GF_Living_Lamp_Table", None, None),
        ]

    def execute(self, event):
        try:
            return
            oh.logInfo("AllLights","Execute")
            dimmer_items = filter(lambda x: isinstance(x.state, PercentType), ir.getItems("GF_Living_Lamp*"))
            oh.logInfo("AllLights","Dimmer {}", [dimmer_items])
            allDimmerOn = all(map(lambda x: int(str(x.state)) > 0, dimmer_items))
            currentState = int(str(ir.getItem("GF_All_lights").state))
            #print("allLiving %s kitchen %s currentState %s" % (allLivingOn, currentState))
            return
            if allDimmerOn and currentState != 1:
                 oh.postUpdate("GF_All_lights","1")
            elif not allDimmerOn and currentState != 0:
                 oh.postUpdate("GF_All_lights","0")
            else:
                 oh.postUpdate("GF_All_lights","2")
        except Exception as e:
            oh.logError("AllLights", "Something went wrong!")
            oh.logError("AllLights", "Test {}", e)


def getRules():
   print("Test")
   return RuleSet( [ AllLightsRule() ] ) 
