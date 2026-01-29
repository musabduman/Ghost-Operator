import sys
if len(sys.argv)>2:
    isim=sys.argv[1]
    puan=sys.argv[2]
    print(f"{isim} şu kadar puan almış {puan}")
    print("işlem başarıyla gerçekleşti")
else:
    print("bir sorun oldu")
