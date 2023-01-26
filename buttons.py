from pykeyboard import ReplyKeyboard, ReplyButton, ReplyKeyboardRemove
import helperfunctions


# suporrted extensions
VIDAUD = ("AIFF","AAC","M4A","OGA","WMA","FLAC","WAV","OPUS","OGG","MP3","MKV","MP4","MOV","AVI","M4B","VOB","DVD","WEBM","WMV")
IMG = ("SVG","OCR","ICO","GIF","TIFF","BMP","WEBP","JP2","JPEG","JPG","PNG")
LBW = ("ODT","DOC","DOCX","DOTX","PDF","XML","HTML","DOTM","WPS","OTT","TXT")
LBI = ("ODP","PPT","PPTX","PPTM","PPSX","POTM","POTX","PPS","POT","ODG","OTP","XML","PDF")
LBC = ("ODS","XLS","HTML","XLSX","XLSM","XLTM","XLTX","OTS","XML","PDF","CSV","XLM")
FF = ("SFD","BDF","FNT","OTF","PFA","PFB","TTC","TTF","UFO","WOFF")
EB = ("EPUB","MOBI","AZW3","KFX","FB2","HTMLZ","LIT","LRF","PDB","PDF","TXT")
ARC = ("ZIP","RAR","7Z","TAR","XZ","GZ","BZ")
SUB = ("TTML","SCC","SRT","VTT")
PRO = ('C','CPP','PY','RS','JL','KT','NIM','DART','GO','JAVA','JS','TS','JAR')
T3D = ('CTM','PLY','STL','3DS','DAE','OBJ','LWO','OFF','WRL')


# buttons
VAboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
VAboard.add(
ReplyButton('AIFF'),
ReplyButton('AAC'),
ReplyButton('M4A'),
ReplyButton('OGA'),
ReplyButton('WMA'),
ReplyButton('FLAC'),
ReplyButton('WAV'),
ReplyButton('OPUS'),
ReplyButton('OGG'),
ReplyButton('MP3'),
ReplyButton('MKV'),
ReplyButton('MP4'),
ReplyButton('MOV'),
ReplyButton('AVI'),
ReplyButton('GIF'),
ReplyButton('M4B'),
ReplyButton('VOB'),
ReplyButton('DVD'),
ReplyButton('WEBM'),
ReplyButton('WMV'),
ReplyButton('SENDVID'),
ReplyButton('SENDDOC'),
ReplyButton('SpeechToText')
            )    

IMGboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
IMGboard.add(
ReplyButton('OCR'),
ReplyButton('ICO'),
ReplyButton('GIF'),
ReplyButton('TIFF'),
ReplyButton('BMP'),
ReplyButton('WEBP'),
ReplyButton('JPEG'),
ReplyButton('JPG'),
ReplyButton('PNG'),
ReplyButton('SVG'),
ReplyButton('COLOR'),
ReplyButton('POSITIVE'),
ReplyButton('UPSCALE'),
ReplyButton('SCAN'),
ReplyButton('BG REMOVE'),
ReplyButton('SENDPHOTO'),
ReplyButton('SENDDOC')
            )

LBWboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
LBWboard.add(
ReplyButton('ODT'),
ReplyButton('DOC'),
ReplyButton('DOCX'),
ReplyButton('DOTX'),
ReplyButton('PDF'),
ReplyButton('XML'),
ReplyButton('HTML'),
ReplyButton('DOTM'),
ReplyButton('WPS'),
ReplyButton('OTT'),
ReplyButton('TXT'),
ReplyButton('READ'),
ReplyButton('TextToSpeech')
            )

LBIboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
LBIboard.add(
ReplyButton('ODP'),
ReplyButton('PPT'),
ReplyButton('PPTX'),
ReplyButton('PPTM'),
ReplyButton('PPSX'),
ReplyButton('POTM'),
ReplyButton('POTX'),
ReplyButton('PPS'),
ReplyButton('POT'),
ReplyButton('ODG'),
ReplyButton('OTP'),
ReplyButton('XML'),
ReplyButton('PDF')
            )

LBCboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
LBCboard.add(
ReplyButton('ODS'),
ReplyButton('XLS'),
ReplyButton('HTML'),
ReplyButton('XLSX'),
ReplyButton('XLSM'),
ReplyButton('XLTM'),
ReplyButton('XLTX'),
ReplyButton('OTS'),
ReplyButton('XML'),
ReplyButton('PDF'),
ReplyButton('CSV'),
ReplyButton('XLM')
            )       

FFboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
FFboard.add(
ReplyButton('SFD'),
ReplyButton('BDF'),
ReplyButton('FNT'),
ReplyButton('OTF'),
ReplyButton('PFA'),
ReplyButton('PFB'),
ReplyButton('TTC'),
ReplyButton('TTF'),
ReplyButton('UFO'),
ReplyButton('WOFF')
            )

EBboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
EBboard.add(           
ReplyButton('EPUB'),
ReplyButton('MOBI'),
ReplyButton('AZW3'),
ReplyButton('KFX'),
ReplyButton('FB2'),
ReplyButton('HTMLZ'),
ReplyButton('LIT'),
ReplyButton('LRF'),
ReplyButton('PDB'),
ReplyButton('PDF'),
ReplyButton('TXT')
            )

ARCboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
ARCboard.add(           
ReplyButton('EXTRACT'),
            )


SUBboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
SUBboard.add(           
ReplyButton("TTML"), 
#ReplyButton("SCC"),
ReplyButton("SRT"),
ReplyButton("VTT")
            )

PROboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
PROboard.add(           
#ReplyButton('C'), 
ReplyButton('CPP'),
#ReplyButton('PY'),
ReplyButton('RS'),
ReplyButton('JL'),
ReplyButton('KT'),
ReplyButton('NIM'),
ReplyButton('DART'),
ReplyButton('GO'),
#ReplyButton('JAVA'),
ReplyButton('TS'),
ReplyButton('JS'),
#ReplyButton('JAR'),
ReplyButton('READ'),
ReplyButton('COMPILE'),
ReplyButton('RUN')
            )

T3Dboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="convert to",resize_keyboard=True,selective=True)
T3Dboard.add(           
ReplyButton('CTM'), 
ReplyButton('PLY'),
ReplyButton('STL'),
ReplyButton('3DS'),
ReplyButton('DAE'),
ReplyButton('OBJ'),
ReplyButton('LWO'),
ReplyButton('OFF'),
#ReplyButton('WRL')
            )


# texts
VA_TEXT = helperfunctions.give_name(VIDAUD)
IMG_TEXT = helperfunctions.give_name(IMG)
LBW_TEXT = helperfunctions.give_name(LBW)
LBC_TEXT = helperfunctions.give_name(LBC)
LBI_TEXT = helperfunctions.give_name(LBI)
FF_TEXT = helperfunctions.give_name(FF)
EB_TEXT = helperfunctions.give_name(EB)
ARC_TEXT = helperfunctions.give_name(ARC)
SUB_TEXT = helperfunctions.give_name(SUB)
PRO_TEXT = helperfunctions.give_name(PRO)
T3D_TEXT = helperfunctions.give_name(T3D)


START_TEXT = f'**Images** 📷 \n__{IMG_TEXT}__\n\n\
**Videos/Audios** 📹 / 🔊 \n__{VA_TEXT}__\n\n\
**Documents** 💼 \n__{LBW_TEXT},{LBI_TEXT},{LBC_TEXT}__\n\n\
**Fonts** 🔤 \n__{FF_TEXT}__\n\n\
**eBooks** 📚 \n__{EB_TEXT}__\n\n\
**Archives** 🗄 \n__{ARC_TEXT}__\n\n\
**Subtitles** 🗯️ \n__{SUB_TEXT}__\n\n\
**Programming Languages** 👨‍💻 \n__{PRO_TEXT}__\n\n\
**3D Files** 💠 \n__{T3D_TEXT}__\n\n\
**Special** 🎁 \n__Colorize, Positive, Upscale, Text-to-Speech, Speech-to-Text, AI Image, Chat with AI, AI Article Writter, Text-to-3D, TEXT-to-MUSIC, BG REMOVE, Scan, Compile & Run__\n\n\
**Extra** ➕  \n__Play TicTacToe, Guess Game, Save Restricted Content, Torrent <-> Magnet, Time or Date, Maths & Base64__'