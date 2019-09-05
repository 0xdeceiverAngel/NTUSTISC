# lab 6 ret2plt
跟上一題 ROP 很類似

就是call 現有的func

像是這題 就是把rdi 控成`sh`

再去call 現有的`system()` 就萬事如意

為啥中間還要塞一個`ret` 據原出題者表示 可以跳上 system 但是會死掉

因為 它會用到 xmm register 會需要對齊 尾數要0x10
