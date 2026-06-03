import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# 1. Sayfa Başlığı
st.set_page_config(page_title="Dinamik Fonksiyon Laboratuvarı", layout="wide")
st.title("🎛️ Gelişmiş Dinamik Fonksiyon Laboratuvarı")
st.write("Sol menüden dilediğiniz kadar fonksiyon ekleyin, değerlerini değiştirin ve X sayısına gidişini canlı izleyin.")

# 2. Sol Menü - Fonksiyon Yönetimi
st.sidebar.header("🛠️ Fonksiyon Yönetim Paneli")

# Kaç adet fonksiyon olacağını hafızada tutmak için Streamlit Session State kullanıyoruz
if "fonksiyon_sayisi" not in st.session_state:
    st.session_state.fonksiyon_sayisi = 2  # Varsayılan olarak 2 fonksiyonla başlasın

# Fonksiyon Ekleme ve Çıkarma Butonları
col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    if st.button("➕ Fonksiyon Ekle"):
        st.session_state.fonksiyon_sayisi += 1
with col_btn2:
    if st.button("➖ Sonuncuyu Sil") and st.session_state.fonksiyon_sayisi > 1:
        st.session_state.fonksiyon_sayisi -= 1

# Kullanıcıdan fonksiyon katsayılarını alma
fonksiyonlar = []
Harfler = ["f", "g", "h", "p", "r", "s", "t", "k"] # Fonksiyon isimleri

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Fonksiyon Kurallarını Belirleyin:")

for i in range(st.session_state.fonksiyon_sayisi):
    harf = Harfler[i % len(Harfler)]
    st.sidebar.markdown(f"**{harf}(x) = a·x + b**")
    
    # Her fonksiyonun a ve b değerleri için yan yana iki kutu/sürgü açalım
    c1, c2 = st.sidebar.columns(2)
    with c1:
        a = float(st.number_input(f"{harf}(x) için 'a' (Eğim):", value=1.0 if i==0 else -1.0, key=f"a_{i}", step=0.5))
    with c2:
        b = float(st.number_input(f"{harf}(x) için 'b' (Sabit):", value=2.0 if i==0 else 4.0, key=f"b_{i}", step=0.5))
        
    fonksiyonlar.append({"ad": f"{harf}(x)", "a": a, "b": b})

st.sidebar.markdown("---")
# 3. Grafik Hızı ve Ortak X Girdisi
x_hedef = st.sidebar.slider("Takip edilecek X sayısını seçin (Girdi):", min_value=-10.0, max_value=10.0, value=3.0, step=0.5)
animasyon_hizi = st.sidebar.slider("Çizim Hızı:", min_value=0.01, max_value=0.1, value=0.03, step=0.01)
baslat = st.sidebar.button("🚀 Tüm Çizimleri Başlat", use_container_width=True)

# 4. Sağ Taraf - Matematiksel Sonuç Paneli ve Grafik
st.subheader("📊 Matematiksel Çıktılar (Değer Kümesi Karşılıkları):")

# Ekranı ikiye bölelim: Sol tarafta sonuç metinleri, sağ tarafta dev grafik olsun
sol_panel, sag_panel = st.columns([1, 2])

with sol_panel:
    st.markdown(f"**Girilen Girdi Elemanı:** $x = {x_hedef}$")
    sonuclar = []
    # Her fonksiyonun o X için sonucunu hesapla ve ekrana yaz
    for f in fonksiyonlar:
        y_sonuc = (f["a"] * x_hedef) + f["b"]
        sonuclar.append(y_sonuc)
        st.info(f"📍 **{f['ad']}** = {f['a']}·({x_hedef}) + {f['b']} = **{y_sonuc}** → Nokta:  **({x_hedef}, {y_sonuc})**")

with sag_panel:
    grafik_alani = st.empty()

# 5. Animasyonlu Çizim Döngüsü
def animasyonu_oynat():
    x_adimlari = np.linspace(-10, x_hedef, 40)
    renkler = ["#007BFF", "#28A745", "#DC3545", "#F39C12", "#9B59B6", "#1ABC9C"]
    
    for idx in range(1, len(x_adimlari) + 1):
        current_x = x_adimlari[:idx]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Eklenen tüm fonksiyonları sırayla çizdiriyoruz
        for s_idx, f in enumerate(fonksiyonlar):
            current_y = f["a"] * current_x + f["b"]
            renk = renkler[s_idx % len(renkler)]
            
            # Çizgiyi çiz
            ax.plot(current_x, current_y, color=renk, linewidth=2.5, label=f"{f['ad']} = {f['a']}x + {f['b']}")
            
            # Eğer animasyon son adıma geldiyse bitiş noktasına hedef işareti koy
            if idx == len(x_adimlari):
                y_son = sonuclar[s_idx]
                ax.scatter([x_hedef], [y_son], color=renk, s=150, zorder=5, edgecolors='black')
        
        # Grafik Koordinat Sistemi Ayarları
        ax.axhline(0, color='black', linewidth=1.5) # X Ekseni
        ax.axvline(0, color='black', linewidth=1.5) # Y Ekseni
        ax.set_xlim([-10, 10])
        ax.set_ylim([-15, 15])
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc="upper left", fontsize=10)
        ax.set_title("Fonksiyonların Koordinat Sistemindeki Canlı Takibi", fontsize=12)
        
        grafik_alani.pyplot(fig)
        plt.close(fig)
        time.sleep(animasyon_hizi)

# Tetikleyiciler
if baslat:
    animasyonu_oynat()
else:
    # Sayfa ilk açıldığında boş koordinat düzlemi gösterilsin
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axhline(0, color='black', linewidth=1.5)
    ax.axvline(0, color='black', linewidth=1.5)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-15, 15])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title("Başlamak için sol menüden fonksiyonları ayarlayıp butona basın.")
    grafik_alani.pyplot(fig)
    plt.close(fig)
