#!/bin/bash

echo "Assume Chrome are already installed in your Windows"

echo "Installing ChromeDriver..."

chrome_driver_windows='https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_win32.zip'
wget $chrome_driver_windows
unzip chromedriver*.zip


echo "Create chromedriver executable"

executable='./chromedriver'

# http://rolandtanglao.com/2018/05/01/p1-how-to-invoke-chromedriver-from-windows-subsystem-linux/
# https://stackoverflow.com/questions/23929235/multi-line-string-with-extra-space-preserved-indentation
cat > $executable <<- EOM
#!/bin/sh
DIR=\`dirname "\$0"\`
\$DIR/chromedriver.exe "\$@"
EOM

chmod +x $executable
