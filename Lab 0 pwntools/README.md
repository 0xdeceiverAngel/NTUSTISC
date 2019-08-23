# lab 0
它會read 4 byte

轉成ascii  比較比較
```
read(0, &magic, 4);
if (magic != 3735928559)
--------------------------------
p32(3735928559)='\xef\xbe\xad\xde'
```
就是寫腳本爆破

只是`read(0, &magic, 4);`

不知道為啥它要加`&`
