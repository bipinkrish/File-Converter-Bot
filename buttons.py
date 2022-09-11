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


# texts
START_TEXT = f'--**Available formats**--\n\n\
**IMAGES** 📷 \n__{helperfunctions.give_name(IMG)}__\n\n\
**SPECIAL** 🎁 \n__COLORIZE, POSITIVE, UPSCALE, TEXT-to-SPEECH, SPEECH-to-TEXT, AI IMAGE & AI VIDEO__\n\n\
**VIDEOS/AUDIOS** 📹 / 🔊 \n__{helperfunctions.give_name(VIDAUD)}__\n\n\
**Documents** 💼 \n__{helperfunctions.give_name(LBW)},{helperfunctions.give_name(LBI)},{helperfunctions.give_name(LBC)}__\n\n\
**Fonts** 🔤 \n__{helperfunctions.give_name(FF)}__\n\n\
**EBooks** 📚 \n__{helperfunctions.give_name(EB)}__\n\n\
**Archives** 🗄 \n__{helperfunctions.give_name(ARC)}__'
VA_TEXT = helperfunctions.give_name(VIDAUD)
IMG_TEXT = helperfunctions.give_name(IMG)
LBW_TEXT = helperfunctions.give_name(LBW)
LBC_TEXT = helperfunctions.give_name(LBC)
LBI_TEXT = helperfunctions.give_name(LBI)
FF_TEXT = helperfunctions.give_name(FF)
EB_TEXT = helperfunctions.give_name(EB)
ARC_TEXT = helperfunctions.give_name(ARC)
