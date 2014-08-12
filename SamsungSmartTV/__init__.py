"""<rst>
Adds actions to control the Samsung Smart TVs over the newtork

|

**TV IP Address** - the IP address of your TV. You can see it under 
*Menu > Network > Network Status*

**Port** - the port used to send commands. Usualy the port is 55000

**Connection timeout** - use this to control the connection timeout 
in seconds. You can use this to check is the TV powered on or not

**Remote control name** - the name that will appear in your TV when 
allowing it

**TV model** - fill this with your exact TV model (like UE50ES6710)

When the first command is sent to the TV, you will see a prompt on 
the TV to allow the remote. You can remote the remote later from the 
TV menu.

Each remote is identified by your **MAC address** and the 
"**Remote control name**"

"""



import eg

eg.RegisterPlugin(
    name = "Samsung Smart TV Network Remote",
    author = "Georgi Krastev",
    version = "0.0.2",
    kind = "external",
    description = __doc__
)

import socket
import base64
import time, datetime
from types import ClassType
from uuid import getnode as get_mac

eg.RegisterPlugin()

tv_keys_standard = (
('fnKEY_1', 'KEY_1', 'Key1'), 
('fnKEY_2', 'KEY_2', 'Key2'), 
('fnKEY_3', 'KEY_3', 'Key3'), 
('fnKEY_4', 'KEY_4', 'Key4'), 
('fnKEY_5', 'KEY_5', 'Key5'), 
('fnKEY_6', 'KEY_6', 'Key6'), 
('fnKEY_7', 'KEY_7', 'Key7'), 
('fnKEY_8', 'KEY_8', 'Key8'), 
('fnKEY_9', 'KEY_9', 'Key9'), 
('fnKEY_0', 'KEY_0', 'Key0'), 
('fnKEY_CHUP', 'KEY_CHUP', 'ChannelUp'), 
('fnKEY_CHDOWN', 'KEY_CHDOWN', 'ChannelDown'), 
('fnKEY_VOLUP', 'KEY_VOLUP', 'VolUp'),
('fnKEY_VOLDOWN', 'KEY_VOLDOWN', 'VolDown'), 
('fnKEY_MENU', 'KEY_MENU', 'Menu'), 
('fnKEY_UP', 'KEY_UP', 'Up'), 
('fnKEY_DOWN', 'KEY_DOWN', 'Down'), 
('fnKEY_LEFT', 'KEY_LEFT', 'Left'), 
('fnKEY_RIGHT', 'KEY_RIGHT', 'Right'), 
('fnKEY_MUTE', 'KEY_MUTE', 'Mute')
)

