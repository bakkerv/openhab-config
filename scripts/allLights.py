from org.openhab.core.library.types import PercentType

class AllLightsRule(Rule):
    def getEventTrigger(self):
        return [ StartupTrigger(), 
           ChangedEventTrigger("GF_Living_Lamp_TV", None, None),
           ChangedEventTrigger("GF_Living_Lamp_Bank", None, None),
           ChangedEventTrigger("GF_Living_Lamp_Table", None, None),
        ]

    def execute(self, event):
        print("Execute")
        items = filter(lambda x: isinstance(x.state, PercentType), ir.getItems("GF_Living_Lamp*"))
        print(items)
        allLivingOn = all(map(lambda x: int(str(x.state)) > 0, items))
        currentState = int(str(ir.getItem("GF_All_lights").state))
        #kitchenOn = int(str(ir.getItem("GF_Kitchen_Lamp").state)) > 0
        print("allLiving %s kitchen %s currentState %s" % (allLivingOn, currentState))
        if allLivingOn and currentState != 1:
             oh.postUpdate("GF_All_lights","1")
        elif not allLivingOn and currentState != 0:
             oh.postUpdate("GF_All_lights","0")
        else:
             oh.postUpdate("GF_All_lights","2")


def getRules():
   print("Test")
   return RuleSet( [ AllLightsRule() ] ) 
