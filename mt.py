from linepy import *
from akad.ttypes import Message
from akad.ttypes import ContentType as Type
from akad.ttypes import ChatRoomAnnouncementContents
from akad.ttypes import ChatRoomAnnouncement
from multiprocessing import Pool, Process
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib.request, urllib.parse, urllib.error, urllib.parse,antolib, subprocess, unicodedata, pafy
_session = requests.session()
from gtts import gTTS
from googletrans import Translator
#==============================================================================#

readOpen = codecs.open("read.json","r","utf-8")
#settingsOpen = codecs.open("temp.json","r","utf-8")
read = json.load(readOpen)
#settings = json.load(settingsOpen)

line = LINE('')

lineMID = line.profile.mid
lineProfile = line.getProfile()
lineSettings = line.getSettings()

oepoll = OEPoll(line)

Rfu = [line]
Exc = [line]
lineMID = line.getProfile().mid
bot1 = line.getProfile().mid
RfuBot=[lineMID]
admin = [lineMID]
Family=[lineMID]

tagmessage = []
spam = {"a":{}}
maxky = {"kw":{}}
msg_dict = {}
msg_image={}
msg_video={}
msg_sticker={}

#==============================================================================================================
settings = {
   "myProfile": {
        "coverId": "",
        "displayName": "",
        "pictureStatus": "",
        "statusMessage": ""
        }
}
myProfile = {
	"displayName": "",
  "statusMessage": "",
	"pictureStatus": ""
}
read = {
    "readPoint": {},
    "readMember": {},
    "readTime": {},
    "setTime":{},
    "ROM": {}
}

rfuSet = {
    'setTime':{},
    'ricoinvite':{},
    'winvite':{},
    }

user1 = lineMID
user2 = ""

setTime = {}
setTime = rfuSet['setTime']

contact = line.getProfile() 
backup = line.getProfile() 
backup.dispalyName = contact.displayName 
backup.statusMessage = contact.statusMessage
backup.pictureStatus = contact.pictureStatus

mulai = time.time()
lineStart = time.time()

tz = pytz.timezone("Asia/Jakarta")
timeNow = datetime.now(tz=tz)

myProfile["displayName"] = lineProfile.displayName
myProfile["statusMessage"] = lineProfile.statusMessage
myProfile["pictureStatus"] = lineProfile.pictureStatus
#==============================================================================#

def RhyN_(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@Rh'
        line.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)

#==============================================================================================================

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')

