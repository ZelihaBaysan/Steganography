#elimde bi örnek olması için chatGPT'ye yazdırdım 

from PIL import Image

def gizle_mesaj(ana_resim_adi, gizli_mesaj, yeni_resim_adi):
    ana_resim = Image.open(ana_resim_adi)
    mesaj_uzunlugu = len(gizli_mesaj)
    
    # Mesaj uzunluğunu ana resmin sonuna ekleyelim
    ana_resim.putpixel((0, 0), mesaj_uzunlugu)
    
    mesaj_bitleri = ''.join(format(ord(character), '08b') for character in gizli_mesaj)
    mesaj_bit_index = 0
    
    # Her pikselin RGB değerlerini değiştirerek mesajı gizleyelim
    width, height = ana_resim.size
    for y in range(height):
        for x in range(width):
            r, g, b = ana_resim.getpixel((x, y))
            
            if mesaj_bit_index < len(mesaj_bitleri):
                r = r & ~1 | int(mesaj_bitleri[mesaj_bit_index])
                mesaj_bit_index += 1
            if mesaj_bit_index < len(mesaj_bitleri):
                g = g & ~1 | int(mesaj_bitleri[mesaj_bit_index])
                mesaj_bit_index += 1
            if mesaj_bit_index < len(mesaj_bitleri):
                b = b & ~1 | int(mesaj_bitleri[mesaj_bit_index])
                mesaj_bit_index += 1
                
            ana_resim.putpixel((x, y), (r, g, b))
    
    ana_resim.save(yeni_resim_adi)

def cikar_mesaj(gizli_resim_adi):
    gizli_resim = Image.open(gizli_resim_adi)
    
    # Gizlenmiş mesajın uzunluğunu çıkaralım
    mesaj_uzunlugu = gizli_resim.getpixel((0, 0))
    
    mesaj_bits = ''
    width, height = gizli_resim.size
    for y in range(height):
        for x in range(width):
            r, g, b = gizli_resim.getpixel((x, y))
            mesaj_bits += str(r & 1)
            mesaj_bits += str(g & 1)
            mesaj_bits += str(b & 1)
            
            # Eğer mesaj uzunluğuna ulaştıysak, mesajı çıkaralım
            if len(mesaj_bits) >= mesaj_uzunlugu * 8:
                mesaj = ''
                for i in range(mesaj_uzunlugu):
                    byte = mesaj_bits[i*8:(i+1)*8]
                    mesaj += chr(int(byte, 2))
                return mesaj

# Örnek kullanım
ana_resim_adi = "ornek_resim.png"
gizli_mesaj = "Bu bir gizli mesajdır."
yeni_resim_adi = "gizli_resim.png"

# Mesajı gizle
gizle_mesaj(ana_resim_adi, gizli_mesaj, yeni_resim_adi)

# Gizli mesajı çıkar
mesaj = cikar_mesaj(yeni_resim_adi)
print("Çıkarılan Gizli Mesaj:", mesaj)

