cd C:/Source

IF EXIST neopetsbot (
    Echo neopetsbot
 ) ELSE ( 
    git clone https://github.com/drewmrobson/neopetsbot.git
 )

cd C:\Source\neopetsbot

choco install python312 -y
pip install pytest-playwright
playwright install
pip install pytest-playwright playwright -U
pytest -rP --headed -s

cd C:/Source
rmdir /s /q neopetsbot