def logError(text):
    line.log("[ แจ้งเตือน ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    
def NOTIFIED_READ_MESSAGE(op):
    try:
        if read['readPoint'][op.param1]:
            if op.param2 in read['readMember'][op.param1]:
                pass
            else:
                read['readMember'][op.param1][op.param2] = True
                read['ROM'][op.param1] = op.param2
        else:
            pass
    except:
        pass
    
def load():
    global images
    global stickers
    with open("image.json","r") as fp:
        images = json.load(fp)
    with open("sticker.json","r") as fp:
        stickers = json.load(fp)
        
def sendSticker(to, version, packageId, stickerId):
    contentMetadata = {
        'STKVER': version,
        'STKPKGID': packageId,
        'STKID': stickerId
    }
    line.sendMessage(to, '', contentMetadata, 7)
    
def delete_log():
    ndt = datetime.datetime.now()
    for data in msg_dict:
        if (datetime.datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > datetime.timedelta(1):
            del msg_dict[msg_id]
            
def changeVideoAndPictureProfile(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = line.genOBSParams({'oid': lineMID, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4'})
        data = {'params': obs_params}
        r_vp = line.server.postContent('{}/talk/vp/upload.nhn'.format(str(line.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return "Failed update profile"
        line.updateProfilePicture(pict, 'vp')
        return "Success update profile"
    except Exception as e:
        raise Exception("Error change video and picture profile {}".format(str(e)))
        
def changeProfileVideo(to):
    if settings['changeProfileVideo']['picture'] == None:
        return line.sendMessage(to, "Foto tidak ditemukan")
    elif settings['changeProfileVideo']['video'] == None:
        return line.sendMessage(to, "Video tidak ditemukan")
    else:
        path = settings['changeProfileVideo']['video']
        files = {'file': open(path, 'rb')}
        obs_params = line.genOBSParams({'oid': line.getProfile().mid, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4'})
        data = {'params': obs_params}
        r_vp = line.server.postContent('{}/talk/vp/upload.nhn'.format(str(line.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return line.sendMessage(to, "Gagal update profile")
        path_p = settings['changeProfileVideo']['picture']
        settings['changeProfileVideo']['status'] = False
        line.updateProfilePicture(path_p, 'vp')

def sendMessageWithMention(to, lineMID):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(lineMID)+'}'
        text_ = '@x '
        line.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)

def sendMention(to, mid, firstmessage, lastmessage):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@x "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        line.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        line.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def mentionMembers(to, mid):
    try:
        group = line.getGroup(to)
        mids = [mem.mid for mem in group.members]
        jml = len(mids)
        arrData = ""
        if mid[0] == mids[0]:
            textx = ""
        else:
            textx = ""
        arr = []
        for i in mid:
            no = mids.index(i) + 1
            textx += "{}.".format(str(no))
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
        if no == jml:
            textx += "「 {} 」".format(str(group.name))
            textx += ""
        line.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        line.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def sendImage(to, path, name="image"):
    try:
        if settings["server"] == "VPS":
            line.sendImageWithURL(to, str(path))
    except Exception as error:
        logError(error)

def Rapid1Say(mtosay):
    line.sendText(Rapid1To,mtosay)

def restartBot():
    print ("RESETBOT..")
    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)

def waktu(secs):
  mins, secs = divmod(secs,60)
  hours, mins = divmod(mins,60)
  days,hours = divmod(hours,24)
  return '╭────────────\n├ %2d วัน %2d ชั่วโมง \n├ %2d นาที %2d วินาที\n╰────────────' % (days, hours, mins, secs)

def timeChange(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weeks, days = divmod(days,7)
    months, weeks = divmod(weeks,4)
    text = ""
    if months != 0: text += "%02d เดือน" % (months)
    if weeks != 0: text += " %02d สัปดาห์" % (weeks)
    if days != 0: text += " %02d วัน" % (days)
    if hours !=  0: text +=  " %02d ชั่วโมง" % (hours)
    if mins != 0: text += " %02d นาที" % (mins)
    if secs != 0: text += " %02d วินาที" % (secs)
    if text[0] == " ":
            text = text[1:]
    return text

def myhelp():
    myHelp = """╭────────────────
➻ Creator By @MaxGie ➻
╰────────────────
╭────────────────
│〖 คำสั่งเบื้องต้น Self 〗
├────────────────
├➻ คำสั่ง〖ใบคำสั่งเชลบอท〗
├➻ คำสั่งตั้งค่า〖คำสั่งตั้งค่า〗
├➻ คท〖ส่งคอนแทคผู้ใช้งาน〗
├➻ ออน〖ดูเวลาการใช้งาน〗
├➻ สปีด〖เช็คความเร็ว〗
├➻ รีบอท〖รีเช็ตเชลบอท〗
├➻ ข้อมูล〖ข้อมูลส่วนตัวเรา〗
├➻ ลบรัน〖ยกค้างเชิญกลุ่ม〗
├─────────────────
│〖 หมวดแทคทั้งหมด 〗
├─────────────────
├➻ แทค〖แทคคนทั้งห้อง〗
├➻ แทค〖ตามด้วยเลข〗
├➻ คท @〖ดึงคท.〗
├➻ ชื่อ @〖ดึงชื่อ〗
├➻ ตัส @〖ดึงตัส〗
├➻ mid @〖ดึงMID〗
├➻ รูป @〖ดึงรูปโปรไฟล์〗
├➻ ปก @〖ดึงปก〗
├➻ วีดีโอ @〖ดึงรูปวีดีโอ〗
├➻ บันทึก〖บันทึกก่อนก็อปทุกครั้ง〗
├➻ ก็อป @〖ก็อปปี้คอนแทค〗
├➻ กลับร่าง〖กลับคืนบัญชีหลัก〗
├➻ สแปมแทค〖พิม'สแปมแทค'ดูวิธีใช้〗
├➻ ตั้งสแปมแทค〖ข้อความ〗
├─────────────────
│〖 คำสั่งและลูกเล่นอื่น 〗
├─────────────────
├➻ จุด〖ตั้งนับคนอ่าน〗
├➻ อ่าน〖ดูคนแอบอ่าน〗
├➻ เชคapi〖เชคคำตอบโต้〗
├➻ ตั้งapi〖พิม'api'ดูวิธีใช้〗
├➻ ล้างapi〖พิม'api'ดูวิธีใช้〗
├➻ เขียน〖ข้อความ〗
├➻ ไอดีไลน์〖หาคท+IDline〗
╰─────────────────
"""
    return myHelp

def myhelpmessage():
    myHelpmessage = """╭───────────────────
➻ Creator By @MaxGie ➻
╰───────────────────
╭───────────────────
│    คำสั่งตั้งค่าทั้งหมด
│กรุณาอ่านใบคำสั่งให้ละอาด
├───────────────────
├➻ ล้างแทค〖ล้างคำสั่งแทค〗
├➻ ตั้งแทค〖พิม'ตั้งแทค'ดูวิธีใช้〗
├➻ 〖〗
├➻ 〖〗
├➻ 〖〗
├➻ 〖〗
├➻ 〖〗
├➻ 〖〗
╰───────────────────
"""
    return myHelpmessage
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if testbot["ออโต้แอด"] == True:
                line.findAndAddContactsByMid(op.param1)
                sendMention(op.param1,"",str(testbot["add"]))
            if testbot["ออโต้บล็อค"] == True:
                line.blockContact(op.param1)
            if testbot["ออโต้เข้ากลุ่ม"] == True:
                line.acceptGroupInvitation(op.param1)
                sendMention(op.param1, op.param2, "",(str(testbot["join"])))
#==============================================================================================================
        if op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != line.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
                elif text.lower() == "คำสั่ง":
                    myHelp = myhelp()
                    line.sendMessage(msg.to, str(myHelp))
                elif text.lower() == "คำสั่งตั้งค่า":
                    myHelpmessage = myhelpmessage()
                    line.sendMessage(msg.to, str(myHelpmessage))
                elif text.lower() == 'me':
                    sendMention(msg.to, sender, "〖★〗Self Bot〖★〗\n","")
                    line.sendContact(msg.to, lineMID)
                elif text.lower() == 'คท':
                    sendMention(msg.to, sender, "〖★〗Self Bot〖★〗\n","")
                    line.sendContact(msg.to, lineMID)
                elif text.lower() == 'sp' or text.lower() == "สปีด":
                    start = time.time()
                    sendMention(to,lineMID, "","\n〖 BOT SPEED 〗")
                    elapsed_time = time.time() - start
                    line.sendMessage(msg.to, "[ %s Seconds ] [ " % (elapsed_time) + str(int(round((time.time() - start) * 1000)))+" ms ]")
                elif text.lower() == 'ออน':
                    eltime = time.time() - mulai
                    van = "〔 เวลาออนบอท 〕\n"+waktu(eltime)
                    line.sendMessage(receiver,van)
                elif text.lower() == "runtime":
                    timeNow = time.time() - lineStart
                    runtime = timeChange(timeNow)
                    line.sendMessage(msg.to, "「 RUN TIME BOT 」\n {}".format(str(runtime)))
                elif text.lower() == 'รีบอท':
                    see = "https://i.pinimg.com/originals/00/15/33/0015336df0fd6bd8f36bce3b27611c58.jpg"
                    line.sendMessage(to, "Please wait....")
                    time.sleep(1)
                    line.sendImageWithURL(msg.to, str(see))
                    restartBot()
                elif text.lower() == 'reset':
                    seeq = "https://i.pinimg.com/originals/00/15/33/0015336df0fd6bd8f36bce3b27611c58.jpg"
                    line.sendMessage(msg.to,"Please wait.....")
                    time.sleep(1)
                    line.sendImageWithURL(msg.to,str(seeq))
                    restartBot()
                elif text.lower() == 'ข้อมูล' or text.lower() == "about":
                    try:
                        arr = []
                        owner = "ub90fee136a68d4602aa10f734f24ff42"
                        creator = line.getContact(owner)
                        contact = line.getContact(lineMID)
                        grouplist = line.getGroupIdsJoined()
                        contactlist = line.getAllContactIds()
                        blockedlist = line.getBlockedContactIds()
                        IdsInvit = line.getGroupIdsInvited()
                        times = time.time() - lineStart
                        runtime = timeChange(times)
                        ret_ = "╭───「 About Your 」"
                        ret_ += "\n├ ชื่อ : {}".format(contact.displayName)
                        ret_ += "\n├ กลุ่ม : {}".format(str(len(grouplist)))
                        ret_ += "\n├ เพื่อน : {}".format(str(len(contactlist)))
                        ret_ += "\n├ บล็อค : {}".format(str(len(blockedlist)))
                        ret_ += "\n├ ค้างเชิญ : {}".format(str(len(IdsInvit)))
                        ret_ += "\n├────────────"
                        ret_ += "\n├ เวลาออนบอท :"
                        ret_ += "\n├ {}".format(str(runtime))
                        ret_ += "\n├────────────"
                        ret_ += "\n├ ผู้สร้าง : {}".format(str(creator.displayName))
                        ret_ += "\n╰───「 About Your 」"
                        line.sendMessage(msg.to, str(ret_))
                        line.sendContact(msg.to, creator.mid)
                    except Exception as e:
                        line.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == "แทค" or text.lower() == "tagall":
                    if msg._from in lineMID:
                        group = line.getGroup(msg.to)
                        nama = [contact.mid for contact in group.members]
                        nm1, nm2, nm3, nm4, nm5, nm6, nm7, nm8, nm9, jml = [], [], [], [], [], [], [], [], [], len(nama)
                        if jml <= 20:
                          mentionMembers(msg.to, nama)
                        if jml > 20 and jml < 40:
                          for i in range (0, 19):
                              nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, len(nama)):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                        if jml > 40 and jml < 60:
                          for i in range (0, 19):
                              nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, 39):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                          for k in range (40, len(nama)):
                              nm3 += [nama[k]]
                          mentionMembers(msg.to, nm3)
                        if jml > 60 and jml < 80:
                          for i in range (0, 19):
                              nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, 39):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                          for k in range (40, 59):
                              nm3 += [nama[k]]
                          mentionMembers(msg.to, nm3)
                          for l in range (60, len(nama)):
                              nm4 += [nama[l]]
                          mentionMembers(msg.to, nm4)
                        if jml > 80 and jml < 100:
                          for i in range (0, 19):
                              nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, 39):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                          for k in range (40, 59):
                              nm3 += [nama[k]]
                          mentionMembers(msg.to, nm3)
                          for l in range (60, 79):
                              nm4 += [nama[l]]
                          mentionMembers(msg.to, nm4)
                          for m in range (80, len(nama)):
                              nm5 += [nama[m]]
                          mentionMembers(msg.to, nm5)
                        if jml > 100 and jml < 120:
                          for i in range (0, 19):
                              nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, 39):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                          for k in range (40, 59):
                              nm3 += [nama[k]]
                          mentionMembers(msg.to, nm3)
                          for l in range (60, 79):
                              nm4 += [nama[l]]
                          mentionMembers(msg.to, nm4)
                          for n in range (80, 99):
                              nm5 += [nama[n]]
                          mentionMembers(msg.to, nm5)
                          for o in range (100, len(nama)):
                              nm6 += [nama[o]]
                          mentionMembers(msg.to, nm6)
                        if jml > 120 and jml < 140:
                          for i in range (0, 19):
                              nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, 39):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                          for k in range (40, 59):
                              nm3 += [nama[k]]
                          mentionMembers(msg.to, nm3)
                          for l in range (60, 79):
                              nm4 += [nama[l]]
                          mentionMembers(msg.to, nm4)
                          for n in range (80, 99):
                              nm5 += [nama[n]]
                          mentionMembers(msg.to, nm5)
                          for o in range (100, 119):
                              nm6 += [nama[o]]
                          mentionMembers(msg.to, nm6)
                          for v in range (120, len(nama)):
                              nm7 += [nama[v]]
                          mentionMembers(msg.to, nm7)
                        if jml > 140 and jml < 160:
                          for i in range (0, 19):
                               nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, 39):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                          for k in range (40, 59):
                              nm3 += [nama[k]]
                          mentionMembers(msg.to, nm3)
                          for l in range (60, 79):
                              nm4 += [nama[l]]
                          mentionMembers(msg.to, nm4)
                          for n in range (80, 99):
                              nm5 += [nama[n]]
                          mentionMembers(msg.to, nm5)
                          for o in range (100, 119):
                              nm6 += [nama[o]]
                          mentionMembers(msg.to, nm6)
                          for q in range (120, 139):
                              nm7 += [nama[q]]
                          mentionMembers(msg.to, nm7)
                          for r in range (140, len(nama)):
                              nm8 += [nama[r]]
                          mentionMembers(msg.to, nm8)
                        if jml > 160 and jml < 180:
                          for i in range (0, 19):
                              nm1 += [nama[i]]
                          mentionMembers(msg.to, nm1)
                          for j in range (20, 39):
                              nm2 += [nama[j]]
                          mentionMembers(msg.to, nm2)
                          for k in range (40, 59):
                              nm3 += [nama[k]]
                          mentionMembers(msg.to, nm3)
                          for l in range (60, 79):
                              nm4 += [nama[l]]
                          mentionMembers(msg.to, nm4)
                          for n in range (80, 99):
                              nm5 += [nama[n]]
                          mentionMembers(msg.to, nm5)
                          for o in range (100, 119):
                              nm6 += [nama[o]]
                          mentionMembers(msg.to, nm6)
                          for q in range (120, 139):
                              nm7 += [nama[q]]
                          mentionMembers(msg.to, nm7)
                          for z in range (140, 159):
                              nm8 += [nama[z]]
                          mentionMembers(msg.to, nm8)
                          for f in range (160, len(nama)):
                              nm9 += [nama[f]]
                          mentionMembers(msg.to, nm9)
                          
                elif msg.text.lower().startswith("สแปมแทค "):
                    sep = text.split(" ")
                    text = text.replace(sep[0] + " ","")
                    cond = text.split(" ")
                    jml = int(cond[0])
                    if msg.toType == 2:
                        group = line.getGroup(to)
                    for x in range(jml):
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for receiver in lists:
                                contact = line.getContact(receiver)
                                #
                                sendMention(to, contact.mid, spam["a"],"")
                                
                if "แทค " in msg.text.lower() and msg.text.lower().startswith("แทค"):
                  group = line.getGroup(msg.to)
                  gMembMids = [i.displayName for i in group.members]
                  y = msg.text.replace("แทค ","")
                  b="None"
                  s = 0
                  for t in gMembMids:
                      s=s+1
                      if s==int(y):
                          b=t
                  if b=="None":
                      b="ไม่พบ"	
                      line.sendMessage(msg.to,b)
                  else:
                      g = [i.mid for i in group.members if i.displayName == b]
                      sendMessageWithMention(msg.to, str(g[0]))
                      
                elif msg.text.lower().startswith("คท "):
                    if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = line.getContact(ls)
                            mi_d = contact.mid
                            line.sendContact(msg.to, mi_d)
                            
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            ret_ = ls
                        line.sendMessage(msg.to, str(ret_))
                        
                elif msg.text.lower().startswith("ชื่อ "):
                    if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = line.getContact(ls)
                            sendMention(msg.to, contact.mid,"","\nชื่อ : {}".format(contact.displayName))
                            
                elif msg.text.lower().startswith("ตัส "):
                    if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = line.getContact(ls)
                            sendMention(msg.to, contact.mid,"","\n╭───────────────\n│  〔 สเตตัสของคนนี้ 〕╰───────────────\n{}\n────────────────".format(contact.statusMessage))
                            
                elif msg.text.lower().startswith("รูป "):
                    if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + line.getContact(ls).pictureStatus
                            line.sendImageWithURL(msg.to, str(path))
                            
                elif msg.text.lower().startswith("วีดีโอ "):
                    if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + line.getContact(ls).pictureStatus + "/vp"
                            line.sendImageWithURL(msg.to, str(path))
                            
                elif msg.text.lower().startswith("ปก "):
                    if line != None:
                        if 'MENTION' in list(msg.contentMetadata.keys())!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = line.getProfileCoverURL(ls)
                                line.sendImageWithURL(msg.to, str(path))
                                
#==============================================================================#
                elif msg.text.lower().startswith("เขียน "):
                    sep = msg.text.split(" ")
                    textnya = msg.text.replace(sep[0] + " ","")
                    urlnya = "http://chart.apis.google.com/chart?chs=480x80&cht=p3&chtt=" + textnya + "&chts=FFFFFF,70&chf=bg,s,000000"
                    line.sendImageWithURL(msg.to, urlnya)
    
                elif msg.text.lower().startswith("ไอดีไลน์ "):
                    id = msg.text.lower().replace("ไอดีไลน์ ","")
                    conn = line.findContactsByUserid(id)
                    if True:                                      
                        line.sendMessage(to,"http://line.me/ti/p/~" + id)
                        line.sendContact(to,conn.mid)
#==============================================================================#

                elif "ลบรัน" in msg.text.lower():
                    spl = re.split("ลบรัน",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                        spl[1] = spl[1].strip()
                        ag = line.getGroupIdsInvited()
                        txt = "กำลังยกเลิกค้างเชิญจำนวน "+str(len(ag))+" กลุ่ม"
                        if spl[1] != "":
                            txt = txt + " ด้วยข้อความ \""+spl[1]+"\""
                        txt = txt + "\nกรุณารอสักครู่.."
                        line.sendMessage(msg.to,txt)
                        procLock = len(ag)
                        for gr in ag:
                            try:
                                line.acceptGroupInvitation(gr)
                                if spl[1] != "":
                                    line.sendMessage(gr,spl[1])
                                line.leaveGroup(gr)
                            except:
                                pass
                        line.sendMessage(msg.to,"สำเร็จแล้ว (｀・ω・´)")
                        
#==============================================================================#
                elif "ก็อป " in msg.text:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            line.cloneContactProfile(ls)
                            line.sendContact(to, sender)
                            line.sendMessage(to, "คัดลอกบัญชีเรียบร้อยแล้ว (｀・ω・´)")
                elif msg.text in ["บันทึก"]:
                    try:
                        lineProfile = line.getProfile()
                        settings["myProfile"]["displayName"] = str(lineProfile.displayName)
                        settings["myProfile"]["statusMessage"] = str(lineProfile.statusMessage)
                        settings["myProfile"]["pictureStatus"] = str(lineProfile.pictureStatus)
                        coverId = line.getProfileDetail()["result"]["objectId"]
                        settings["myProfile"]["coverId"] = str(coverId)
                        line.sendMessage(to, "บันทึกสถานะบัญชีเรียบร้อยแล้ว (｀・ω・´)")
                    except Exception as error:
                        logError(error)							
                        line.sendMessage(to, "ไม่สามารถบันทึกสถานะบัญชีได้ (｀・ω・´)")
                 
                elif msg.text in ["กลับร่าง"]:
                    try:
                        lineProfile = line.getProfile()
                        lineProfile.displayName = str(settings["myProfile"]["displayName"])
                        lineProfile.statusMessage = str(settings["myProfile"]["statusMessage"])
                        linePictureStatus = line.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(str(settings["myProfile"]["pictureStatus"])), saveAs="tmp/backupPicture.bin")
                        coverId = str(settings["myProfile"]["coverId"])
                        line.updateProfile(lineProfile)
                        line.updateProfileCoverById(coverId)
                        line.updateProfilePicture(linePictureStatus)
                        line.sendMessage(to, "เรียกคืนสถานะบัญชีเรียบร้อยแล้ว (｀・ω・´)")
                        line.sendContact(to, sender)
                        line.deleteFile(linePictureStatus)
                    except Exception as error:
                        logError(error)							
                        line.sendMessage(to, "ไม่พบข้อมูลการบันทึกบัญชี (｀・ω・´)")
#==============================================================================#
                elif text.lower() == "สแปมแทค":
                   try:
                       maxgie = "╭───────────────"
                       maxgie += "\n│วิธีการใช้สแปมแทค:\n│พิม คำสั่ง จำนวน @แทค\n│ดูตัวอย่าง:\n│สแปมแทค 10 @แทค\n│ขอบคุณที่ให้ความร่วมมือ・ω・"
                       maxgie += "\n╰───────────────"
                       line.sendMessage(msg.to, str(maxgie))
                   except Exception as error:
                      logError(error)
            
                elif msg.text.startswith("ตั้งสแปมแทค "):
                   if msg._from in admin:
                       spl = msg.text.replace("ตั้งสแปมแทค ","")
                       if spl in [""," ","\n",None]:
                           line.sendMessage(msg.to,"เกิดข้อผิดปกติกับระแบบสแปมแทค (｀・ω・´)")
                       else:
                           spam["a"] = spl
                           line.sendMessage(msg.to,"「 SET SPAM TAG 」\nตั้งคำสแปมว่า : {}".format(spl))
#==============================================================================#
        if op.type == 25 or op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != line.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
                if msg.text.lower() == "จุด" or text.lower() == ".":
                  group = line.getGroup(msg.to)
                  groupMemberMids = [i.mid for i in group.members if i.mid in admin]
                  b=  "พิมว่า อ่าน เพื่อดูสมาชิกที่อ่านข้อความ (｀・ω・´)"
                  if lineMID in groupMemberMids:
                      line.sendMessage(msg.to, b)
                  else:
                      line.sendMessage(msg.to,b)
                  try:
                      del read['readPoint'][msg.to]
                      del read['readMember'][msg.to]
                  except:
                      pass
                  read['readPoint'][msg.to] = True
                  read['readMember'][msg.to] = {}
                  read['ROM'][msg.to] = {}
                  
                if msg.text.lower() == "อ่าน" or text.lower() == "read":
                  group = line.getGroup(msg.to)
                  groupMemberMids = [i.mid for i in group.members if i.mid in admin]
                  if msg.to in read['readPoint']:
                      if read["ROM"][msg.to] == {}:
                          ed = "\nไม่มีใครอ่าน"
                          lread = "ไม่มีใครอ่าน"
                      else:
                          ed = ""
                          for i in read["readMember"][msg.to]:
                              ed += "\n- " + line.getContact(i).displayName
                          lr = read["ROM"][msg.to]
                          lread = "- " + line.getContact(lr).displayName

                      b="รายชื่อสมาชิกที่อ่านทั้งหมด\n\nสมาชิกที่อ่าน" + ed + "\n\nสมาชิกที่อ่านล่าสุด\n"+lread+"\n\nพิมพ์ จุด เพื่อตั้งจุดอ่านใหม่ (｀・ω・´)"

                      if lineMID in groupMemberMids:
                          line.sendMessage(msg.to, b)
                      else:
                          line.sendMessage(msg.to,b)
                  else:
                      b="คุณยังไม่ได้ตั้งจุดอ่าน พิมพ์ จุด เพื่อตั้งจุดอ่าน (｀・ω・´)"
                      if lineMID in groupMemberMids:
                          line.sendMessage(msg.to, b)
                      else:
                          line.sendMessage(msg.to,b)
#==============================================================================#
        if op.type == 26 or op.type == 25:
            msg = op.message
            sender = msg._from
            try:
               if maxky["kw"][str(msg.text)]:
                   line.sendMessage(msg.to,maxky["kw"][str(msg.text)])
            except:
              pass
#==============================================================================#
        if op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != line.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
                if msg.text is None:
                    return
                if msg.text.lower() == "api":
                    mas = "╭────────────"
                    mas += "\n│ดูตัวอย่าง:\n│ตั้งapi เทส;;เทสอะไรครับ"
                    mas += "\n│ต้องมี ;; ทุกครั้ง"
                    mas += "\n╰────────────"
                    line.sendMessage(msg.to,mas)
                if msg.text.lower() == "เชคapi":
                    lisk = "[ คำสั่งตอบโต้ ]\n"
                    for i in maxky["kw"]:
                        lisk+="\nคีย์เวิร์ด: "+str(i)+"\nตอบโต้: "+str(maxky["kw"][i])+"\n"
                    line.sendMessage(msg.to,lisk)
                if msg.text.startswith("ล้างapi "):
                    try:
                        delcmd = msg.text.split(" ")
                        getx = msg.text.replace(delcmd[0] + " ","")
                        del maxky["kw"][getx]
                        line.sendMessage(msg.to, "คำตอบโต้ " + str(getx) + " ล้างแล้ว")
                        f=codecs.open('sb.json','w','utf-8')
                        json.dump(maxky, f, sort_keys=True, indent=4, ensure_ascii=False)
                    except Exception as Error:
                        print(Error)
                if msg.text.startswith("ตั้งapi "):
                    try:
                        delcmd = msg.text.split(" ")
                        get = msg.text.replace(delcmd[0]+" ","").split(";;")
                        kw = get[0]
                        ans = get[1]
                        maxky["kw"][kw] = ans
                        f=codecs.open('sb.json','w','utf-8')
                        json.dump(maxky, f, sort_keys=True, indent=4, ensure_ascii=False)
                        line.sendMessage(msg.to,"คีย์เวิร์ด: " + str(kw) + "\nตอบกลับ: " +str(ans))
                    except Exception as Error:
                        print(Error)
                if msg.text.lower() == "ตั้งแทค":
                    asw = "╭──────────────"
                    asw += "\n│ดูตัวอย่าง:"
                    asw += "\n│ตั้งแทค แทคทำไม??? {name}{tag}{contact}{pict}"
                    asw += "\n│{name} คือชื่อคนแทค"
                    asw += "\n│{tag} คือแทคคนแทค"
                    asw += "\n│{contact} คือคท.คนแทค"
                    asw += "\n│{pict} คือรูปคนแทค"
                    asw += "\n│4 อันนี้สามารถเลือกใช้ได้"
                    asw += "\n├──────────────"
                    asw += "\n│ตั้งเสร็จให้พิม'tag'ครับ"
                    asw += "\n│เพื่อเชคดูคำสั่ง (｀・ω・´)"
                    asw += "\n╰──────────────"
                    line.sendMessage(msg.to, asw)
                if msg.text.lower() == "tag":
                    try:
                        tagmessage = maxky["tag"]
                        user = line.getContact(msg._from)
                        get = tagmessage.replace("{name}",user.displayName)
                        if "{tag}" in tagmessage:
                            taguser = user.mid
                        get = get.replace("{tag}","")
                        if "{pict}" in get:
                            pict = "http://dl.profile.line-cdn.net/" + user.pictureStatus
                        get = get.replace("{pict}","")
                        if "{contact}" in get:
                            contact = user.mid
                        get = get.replace("{contact}","")
                        line.sendMessage(msg.to,get)
                        sendMessageWithMention(msg.to,taguser)
                        line.sendContact(msg.to,contact)
                        line.sendImageWithURL(msg.to,pict)
                    except Exception as Error:
                        print(Error)
                if msg.text.lower().startswith("ตั้งแทค "):
                    try:
                        delcmd = msg.text.split(" ")
                        replacecmd = msg.text.replace(delcmd[0] + " ","")
                        maxky["tag"] = replacecmd
                        line.sendMessage(msg.to,"ตั้งคำสั่งตอบกลับคนแทคแล้ว (｀・ω・´)")
                        f=codecs.open('sb.json','w','utf-8')
                        json.dump(maxky, f, sort_keys=True, indent=4, ensure_ascii=False)
                    except Exception as Error:
                        print(Error)
                if msg.text.lower() == "ล้างแทค":
                    maxky["tag"] = ""
                    line.sendMessage(msg.to,"ล้างแทคเรียบร้อบ... (｀・ω・´)")
#==============================================================================#
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != line.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
                if msg.contentType == 0 and sender not in lineMID and msg.toType == 2:
                   if "MENTION" in list(msg.contentMetadata.keys())!= None:
                      tagmessage = maxky["tag"]
                      user = line.getContact(msg._from)
                      name = re.findall(r'@(\w+)', msg.text)
                      mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                      mentionees = mention['MENTIONEES']
                      for mention in mentionees:
                          if mention['M'] in lineMID:
                              get = tagmessage.replace("{name}",user.displayName)
                              if "{tag}" in tagmessage:
                                  taguser = user.mid
                                  get = get.replace("{tag}","")
                              if "{pict}" in get:
                                  pict = "http://dl.profile.line-cdn.net/" + user.pictureStatus
                                  get = get.replace("{pict}","")
                              if "{contact}" in get:
                                  contact = user.mid
                                  get = get.replace("{contact}","")
                              line.sendMessage(msg.to,str(get))
                              sendMessageWithMention(msg.to,str(taguser))
                              line.sendContact(msg.to,str(contact))
                              line.sendImageWithURL(msg.to,str(pict))
#==============================================================================#
        if op.type == 55:
            print ("ตรวจพบข้อความ")
            NOTIFIED_READ_MESSAGE(op)
    except Exception as error:
        logError(error)
#==============================================================================#
def a2():
    now2 = datetime.now()
    nowT = datetime.strftime(now2,"%M")
    if nowT[14:] in ["10","20","30","40","50","00"]:
        return False
    else:
        return True

while True:
    try:
        ops = oepoll.singleTrace(count=5)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)

def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
atexit.register(atend)
