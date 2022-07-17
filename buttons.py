from pykeyboard import ReplyKeyboard, ReplyButton

VAboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="extension to convert",resize_keyboard=True,selective=True)
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
ReplyButton('WMV')
            )    

IMGboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="extension to convert",resize_keyboard=True,selective=True)
IMGboard.add(
ReplyButton('OCR'),
ReplyButton('ICO'),
ReplyButton('GIF'),
ReplyButton('TIFF'),
ReplyButton('TIF'),
ReplyButton('BMP'),
ReplyButton('WEBP'),
ReplyButton('JP2'),
ReplyButton('JPEG'),
ReplyButton('JPG'),
ReplyButton('PNG')
            )

LBWboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="extension to convert",resize_keyboard=True,selective=True)
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
ReplyButton('TXT')
            )

LBIboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="extension to convert",resize_keyboard=True,selective=True)
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

LBCboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="extension to convert",resize_keyboard=True,selective=True)
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

FFboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="extension to convert",resize_keyboard=True,selective=True)
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

EBboard = ReplyKeyboard(row_width=3,one_time_keyboard=True,placeholder="extension to convert",resize_keyboard=True,selective=True)
FFboard.add(           
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
ReplyButton('TXT'),
ReplyButton('ZIP')
            )