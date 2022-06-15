
import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from nltk.corpus import stopwords
import re
import PySimpleGUI as sg
import pymsgbox
from urllib.parse import urlparse


#nltk.download('stopwords')


stopWords = stopwords.words('english')


def isBitCoinAddress(address):
    result = True 
    
    if(len(address) > 35 or len(address) < 26):
        result = False
    elif(address[0] != '1' and address[0] != '3' and address[:3] != 'bc1'):
        result = False
    else:
        for char in address:
            if(not char.isalpha() and not char.isnumeric()):
                result = False
            elif(char == 'O' or char == 'I' or char == 'l' or char == '0'):
                result = False

    return result


symbols = ['~', ':', "'", '+', '[', '\\', '@', 
           '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', 
           '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']

def vectorize(tokens):
    vector=[]
    for w in filtered_vocab:
        vector.append(tokens.count(w))
    return vector
def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


filtered_vocab = []



def extractFeatures(fileData):
    
    try:
        lines = []
        
        for line in fileData.splitlines():
            lines.append(line)
        
       
        fileDataNoPunc = fileData.translate(str.maketrans('', '', string.punctuation))
        fileDataNoPunc = fileDataNoPunc.lower()
        

        
        tokens = fileDataNoPunc.split()
        
        vocab = unique(tokens)
        
        for w in vocab: 
            if w not in stopWords and w not in symbols: 
                filtered_vocab.append(w)
                        
        vector1 = vectorize(tokens)
        
        CountVec = CountVectorizer(ngram_range=(1,1),
                                   stop_words='english')
        
        Count_data = CountVec.fit_transform([fileData])
        
        cv_dataframe=pd.DataFrame(Count_data.toarray(),columns=CountVec.get_feature_names_out())
        pd.set_option('display.width', 120)
        
        
        top20Words = cv_dataframe.iloc[0].nlargest(50).index
        
        emails = list(dict.fromkeys(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", fileData.lower())))
        
        urls = list(dict.fromkeys(re.findall("(?P<url>https?://[^\s]+)", fileData.lower())))
        
        extractedURLS = []
     
        for i in range(0, len(urls)):
           
            parsed = urlparse(urls[i])
        
            
            if(parsed.netloc == 'mega.nz' and parsed.fragment == ''):
                url =  parsed.scheme + "://"  + parsed.netloc + parsed.path
                
            elif(parsed.netloc == 'mega.nz' and parsed.fragment != ''):
                url =  parsed.scheme + "://"  + parsed.netloc + "/" + parsed.fragment
                
            else:
                url = parsed.scheme + "://"  + parsed.netloc 
                
            extractedURLS.append(url)
        
            
        extractedURLS = list(dict.fromkeys(extractedURLS))
        
        return emails, top20Words, extractedURLS, lines
        
        
    except:
        print("An exception occurred")
        
        return None, None, None
        
        
        
def getRansType(email, topWords, dropType, links, lines):
    
    ransType = ""


    
    if(not email and not links and dropType == "Text Only"):
        if('alcatraz' in topWords):
            ransType = 'Alcatraz'
        elif(len(lines) >= 2 and 'send' in lines[0].lower() and 'bitcoins' in lines[0].lower() and isBitCoinAddress(lines[1])):
            ransType = 'ZeroFucks'
        elif(len(lines) >= 17 and 'send' in lines[15].lower() and 'bitcoin' in lines[15].lower()  and isBitCoinAddress(lines[16])):
            ransType = 'Jigsaw'
        else:
            ransType = 'UNKNOWN'
      
        
    elif(not email and links and  dropType == "Text Only"):
        if('nemty' in topWords and ('http://nemty.top' in links or
                                    'http://zjoxyw5mkacojk5ptn2iprkivg5clow72mjkyk5ttubzxprjjnwapkad.onion' in links)):
            ransType = 'Nemty'
        elif('gandcrab' in topWords and 'http://gandcrabmfe6mnef.onion' in links):
               ransType = 'Gandcrab'
        elif('http://pylockyrkumqih5l.onion' in links):
            ransType = 'PyLocky'
        elif('http://n224ezvhg4sgyamb.onion' in links):
            ransType = 'GlobeImposter'
        elif('jaff' in topWords and 'http://rktazuzi7hbln7sy.onion' in links):
            ransType = 'Jaff'
        elif('http://uk74sqtx2ynr2nzb.onion.gq' in links or 
             'http://uk74sqtx2ynr2nzb.onion.nu' in links or'http://uk74sqtx2ynr2nzb.onion.cab' in links or 
             'http://uk74sqtx2ynr2nzb.onion.to' in links):
            ransType = 'BartRansom'
        elif(len(lines) >= 33 and 'send' in lines[31].lower()  and ('btc' in lines[31].lower() or 'bitcoin' in lines[31].lower()) and isBitCoinAddress(lines[32])):
             ransType = 'Malboro'
        else:
            ransType = 'UNKNOWN'
            
            
        
    elif(email and links and dropType == "Text Only"):
        if('hildacrypt' in topWords and ('hildaseriesnetflix125@tutanota.com' in email or 'hildaseriesnetflix125@horsefucker.org' in email)):
            ransType = 'HildaCrypt'
        elif('hakbit@protonmail.com' in email):
              ransType = 'Hakbit'
        elif('bigbobross@computer4u.com' in email):
             ransType = 'BigBobRoss'
        elif(('0xc030@protonmail.ch' in email or '0xc030@tuta.io' in email or'aes-ni@scryptmail.com' in email) and 'aes' in topWords 
             and 'ni' in topWords):
            ransType = 'AES_NI'
        elif('info@decrypt.ws' in email):
            ransType = 'Paradise'
        elif('lordcracker@protonmail.com' in email or 'phabos@cock.li' in email):
            ransType = 'SpartCrypt'
        elif('lambdasquad' in topWords and 'lambdasquad.hl@yandex.com' in email):
            ransType = 'LambdaLocker'
        else:
            ransType = 'UNKNOWN'
            
            
            
    elif(email and not links and dropType == "Text Only"): 
        if('support.mbox@pm.me' in email and 'mapo' in topWords):
            ransType = 'Morpa'
        elif('s1an1er111@protonmail.com' in email):
            ransType = 'Amnesia'
        elif('nano18@airmail.cc' in email):
            ransType = 'Aurora'
        elif('unlocksupp@airmail.cc' in email or 'bm-2ctvhx6b7ryhj9ggkzn6ytubpbbq3lhrkz@bitmessage.ch' in email):
             ransType = 'BTCware'
        elif('biger@x-mail.pro' in email):
            ransType = 'Cryakl'
        elif('bufalo' in topWords and 'bufalo@boximail.com' in email):
            ransType = 'Crypt888'
        elif('dllteam@protonmail.com' in email or 'dllteam1@protonmail.com' in email or 'dllpc@mail.com' in email or 'dllpc@tuta.io' in email 
             or 'claremohan@tuta.io' in email or 'claremohan@yandex.com' in email or 'mohanclare@yandex.com' in email):
            ransType = "Cryptomix"
        elif('embrace' in topWords and 'embrace@airmail.cc' in email):
            ransType = 'Embrace'
        elif('centrumfr@india.com' in email):
            ransType = 'FenixLocker'
        elif('filesl0cker' in topWords and 'bakfiles@protonmail.com' in email):
            ransType = 'FilesLocker'
        elif('yatronraas@mail.ru' in email):
            ransType = 'Yatron'
        elif('xdata' in topWords and ('begins@colocasia.org'in email or 'bilbo@colocasia.org' in email
        or 'frodo@colocasia.org' in email or 'trevor@thwonderfulday.com' in email or 'bob@thwonderfulday.com' in email 
        or 'bil@thwonderfulday.com' in email)):
            ransType = 'Xdata'
        elif('c-m58@mail.ru' in email):
            ransType = 'Thanatos'
        elif('syrk' in topWords and 'panda831@protonmail.com' in email):
            ransType = 'Syrk'
        elif('recoverymydata@protonmail.com' in email or'recoverydata@india.com'  in email):
            ransType = 'Mira'
        elif('mrlocker@protonmail.com' in email):
            ransType = 'Stampado'
        elif('rememberggg@tutanota.com.you' in email):
            ransType = 'InsaneCrypt'
        elif('backfilehelp@protonmail.com' in email):
            ransType = 'Ouroboros'
        elif('auguststeen@writeme.com' in email or 'auguststeen@india.com' in email):
            ransType = 'Mole'
        elif('symmetries@tutamail.com' in email or 'symmetries0@tutanota.com' in email):
            ransType = 'JSworm4'
        elif('cyborgyarraq@protonmail.ch' in email):
            ransType = 'HiddenTear'
        elif('getcrypt' in topWords and 'getcrypt@cock.li' in email):
            ransType = 'GetCrypt'
        else:
            ransType = 'UNKNOWN'
        
            
            
            
    elif(not email and not links and dropType == "GUI"):
        if('derialock' in topWords):
            ransType = 'Derialock'
        elif('dragoncyber' in topWords):
            ransType = 'DragonCyber'
        elif('pewdiepie' in topWords):
             ransType = 'PewCrypt'
        elif('wanadecryptor' in topWords):
            ransType = 'Wannacry'
        elif(len(lines) >= 18 and 'send' in lines[16].lower() and 'btc' in lines[16].lower() and isBitCoinAddress(lines[17])):
            ransType = 'NoobCrypt'
        else:
            ransType = 'UNKNOWN'    
        
        
        
    elif(not email and links and  dropType == "GUI"):
         if('petya' in topWords and 'http://petya37h5tbhyvki.onion' in links):
             ransType = 'Petya'
         elif('http://3kxwjihmkgibht2s.wh47f2as19.com' in links or 'http://34r6hq26q2h4jkzj.7hwr34n18.com' in links 
              or 'https://3kxwjihmkgibht2s.s5.tor-gateways.de' in links or 'http://34r6hq26q2h4jkzj.onion' in links):
             ransType = 'TeslaCrypt_V1'
         elif('cerber' in topWords and ('http://p27dokhpz2n7nvgr.onion' in links or
                                        'http://p27dokhpz2n7nvgr.14ewqv.top' in links or 'http://p27dokhpz2n7nvgr.14vvrc.top' in links
                                        or 'http://p27dokhpz2n7nvgr.129p1t.top' in links or'http://p27dokhpz2n7nvgr.1apgrn.top' in links 
                                        or 'http://p27dokhpz2n7nvgr.1p5fwl.top' in links)):
            ransType = 'Cerber'
         elif('chimera' in topWords and 'https://mega.nz/chimeradecrypter' in links):
                ransType = 'Chimera-SecondSample'
         elif('https://mega.nz/!kclrviry!yruggjvldsotunzbcojebaz5la7hbb41njhk1mlgqzo' in links):
             ransType = 'LooCipher'
         elif('http://ert54nfh6hdshbw4f.nursespelk.com' in links 
              or 'http://kk4dshfjn45tsnkdf34fg.tatiejava.at' in links or'http://akdfrefdkm45tf33fsdfsdf.yamenswash.com' in links):
             ransType = 'TeslaCrypt_V4'
         else:
            ransType = 'UNKNOWN'
        
        
        
    elif(email and links and dropType == "GUI"):
        if('cerys.stone2@aol.com' in email or 'amani_crisp2@aol.com' in email):
            ransType = 'CrySIS'
        elif('bitpandacom@qq.com' in email):
            ransType = 'Dharma'
        elif('bithash@india.com' in email):
            ransType = 'Globe_V3'
        else:
            ransType = 'UNKNOWN'
        
        
        
    else:
        if('tits' in topWords and 'sashagrey@blurred.credit' in email):
            ransType = "Iwanttits"
        elif('filelocker@protonmail.ch' in email):
            ransType = 'Chernolcoker'
        elif('bitpandacom@qq.com' in email):
            ransType = 'Dharma'
        elif('cerys.stone2@aol.com' in email or 'amani_crisp2@aol.com' in email):
            ransType = 'CrySIS'
        else:
            ransType = 'UNKNOWN'
        

        
    return ransType
    
    


sg.theme('SandyBeach')   # Add a touch of color

options = []

# All the stuff inside your window.
layout = [  [sg.Text('Enter the text you found in your ransom note')],
            [sg.Button('Submit'), sg.Button('Close Window')],
            [sg.Text("RESULT HERE", size=(0, 1), key='Output')],
            [sg.Text('Choose Drop Type',size=(30, 1), font='Lucida',justification='left')],
            [sg.Combo(['GUI','Text Only'],key='dropType')],
            [sg.Multiline(size=(150, 30), key='textbox')]]  # identify the multiline via key option

# Create the Window
window = sg.Window('Ransom Tool', layout).Finalize()
#window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    
    if(values['textbox'] == ""):
        pymsgbox.alert('Do not leave textbox empty!!!', 'Error')
        continue
    if(values['dropType'] == ""):
        pymsgbox.alert('Choose a drop type!!!', 'Error')
        continue

    email, topWords, urls, lines= extractFeatures(values['textbox'])
        
  
    #ransType = getRansType(email, topWords, values['dropType'], urls, lines)
    #window['Output'].update(value=ransType)
    
    
        

window.close()








