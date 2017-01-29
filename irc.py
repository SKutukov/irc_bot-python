import socket
import string
import httplib 
import json

def getInfo(req):
    conn = httplib.HTTPConnection("swapi.co")
    conn.request("GET", "/api/"+req)
    r = conn.getresponse()
    print(r.status)
    data = r.read()
    parsedString = json.loads(data)
    conn.close()
    return parsedString["name"]+' height:'+parsedString["height"]+' mass:'+parsedString["mass"]+" birth year:"+parsedString["birth_year"]+ ' eye color:'+ parsedString["eye_color"]

def findInfo(str):
    j=-1
    with open('document.json') as json_file:
        jsonString=json_file.read()
        data = json.loads(jsonString)
        json_file.close()
        persons= data["people"]
        k=0
        for person in persons:
            name=person["name"]
            if str in  name:
                j=k
                break   
            k=k+1
        api= persons[j]["api"]
    if(j!=-1):
        return getInfo(api)
    else:
        return "Can't find character"   

HOST='irc.freenode.org'
PORT=6667
CHANNEL="#spbnet"
NICK = 'SkBot' #define nick
IDENT='SK101'
REALNAME='NANANANANANANA'
readbuffer=""
                                   
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
sock.connect((HOST, PORT)) #open port 
print sock.recv(4096)
#join chat
sock.send("NICK "+ NICK +'\r\n')
sock.send('USER SkBot SkBot SkBot :SkBot IRC\r\n') 
sock.send("JOIN "+ CHANNEL +"\n")

#sock.send('PRIVMSG ' + CHANNEL + ' :Hello, world.\r\n'); #Send a Message to the  channel    
def writeMessageToConsol(msg):
    index = msg.find("!", 0, len(msg))
    nick = msg[1:index]
    index = msg.find(" :", 0, len(msg))
    message = msg[index+len(' :'):len(msg)-1]
    print nick+': '+message

def fun():
    while 1:
        rBuffer= sock.recv(1024)
        temp=string.split(rBuffer, "\n")
        rBuffer=temp.pop( )

        for msg in temp:
                        
            if "PRIVMSG" in msg:
                print msg
                #writeMessageTo
                if "_starWars" in msg:
                    index = msg.find(" :_starWars", 0, len(msg))
                    m=msg[index+len(' :_starWars '):len(msg)-1]
                    #  print m
                    #print len(m)
                    message=findInfo(m)
                    print NICK+': '+message
                    #get nick
                    index = msg.find("!", 0, len(msg))
                    nick = msg[1:index]
                    #send message
                    if 'PRIVMSG '+CHANNEL in  msg:
                        sock.send('PRIVMSG ' + CHANNEL + ' :'+ message +'\r\n'); #Send a Message to the  channel
                    else:
                        sock.send('PRIVMSG ' + nick + ' :'+ message +'\r\n'); #Send a Message to the  channel  
                if ("show some magic" in msg )and(NICK in msg):
                    message=findInfo("Luke")
                    index = msg.find("!", 0, len(msg))
                    nick = msg[1:index]
                    if 'PRIVMSG '+CHANNEL in  msg:
                        sock.send('PRIVMSG ' + CHANNEL + ' :'+ message +'\r\n'); #Send a Message to the  channel
                        sock.send('PRIVMSG ' + CHANNEL + ' :'+ "Try more character using comand like _starWars character" +'\r\n'); #Send a Message to the  channel
                    else:
                        sock.send('PRIVMSG ' + nick + ' :'+ message +'\r\n'); #Send a Message to the  channel  
                        sock.send('PRIVMSG ' + nick + ' :'+ "Try more character using comand like: _starWars character" +'\r\n'); #Send a Message to the  channel
                if "_quit2016" in msg:
                    sock.close()    
   
            if "PING"  in msg:
                sock.send("PONG %s\r\n" % msg[1])

#findInfo("Yoda")     

fun()

sock.close()
