
**MaestroC2-V2**



– *Güvenlik Testleri İçin Gelişmiş Komuta ve Kontrol (C2) Platformu*

*MaestroC2-V2, hedef sistemler üzerinde geniş bir yelpazede komut ve kontrol işlemleri gerçekleştirebileceğiniz, özelleştirilebilir bir Komuta ve Kontrol (C2) platformudur. Bu platform, güvenlik araştırmacıları ve sızma testi uzmanları için tasarlanmıştır.*



🚀 **Özellikler**



*Çoklu İşletim Sistemi Desteği: Windows ve Linux üzerinde çalışabilen istemci ve sunucu modülleri.*

*Gelişmiş Komut Seti: Sistem bilgisi toplama, dosya yönetimi, ağ bilgisi, ekran görüntüsü alma ve daha fazlası.*

*Özelleştirilebilir Komutlar: Belirli bir komutu istemci üzerinde çalıştırın ve çıktıları anında alın.*

*Dosya Yükleme ve İndirme: Sunucu ve istemci arasında dosya transferi.*

*İstemci Yönetimi: Birden fazla istemci ile aynı anda çalışabilme.*

*Güvenli İletişim: Ağ üzerinden güvenli veri iletişimi sağlar.*




🚀 **KURULUM**



**Gereksinimler**

*Python 3.x*

*Pip (Python paket yöneticisi)*

*Git*




🔗 **Projeyi Klonlayın**

```git clone https://github.com/RamoDigitalMaestro/MaestroC2-V2.git```


**Dizine Girin**

```cd MaestroC2-V2```





📥 **Gereksinimleri Yükleyin**

```pip install -r requirements.txt```





🔌 **Sunucuyu Başlatın**

```python3 server.py -lhost [IP] -lport [PORT]```



**Hedefin Bağlanmasını Bekleyin**



.
📜 **KOMUTLAR**

**exit**: İstemci bağlantısını sonlandırır.

**execute**: Belirli bir terminal komutunu istemcide çalıştırır.

**openfile [dosya_adı]**: Belirtilen dosyanın içeriğini sunucudan istemciye gönderir.

**deletefile [dosya_adı]**: Belirtilen dosyayı siler.

**deletedirectory [dizin_adı]**: Belirtilen dizini siler.

**ls / dir**: İstemcideki mevcut dizinin içeriğini listeler.

**cd [hedef_klasör]**: İstemcideki çalışma dizinini değiştirir.

**createdirectory [klasör_adı]**: Yeni bir klasör oluşturur.

**createfile [dosya_adı]**: Yeni bir dosya oluşturur.

**editfile [metin] >> [dosya_adı]**: Belirtilen dosyanın sonuna metin ekler.

**whoami**: İstemcide oturum açmış kullanıcıyı döndürür.

**ifconfig**: İstemcinin ağ bilgilerini döndürür.

**cpu**: İstemcinin CPU bilgilerini döndürür.

**memory**: İstemcinin bellek kullanım bilgilerini döndürür.

**osinfo**: İstemcinin işletim sistemi bilgilerini döndürür.

**browser [url]**: Belirtilen URL'yi istemcide açar.

**upload**: İstemciden sunucuya dosya yükler.

**download**: İstemciden istemciye dosya indirir.

**screenshot**: İstemcinin ekran görüntüsünü alır.

**restart**: İstemciyi yeniden başlatır.

**poweroff**: İstemciyi kapatır.

**clear**: Terminali temizler.



⚠️ **Güvenlik Uyarısı**




Bu araç yalnızca yasal amaçlarla ve yetkili sistemlerde kullanılmalıdır. Herhangi bir yasa dışı kullanım kesinlikle yasaktır ve tüm sorumluluk kullanıcıya aittir.






  🧑‍💻 **Proje Yapımcısı**
[ RAMO ](https://github.com/RamoDigitalMaestro)