tv_keys_extended = (
("fnKEY_PRECH","KEY_PRECH","Pre-Ch"),
("fnKEY_GREEN","KEY_GREEN","Green"),
("fnKEY_YELLOW","KEY_YELLOW","Yellow"),
("fnKEY_CYAN","KEY_CYAN","Cyan"),
("fnKEY_ADDDEL","KEY_ADDDEL","Add/Del"),
("fnKEY_SOURCE","KEY_SOURCE","Source"),
("fnKEY_INFO","KEY_INFO","Info"),
("fnKEY_PIP_ONOFF","KEY_PIP_ONOFF","PIP"),
("fnKEY_PIP_SWAP","KEY_PIP_SWAP","PIPSwap"),
("fnKEY_PLUS100","KEY_PLUS100","Plus100"),
("fnKEY_CAPTION","KEY_CAPTION","Ad/Subt."),
("fnKEY_PMODE","KEY_PMODE","PictureMode"),
("fnKEY_TTX_MIX","KEY_TTX_MIX","Teletext"),
("fnKEY_TV","KEY_TV","TV"),
("fnKEY_PICTURE_SIZE","KEY_PICTURE_SIZE","PictureFormat"),
("fnKEY_AD","KEY_AD","AD/Subt."),
("fnKEY_PIP_SIZE","KEY_PIP_SIZE","PIPSize"),
("fnKEY_PIP_CHUP","KEY_PIP_CHUP","PIPChannelUp"),
("fnKEY_PIP_CHDOWN","KEY_PIP_CHDOWN","PIPChannelDown"),
("fnKEY_ANTENA","KEY_ANTENA","AntenaTV"),
("fnKEY_AUTO_PROGRAM","KEY_AUTO_PROGRAM","AutoProgram"),
("fnKEY_ASPECT","KEY_ASPECT","PictureFormat"),
("fnKEY_TOPMENU","KEY_TOPMENU","Support"),
("fnKEY_DTV","KEY_DTV","DigitalTV"),
("fnKEY_FAVCH","KEY_FAVCH","Favorites"),
("fnKEY_REWIND","KEY_REWIND","Rewind"),
("fnKEY_STOP","KEY_STOP","Stop"),
("fnKEY_PLAY","KEY_PLAY","Play"),
("fnKEY_FF","KEY_FF","FastForward"),
("fnKEY_REC","KEY_REC","Record"),
("fnKEY_PAUSE","KEY_PAUSE","Pause"),
("fnKEY_TOOLS","KEY_TOOLS","Tools"),
("fnKEY_LINK","KEY_LINK","Link"),
("fnKEY_SLEEP","KEY_SLEEP","SleepTimer"),
("fnKEY_TURBO","KEY_TURBO","SocialTV"),
("fnKEY_CH_LIST","KEY_CH_LIST","ChannelList"),
("fnKEY_RED","KEY_RED","Red"),
("fnKEY_HOME","KEY_HOME","Home"),
("fnKEY_ESAVING","KEY_ESAVING","EnergySaving"),
("fnKEY_CONTENTS","KEY_CONTENTS","SmartTV"),
("fnKEY_VCR_MODE","KEY_VCR_MODE","VCRmode"),
("fnKEY_CATV_MODE","KEY_CATV_MODE","CATVmode"),
("fnKEY_DSS_MODE","KEY_DSS_MODE","DSSmode"),
("fnKEY_TV_MODE","KEY_TV_MODE","TVmode"),
("fnKEY_DVD_MODE","KEY_DVD_MODE","DVDmode"),
("fnKEY_STB_MODE","KEY_STB_MODE","STBmode"),
("fnKEY_ZOOM_MOVE","KEY_ZOOM_MOVE","KEY_ZOOM_MOVE"),
("fnKEY_CLOCK_DISPLAY","KEY_CLOCK_DISPLAY","ClockDisplay"),
("fnKEY_AV1","KEY_AV1","Ext."),
("fnKEY_COMPONENT1","KEY_COMPONENT1","Component"),
("fnKEY_SETUP_CLOCK_TIMER","KEY_SETUP_CLOCK_TIMER","SetupClock"),
("fnKEY_RETURN","KEY_RETURN","Return"),
("fnKEY_HDMI","KEY_HDMI","HDMI"),
("fnKEY_POWEROFF","KEY_POWEROFF","PowerOFF"),
("fnKEY_PANNEL_CHDOWN","KEY_PANNEL_CHDOWN","3D"),
("fnKEY_AUTO_ARC_PIP_SMALL","KEY_AUTO_ARC_PIP_SMALL","PictureModeDynamic"),
("fnKEY_AUTO_ARC_PIP_WIDE","KEY_AUTO_ARC_PIP_WIDE","HDMI2"),
("fnKEY_AUTO_ARC_PIP_RIGHT_BOTTOM","KEY_AUTO_ARC_PIP_RIGHT_BOTTOM","HDMI3"),
("fnKEY_AUTO_ARC_PIP_SOURCE_CHANGE","KEY_AUTO_ARC_PIP_SOURCE_CHANGE","BluetoohPair"),
("fnKEY_EXT9","KEY_EXT9","PictureModeMovie"),
("fnKEY_EXT10","KEY_EXT10","PictureModeStandard"),
("fnKEY_EXT14","KEY_EXT14","PictureSize_3:4"),
("fnKEY_EXT15","KEY_EXT15","PictureSize_16:9"),
("fnKEY_EXT20","KEY_EXT20","HDMI1"),
("fnKEY_EXT23","KEY_EXT23","AV"),
("fnKEY_AUTO_ARC_C_FORCE_AGING","KEY_AUTO_ARC_C_FORCE_AGING","Fam. Story"),
("fnKEY_AUTO_ARC_CAPTION_ENG","KEY_AUTO_ARC_CAPTION_ENG","History"),
("fnKEY_AUTO_ARC_USBJACK_INSPECT","KEY_AUTO_ARC_USBJACK_INSPECT","Camera"),
("fnKEY_DTV_SIGNAL","KEY_DTV_SIGNAL","Search"),
("fnKEY_AV2","KEY_AV2","AllSharePlay"),
("fnKEY_CONVERGENCE","KEY_CONVERGENCE","InternetBrowser")
)

