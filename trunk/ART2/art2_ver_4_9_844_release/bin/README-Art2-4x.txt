# This is an example of how to run nart.out using the
# shareable object libraries included Art2 versions
# 4.3 and later.

export LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH
cd /tmp
tftp -r libanwi.so -g 192.168.1.10
tftp -r libpart.so -g 192.168.1.10
tftp -r libfield.so -g 192.168.1.10
tftp -r liblinkAr9k.so -g 192.168.1.10
tftp -r libar9300_9-3-0.so -g 192.168.1.10
tftp -r nart.out -g 192.168.1.10
chmod +x nart.out
./nart.out -console -instance 0&





