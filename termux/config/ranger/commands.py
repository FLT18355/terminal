import os
import subprocess
from ranger.api.commands import Command

class enc(Command):
    """:enc 加密当前文件"""

    def execute(self):
        filename = self.fm.thisfile.path
        cmd = f'''/data/data/com.termux/files/usr/bin/bash -c '
echo -n "密码: "
stty -echo
read pass
stty echo
echo
openssl enc -aes-256-cbc -salt -pbkdf2 -in "{filename}" -out "{filename}.enc" -k "$pass" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 加密完成: {filename}.enc"
else
    echo "❌ 加密失败"
fi
' '''
        subprocess.call(cmd, shell=True)

class dec(Command):
    """:dec 解密当前文件"""

    def execute(self):
        filename = self.fm.thisfile.path
        cmd = f'''/data/data/com.termux/files/usr/bin/bash -c '
echo -n "密码: "
stty -echo
read pass
stty echo
echo
base="{filename}"
base="${{base%.enc}}"
if [ "$base" = "{filename}" ]; then
    base="{filename}.dec"
fi
openssl enc -d -aes-256-cbc -pbkdf2 -in "{filename}" -out "$base" -k "$pass" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 解密完成: $base"
else
    echo "❌ 解密失败"
fi
' '''
        subprocess.call(cmd, shell=True)
