cd C:/Source

IF EXIST neopetsbot (
    Echo neopetsbot
 ) ELSE ( 
    git clone https://github.com/drewmrobson/neopetsbot.git
 )

cd C:\Source\neopetsbot

choco install python312 -y
pip install playwright
pip install pytest
pip install pytest-playwright
pip install pytest-playwright playwright -U
python -m pytest -rP --headed -s > "C:/Source/log.txt"

cd C:/Source
rmdir /s /q neopetsbot