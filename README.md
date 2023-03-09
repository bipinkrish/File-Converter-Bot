# File-Converter-Bot

**A Telegram Bot that can convert Images, Videos, Audios, Fonts, Documents and Ebooks.**

**_See the Bot in Action [@FilesConvertRobot](https://t.me/filesconvertrobot)_**

---

## Variables
- `HASH` **_Your API Hash from my.telegram.org_**
- `ID` **_Your API ID from my.telegram.org_**
- `TOKEN` **_Your bot token from @BotFather_**

---

## Run Locally

You have to install Docker or Docker Compose.
Set the Environment Variables after the clone, or you can directly change it on [Line 26 - 28 in main.py](https://github.com/bipinkrish/File-Converter-Bot/blob/main/main.py?plain=1#L26) file

```
git clone https://github.com/bipinkrish/File-Converter-Bot.git
cd File-Converter-Bot
docker build . -t File-Converter
docker run File-Converter
```

---

## Supported Formats

**Images**:  *OCR, ICO, GIF, TIFF, BMP, WEBP, JP2, JPEG, JPG, PNG*

**Videos/Audios**:  *AIFF, AAC, M4A, OGA, WMA, FLAC, WAV, OPUS, OGG, MP3, MKV, MP4, MOV, AVI, M4B, VOB, DVD, WEBM, WMV*

**Documents**: *ODT, DOC, DOCX, DOTX, PDF, XML, HTML, DOTM, WPS, OTT, TXT, ODP, PPT, PPTX, PPTM, PPSX, POTM, POTX, PPS, POT, ODG, OTP, XML, ODS, XLS, HTML, XLSX, XLSM, XLTM, XLTX, OTS, XML, CSV, XLM*

**Fonts**:  *SFD, BDF, FNT, OTF, PFA, PFB, TTC, TTF, UFO, WOFF*

**eBooks**:  *EPUB, MOBI, AZW3, KFX, FB2, HTMLZ, LIT, LRF, PDB, PDF, TXT*

**Archives**:  *ZIP, RAR, 7Z, TAR, XY, GZ, BZ*

**Subtitles**: *TTML, SCC, SRT, VTT*

**Programming Languages**: *C, CPP, PY, RS, JL, KT, NIM, DART, GO, JAVA, JS, TS, JAR*

**3D Files**: *CTM, PLY, STL, 3DS, DAE, OBJ, LWO, OFF, WRL*

---

## Special Features

**COLORIZE** - *Colorize your Old B&W Images*

**TEXT-to-IMAGE** - *Get AI created Images from your Prompt*

**POSITIVE** - *Convert your Negetive Images to Positive Images*

**SPEECH-to-TEXT** - *Transcrpting from a Audio*

**TEXT-to-SPEECH** - *Generate Speech from a Text File*

**UPSCALE** - *Increase Resolution of a Image*

**TEXT-to-VIDEO** - *Get AI created Videos from your Prompt*

**SCAN** - *Get Scanned Data from QR Codes and Bar Codes*

**COMPILE** - *Get Self-Contained Linux Executable*

**RUN** - *Run a Python Program*

**Chat with AI** - *Converse with The Sarcastic Chatbot*

**AI Article Writter** - *Finish your Airticle with AI*

**TEXT-to-MUSIC** - *Generate Music from a Text*

---

## Extra Features

**Tic Tac Toe** - *Play a Tic Tac Toe with Bot or Players*

**Guess Game** - *Bot will Guess your Number*

**SAVE RESTRICTED** - *Send a Resctircted Public Chat Post's Link, Bot will Send you that Post*

**Torrent <-> Magnet** - *Send Torrent File to get Magnet Link and Viceversa*

**Time and Date** - *Send 'Time' or 'Date' keyword to get Current Time & Date in Several TimeZones*

**Maths** - *Send Math Expression (in Python Format) to get its Result*

**Base64** - *Send 'b64e string' to encode 'string' and 'b64d string' to decode 'string'*

---

# Wiki

- for converting **Images** it uses **[ImageMagic](https://imagemagick.org/)**

- for **OCR** reading of **Images** it uses **[Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/)**

- for converting **Videos** and **Audios** it uses **[FFmpeg](https://ffmpeg.org/)**

- for converting **Documents** it uses **[LibreOffice](https://www.libreoffice.org/)**

- for converting **Fonts** it uses **[FontForge](https://fontforge.org/)**

- for converting **eBooks** it uses **[Calibre](https://calibre-ebook.com/)**

- for extracting **Archives** it uses **[7zip](https://www.7-zip.org/)**

- for converting **Subtitles** it uses **[TTconv](https://github.com/sandflow/ttconv/)**

- for converting **3D Models** it uses **[OpenCTM-Tools](https://github.com/Danny02/OpenCTM/)**

- for converting **TGS** it uses **[TGSconverter](https://github.com/Benau/tgsconverter/)**

- for transpiling **Python Programs** it uses **[Py2Many](https://github.com/py2many/py2many/)**

- for transpiling **C Programs** it uses **[C4Go](https://github.com/Konstantin8105/c4go/)**

- for transpiling **Java Programs** it uses **[Jsweet](https://github.com/cincheo/jsweet/)**

- for scanning **QR & Bar Codes** it uses **[PyzBar](https://github.com/NaturalHistoryMuseum/pyzbar/)**

- for compiling **JAR** it uses **[Warp4j](https://github.com/guziks/warp4j/)**

- for compiling **C & C++** it uses **[G++](https://gcc.gnu.org/)**

- for compiling **Python** it uses **[PyInstaller](https://github.com/pyinstaller/pyinstaller/)**

- for **Colorizing Images** it uses **[DeOldify](https://github.com/jantic/DeOldify/)** hosted on **[Hugging Face](https://huggingface.co/spaces/PaddlePaddle/deoldify/)** and **[Photo-Colorizer](https://github.com/PySimpleGUI/PySimpleGUI-Photo-Colorizer)**

- for generating **AI Images** it uses **[Craiyon](https://www.craiyon.com/)** (also know as Dalle-Mini) and **[Stable Diffusion](https://github.com/Stability-AI/stablediffusion)** hosted on **[Hugging Face](https://huggingface.co/spaces/stabilityai/stable-diffusion)**


- for generating **Positive Images** it uses **[C41lab or C41](https://gist.github.com/stollcri/1aaec353a0e883888920c1b501cc1484/)**, **[Open-CV](https://opencv.org/)** and **[Negfix8](https://github.com/chrishunt/negfix8/)**

- for **Speech to Text** it uses **[Google's API](https://github.com/Uberi/speech_recognition)** and **[Open-AI's Whisper](https://github.com/openai/whisper)** hosted on **[Hugging Face](https://huggingface.co/spaces/Amrrs/openai-whisper-live-transcribe)**

- for **Text to Speech** it uses **[Google's gTTS API](https://github.com/pndurette/gTTS)** 

- for **Upscalling Images** it uses **[Zyro's Image-Upscaller](https://zyro.com/in/tools/image-upscaler)** 

- for **Torrents** it uses **[iTorrents](https://itorrents.org/)** and **[Torrent2Magnet](https://github.com/repolho/torrent2magnet)**

- for **Date and Time** it uses **[Arrow](https://github.com/arrow-py/arrow)**

- for **Maths** and **RUN** it uses **[ASTeval](https://github.com/newville/asteval)**

- for generating **3D Models** it uses **[Point-E](https://github.com/openai/point-e/)** hosted on **[Hugging Face](https://huggingface.co/spaces/openai/point-e)**

- for **Chat with AI** it uses **V23 CHATBOT hosted on [Hugging Face](https://huggingface.co/spaces/VISION23/V23ChatBot)**

- for **AI Article Writter** it uses **Bloom hosted on [Hugging Face](https://huggingface.co/spaces/huggingface/bloom_demo)**

- for **TEXT-to-MUSIC** it uses **[Riffusion](https://github.com/riffusion/riffusion) hosted on [HuggingFace](https://huggingface.co/spaces/fffiloni/spectrogram-to-music)**

- for **BG REMOVE** it uses **[MODNet](https://github.com/ZHKKKe/MODNet) hosted on [HuggingFace](https://huggingface.co/spaces/nateraw/background-remover)**