tv_keys_other = (
("fnKEY_MAGIC_CHANNEL","KEY_MAGIC_CHANNEL","KEY_MAGIC_CHANNEL"),
("fnKEY_PIP_SCAN","KEY_PIP_SCAN","KEY_PIP_SCAN"),
("fnKEY_DEVICE_CONNECT","KEY_DEVICE_CONNECT","KEY_DEVICE_CONNECT"),
("fnKEY_HELP","KEY_HELP","KEY_HELP"),
("fnKEY_11","KEY_11","KEY_11"),
("fnKEY_12","KEY_12","KEY_12"),
("fnKEY_FACTORY","KEY_FACTORY","KEY_FACTORY"),
("fnKEY_3SPEED","KEY_3SPEED","KEY_3SPEED"),
("fnKEY_RSURF","KEY_RSURF","KEY_RSURF"),
("fnKEY_GAME","KEY_GAME","KEY_GAME"),
("fnKEY_QUICK_REPLAY","KEY_QUICK_REPLAY","KEY_QUICK_REPLAY"),
("fnKEY_STILL_PICTURE","KEY_STILL_PICTURE","KEY_STILL_PICTURE"),
("fnKEY_INSTANT_REPLAY","KEY_INSTANT_REPLAY","KEY_INSTANT_REPLAY"),
("fnKEY_FF_","KEY_FF_","KEY_FF_"),
("fnKEY_GUIDE","KEY_GUIDE","KEY_GUIDE"),
("fnKEY_REWIND_","KEY_REWIND_","KEY_REWIND_"),
("fnKEY_ANGLE","KEY_ANGLE","KEY_ANGLE"),
("fnKEY_RESERVED1","KEY_RESERVED1","KEY_RESERVED1"),
("fnKEY_ZOOM1","KEY_ZOOM1","KEY_ZOOM1"),
("fnKEY_PROGRAM","KEY_PROGRAM","KEY_PROGRAM"),
("fnKEY_BOOKMARK","KEY_BOOKMARK","KEY_BOOKMARK"),
("fnKEY_DISC_MENU","KEY_DISC_MENU","KEY_DISC_MENU"),
("fnKEY_PRINT","KEY_PRINT","KEY_PRINT"),
("fnKEY_SUB_TITLE","KEY_SUB_TITLE","KEY_SUB_TITLE"),
("fnKEY_CLEAR","KEY_CLEAR","KEY_CLEAR"),
("fnKEY_VCHIP","KEY_VCHIP","KEY_VCHIP"),
("fnKEY_REPEAT","KEY_REPEAT","KEY_REPEAT"),
("fnKEY_DOOR","KEY_DOOR","KEY_DOOR"),
("fnKEY_OPEN","KEY_OPEN","KEY_OPEN"),
("fnKEY_WHEEL_LEFT","KEY_WHEEL_LEFT","KEY_WHEEL_LEFT"),
("fnKEY_POWER","KEY_POWER","KEY_POWER"),
("fnKEY_DMA","KEY_DMA","KEY_DMA"),
("fnKEY_FM_RADIO","KEY_FM_RADIO","KEY_FM_RADIO"),
("fnKEY_DVR_MENU","KEY_DVR_MENU","KEY_DVR_MENU"),
("fnKEY_MTS","KEY_MTS","KEY_MTS"),
("fnKEY_PCMODE","KEY_PCMODE","KEY_PCMODE"),
("fnKEY_TTX_SUBFACE","KEY_TTX_SUBFACE","KEY_TTX_SUBFACE"),
("fnKEY_DNIe","KEY_DNIe","KEY_DNIe"),
("fnKEY_SRS","KEY_SRS","KEY_SRS"),
("fnKEY_CONVERT_AUDIO_MAINSUB","KEY_CONVERT_AUDIO_MAINSUB","KEY_CONVERT_AUDIO_MAINSUB"),
("fnKEY_MDC","KEY_MDC","KEY_MDC"),
("fnKEY_SEFFECT","KEY_SEFFECT","KEY_SEFFECT"),
("fnKEY_DVR","KEY_DVR","KEY_DVR"),
("fnKEY_LIVE","KEY_LIVE","KEY_LIVE"),
("fnKEY_PERPECT_FOCUS","KEY_PERPECT_FOCUS","KEY_PERPECT_FOCUS"),
("fnKEY_WHEEL_RIGHT","KEY_WHEEL_RIGHT","KEY_WHEEL_RIGHT"),
("fnKEY_SVIDEO1","KEY_SVIDEO1","KEY_SVIDEO1"),
("fnKEY_CALLER_ID","KEY_CALLER_ID","KEY_CALLER_ID"),
("fnKEY_SCALE","KEY_SCALE","KEY_SCALE"),
("fnKEY_COMPONENT2","KEY_COMPONENT2","KEY_COMPONENT2"),
("fnKEY_MAGIC_BRIGHT","KEY_MAGIC_BRIGHT","KEY_MAGIC_BRIGHT"),
("fnKEY_DVI","KEY_DVI","KEY_DVI"),
("fnKEY_W_LINK","KEY_W_LINK","KEY_W_LINK"),
("fnKEY_DTV_LINK","KEY_DTV_LINK","KEY_DTV_LINK"),
("fnKEY_APP_LIST","KEY_APP_LIST","KEY_APP_LIST"),
("fnKEY_BACK_MHP","KEY_BACK_MHP","KEY_BACK_MHP"),
("fnKEY_ALT_MHP","KEY_ALT_MHP","KEY_ALT_MHP"),
("fnKEY_DNSe","KEY_DNSe","KEY_DNSe"),
("fnKEY_RSS","KEY_RSS","KEY_RSS"),
("fnKEY_ENTERTAINMENT","KEY_ENTERTAINMENT","KEY_ENTERTAINMENT"),
("fnKEY_ID_INPUT","KEY_ID_INPUT","KEY_ID_INPUT"),
("fnKEY_ID_SETUP","KEY_ID_SETUP","KEY_ID_SETUP"),
("fnKEY_ANYNET","KEY_ANYNET","KEY_ANYNET"),
("fnKEY_POWERON","KEY_POWERON","KEY_POWERON"),
("fnKEY_ANYVIEW","KEY_ANYVIEW","KEY_ANYVIEW"),
("fnKEY_MS","KEY_MS","KEY_MS"),
("fnKEY_MORE","KEY_MORE","KEY_MORE"),
("fnKEY_PANNEL_POWER","KEY_PANNEL_POWER","KEY_PANNEL_POWER"),
("fnKEY_PANNEL_CHUP","KEY_PANNEL_CHUP","KEY_PANNEL_CHUP"),
("fnKEY_PANNEL_VOLUP","KEY_PANNEL_VOLUP","KEY_PANNEL_VOLUP"),
("fnKEY_PANNEL_VOLDOW","KEY_PANNEL_VOLDOW","KEY_PANNEL_VOLDOW"),
("fnKEY_PANNEL_ENTER","KEY_PANNEL_ENTER","KEY_PANNEL_ENTER"),
("fnKEY_PANNEL_MENU","KEY_PANNEL_MENU","KEY_PANNEL_MENU"),
("fnKEY_PANNEL_SOURCE","KEY_PANNEL_SOURCE","KEY_PANNEL_SOURCE"),
("fnKEY_AV3","KEY_AV3","KEY_AV3"),
("fnKEY_SVIDEO2","KEY_SVIDEO2","KEY_SVIDEO2"),
("fnKEY_SVIDEO3","KEY_SVIDEO3","KEY_SVIDEO3"),
("fnKEY_ZOOM2","KEY_ZOOM2","KEY_ZOOM2"),
("fnKEY_PANORAMA","KEY_PANORAMA","KEY_PANORAMA"),
("fnKEY_4_3","KEY_4_3","KEY_4_3"),
("fnKEY_16_9","KEY_16_9","KEY_16_9"),
("fnKEY_DYNAMIC","KEY_DYNAMIC","KEY_DYNAMIC"),
("fnKEY_STANDARD","KEY_STANDARD","KEY_STANDARD"),
("fnKEY_MOVIE1","KEY_MOVIE1","KEY_MOVIE1"),
("fnKEY_CUSTOM","KEY_CUSTOM","KEY_CUSTOM"),
("fnKEY_AUTO_ARC_RESET","KEY_AUTO_ARC_RESET","KEY_AUTO_ARC_RESET"),
("fnKEY_AUTO_ARC_LNA_ON","KEY_AUTO_ARC_LNA_ON","KEY_AUTO_ARC_LNA_ON"),
("fnKEY_AUTO_ARC_LNA_OFF","KEY_AUTO_ARC_LNA_OFF","KEY_AUTO_ARC_LNA_OFF"),
("fnKEY_AUTO_ARC_ANYNET_MODE_OK","KEY_AUTO_ARC_ANYNET_MODE_OK","KEY_AUTO_ARC_ANYNET_MODE_OK"),
("fnKEY_AUTO_ARC_ANYNET_AUTO_START","KEY_AUTO_ARC_ANYNET_AUTO_START","KEY_AUTO_ARC_ANYNET_AUTO_START"),
("fnKEY_AUTO_FORMAT","KEY_AUTO_FORMAT","KEY_AUTO_FORMAT"),
("fnKEY_DNET","KEY_DNET","KEY_DNET"),
("fnKEY_HDMI1","KEY_HDMI1","KEY_HDMI1"),
("fnKEY_AUTO_ARC_CAPTION_ON","KEY_AUTO_ARC_CAPTION_ON","KEY_AUTO_ARC_CAPTION_ON"),
("fnKEY_AUTO_ARC_CAPTION_OFF","KEY_AUTO_ARC_CAPTION_OFF","KEY_AUTO_ARC_CAPTION_OFF"),
("fnKEY_AUTO_ARC_PIP_DOUBLE","KEY_AUTO_ARC_PIP_DOUBLE","KEY_AUTO_ARC_PIP_DOUBLE"),
("fnKEY_AUTO_ARC_PIP_LARGE","KEY_AUTO_ARC_PIP_LARGE","KEY_AUTO_ARC_PIP_LARGE"),
("fnKEY_AUTO_ARC_PIP_LEFT_TOP","KEY_AUTO_ARC_PIP_LEFT_TOP","KEY_AUTO_ARC_PIP_LEFT_TOP"),
("fnKEY_AUTO_ARC_PIP_RIGHT_TOP","KEY_AUTO_ARC_PIP_RIGHT_TOP","KEY_AUTO_ARC_PIP_RIGHT_TOP"),
("fnKEY_AUTO_ARC_PIP_LEFT_BOTTOM","KEY_AUTO_ARC_PIP_LEFT_BOTTOM","KEY_AUTO_ARC_PIP_LEFT_BOTTOM"),
("fnKEY_AUTO_ARC_PIP_CH_CHANGE","KEY_AUTO_ARC_PIP_CH_CHANGE","KEY_AUTO_ARC_PIP_CH_CHANGE"),
("fnKEY_AUTO_ARC_AUTOCOLOR_SUCCESS","KEY_AUTO_ARC_AUTOCOLOR_SUCCESS","KEY_AUTO_ARC_AUTOCOLOR_SUCCESS"),
("fnKEY_AUTO_ARC_AUTOCOLOR_FAIL","KEY_AUTO_ARC_AUTOCOLOR_FAIL","KEY_AUTO_ARC_AUTOCOLOR_FAIL"),
("fnKEY_AUTO_ARC_JACK_IDENT","KEY_AUTO_ARC_JACK_IDENT","KEY_AUTO_ARC_JACK_IDENT"),
("fnKEY_NINE_SEPERATE","KEY_NINE_SEPERATE","KEY_NINE_SEPERATE"),
("fnKEY_ZOOM_IN","KEY_ZOOM_IN","KEY_ZOOM_IN"),
("fnKEY_ZOOM_OUT","KEY_ZOOM_OUT","KEY_ZOOM_OUT"),
("fnKEY_MIC","KEY_MIC","KEY_MIC"),
("fnKEY_HDMI2","KEY_HDMI2","KEY_HDMI2"),
("fnKEY_HDMI3","KEY_HDMI3","KEY_HDMI3"),
("fnKEY_AUTO_ARC_CAPTION_KOR","KEY_AUTO_ARC_CAPTION_KOR","KEY_AUTO_ARC_CAPTION_KOR"),
("fnKEY_HDMI4","KEY_HDMI4","KEY_HDMI4"),
("fnKEY_AUTO_ARC_ANTENNA_AIR","KEY_AUTO_ARC_ANTENNA_AIR","KEY_AUTO_ARC_ANTENNA_AIR"),
("fnKEY_AUTO_ARC_ANTENNA_CABLE","KEY_AUTO_ARC_ANTENNA_CABLE","KEY_AUTO_ARC_ANTENNA_CABLE"),
("fnKEY_AUTO_ARC_ANTENNA_SATELLITE","KEY_AUTO_ARC_ANTENNA_SATELLITE","KEY_AUTO_ARC_ANTENNA_SATELLITE"),
("fnKEY_EXT1","KEY_EXT1","KEY_EXT1"),
("fnKEY_EXT2","KEY_EXT2","KEY_EXT2"),
("fnKEY_EXT3","KEY_EXT3","KEY_EXT3"),
("fnKEY_EXT4","KEY_EXT4","KEY_EXT4"),
("fnKEY_EXT5","KEY_EXT5","KEY_EXT5"),
("fnKEY_EXT6","KEY_EXT6","KEY_EXT6"),
("fnKEY_EXT7","KEY_EXT7","KEY_EXT7"),
("fnKEY_EXT8","KEY_EXT8","KEY_EXT8"),
("fnKEY_EXT11","KEY_EXT11","KEY_EXT11"),
("fnKEY_EXT12","KEY_EXT12","KEY_EXT12"),
("fnKEY_EXT13","KEY_EXT13","KEY_EXT13"),
("fnKEY_EXT16","KEY_EXT16","KEY_EXT16"),
("fnKEY_EXT17","KEY_EXT17","KEY_EXT17"),
("fnKEY_EXT18","KEY_EXT18","KEY_EXT18"),
("fnKEY_EXT19","KEY_EXT19","KEY_EXT19"),
("fnKEY_EXT21","KEY_EXT21","KEY_EXT21"),
("fnKEY_EXT22","KEY_EXT22","KEY_EXT22"),
("fnKEY_EXT24","KEY_EXT24","KEY_EXT24"),
("fnKEY_EXT25","KEY_EXT25","KEY_EXT25"),
("fnKEY_EXT26","KEY_EXT26","KEY_EXT26"),
("fnKEY_EXT27","KEY_EXT27","KEY_EXT27"),
("fnKEY_EXT28","KEY_EXT28","KEY_EXT28"),
("fnKEY_EXT29","KEY_EXT29","KEY_EXT29"),
("fnKEY_EXT30","KEY_EXT30","KEY_EXT30"),
("fnKEY_EXT31","KEY_EXT31","KEY_EXT31"),
("fnKEY_EXT32","KEY_EXT32","KEY_EXT32"),
("fnKEY_EXT33","KEY_EXT33","KEY_EXT33"),
("fnKEY_EXT34","KEY_EXT34","KEY_EXT34"),
("fnKEY_EXT35","KEY_EXT35","KEY_EXT35"),
("fnKEY_EXT36","KEY_EXT36","KEY_EXT36"),
("fnKEY_EXT37","KEY_EXT37","KEY_EXT37"),
("fnKEY_EXT38","KEY_EXT38","KEY_EXT38"),
("fnKEY_EXT39","KEY_EXT39","KEY_EXT39"),
("fnKEY_EXT40","KEY_EXT40","KEY_EXT40"),
("fnKEY_EXT41","KEY_EXT41","KEY_EXT41")
)

def sendKey(skey, dataSock, appstring):
  if dataSock == False :
    return False
  messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(skey))) + chr(0x00) + base64.b64encode(skey);
  part3 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
  return dataSock.send(part3);

def socketInit(tvip,tvport,timeout,remotename,tvmodel):

  #IP Address of TV
  #tvip = ""
  #IP Address of user
  myip = socket.gethostbyname(socket.gethostname())
  #Used for the access control/validation, but not after that AFAIK
  #mymac = "00-11-22-33-44-55"
  mac = iter(hex(get_mac())[3:14])
  mymac = '-'.join(a+b for a,b in zip(mac, mac))
  #What the iPhone app reports
  appstring = "iphone..iapp.samsung"
  #Might need changing to match your TV type
  tvappstring = "iphone." + tvmodel + ".iapp.samsung"
  #What gets reported when it asks for permission
  #remotename = "Python Samsung Remote"
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(timeout)
  try:
    sock.connect((tvip, tvport))
  except:
    print "Unable to connect to TV"
    return False
  ipencoded = base64.b64encode(myip)
  macencoded = base64.b64encode(mymac)
  messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) + chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) + macencoded + chr(len(base64.b64encode(remotename))) + chr(0x00) + base64.b64encode(remotename)
  part1 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring + chr(len(messagepart1)) + chr(0x00) + messagepart1
  sock.send(part1)
   
  messagepart2 = chr(0xc8) + chr(0x00)
  part2 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring + chr(len(messagepart2)) + chr(0x00) + messagepart2
  sock.send(part2)
  return sock

class SamsungSmartTVRemote(eg.PluginBase):
    def __init__(self):
       
        group = self.AddGroup('Regular Keys')
        #list = sorted(tv_keys_standard, key=lambda tup: tup[2])
        list = tv_keys_standard
        for className,code,name in list:
            clsAttributes = dict(name=name, description="<b>" + name + "</b> (" + code + ")", value=code)
            cls = ClassType(className, (KeyAction,), clsAttributes)
            group.AddAction(cls)
            
        group = self.AddGroup('Extended Keys')
        list = sorted(tv_keys_extended, key=lambda tup: tup[2])
        for className,code,name in list:
            clsAttributes = dict(name=name, description="<b>" + name + "</b> (" + code + ")", value=code)
            cls = ClassType(className, (KeyAction,), clsAttributes)
            group.AddAction(cls)
            
        group = self.AddGroup('Other Keys')
        list = sorted(tv_keys_other, key=lambda tup: tup[2])
        for className,code,name in list:
            clsAttributes = dict(name=name, description="<b>" + name + "</b> (" + code + ")", value=code)
            cls = ClassType(className, (KeyAction,), clsAttributes)
            group.AddAction(cls)
            
        self.AddAction(self.MyKey)
            
    def __start__(self, host, port, timeout, remotename, tvmodel):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.remotename = remotename
        self.tvmodel = tvmodel
    
    def Configure(
        self, 
        host="localhost", 
        port=55000,
        timeout=3,
        remotename="GhostRemote",
        tvmodel="UE50ES6710"
    ):
        panel = eg.ConfigPanel()
        hostControl = panel.TextCtrl(host)
        portControl = panel.SpinIntCtrl(port, max=65535)
        timeoutControl = panel.SpinIntCtrl(timeout, max=90)
        remotenameControl = panel.TextCtrl(remotename)
        tvmodelControl = panel.TextCtrl(tvmodel)
        tcpBox = panel.BoxedGroup("Network",("TV IP address:",hostControl),("Port:",portControl),("Connection timeout:",timeoutControl, "sec."))
        infoBox = panel.BoxedGroup("Info",("Remote control name:",remotenameControl),("TV model:",tvmodelControl))
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(infoBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(hostControl.GetValue(),portControl.GetValue(),timeoutControl.GetValue(),remotenameControl.GetValue(),tvmodelControl.GetValue())

            
    def DoCommand(self,cmd):
        sock = socketInit(self.host,self.port,self.timeout,self.remotename,self.tvmodel)
        tvappstring = "iphone." + self.tvmodel + ".iapp.samsung"
        if sendKey(cmd,sock,tvappstring) == False:
            self.TriggerEvent("Unable to connect (TV off?)!")
            return False
        sock.close()
    
    class MyKey(eg.ActionWithStringParameter):
        name = "Custom Key"
        def __call__(self, cmd):
            self.plugin.DoCommand(cmd)

class KeyAction(eg.ActionBase):
    def __call__(self):
        self.plugin.DoCommand(self.value)

