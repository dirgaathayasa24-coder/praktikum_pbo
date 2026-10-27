from abc import ABC, abstractmethod


# ==================================================
# ABSTRAKSI: KELAS DASAR MATA UANG
# ==================================================

class MataUang(ABC):
    jumlah_mata_uang = 0

    def __init__(self, kode, nama, kurs_usd):
        self.kode = kode
        self.nama = nama
        self._kurs_usd = kurs_usd
        MataUang.jumlah_mata_uang += 1

    @abstractmethod
    def konversi_ke_usd(self, jumlah):
        pass

    @abstractmethod
    def tampilkan_info(self):
        pass

    # Method konkret yang digunakan bersama oleh subclass
    def ringkasan(self):
        print(
            f"{self.kode} - {self.nama} | "
            f"Nilai 1 unit dalam USD: ${self._kurs_usd:,.6f}"
        )

    def __str__(self):
        return f"{self.kode} ({self.nama})"

    # Operator overloading: membandingkan nilai kurs terhadap USD
    def __lt__(self, mata_uang_lain):
        return self._kurs_usd < mata_uang_lain._kurs_usd


class MataUangFiat(MataUang):
    def __init__(self, kode, nama, kurs_usd, negara):
        super().__init__(kode, nama, kurs_usd)
        self.negara = negara

    def konversi_ke_usd(self, jumlah):
        return jumlah * self._kurs_usd

    def tampilkan_info(self):
        print("Jenis        : Mata uang fiat")
        print("Negara       :", self.negara)
        self.ringkasan()


class MataUangKripto(MataUang):
    def __init__(self, kode, nama, kurs_usd, jaringan):
        super().__init__(kode, nama, kurs_usd)
        self.jaringan = jaringan

    def konversi_ke_usd(self, jumlah):
        return jumlah * self._kurs_usd

    def tampilkan_info(self):
        print("Jenis        : Mata uang kripto")
        print("Jaringan     :", self.jaringan)
        self.ringkasan()


# ==================================================
# PENGGUNA
# ==================================================

class Pengguna:
    jumlah_pengguna = 0

    def __init__(self, id_pengguna, nama):
        self.__id_pengguna = id_pengguna
        self._nama = nama
        Pengguna.jumlah_pengguna += 1

    def get_id(self):
        return self.__id_pengguna

    def get_nama(self):
        return self._nama

    def tampilkan_info(self):
        print("ID Pengguna  :", self.__id_pengguna)
        print("Nama         :", self._nama)


# ==================================================
# AGREGASI: KATALOG MENAMPUNG OBJEK MATA UANG
# ==================================================

class KatalogMataUang:
    def __init__(self, daftar_mata_uang):
        # Objek mata uang dibuat di luar katalog lalu diberikan ke sini
        self.daftar_mata_uang = daftar_mata_uang

    def tampilkan_semua(self):
        for mata_uang in self.daftar_mata_uang:
            print()
            mata_uang.tampilkan_info()

    def cari(self, kode):
        for mata_uang in self.daftar_mata_uang:
            if mata_uang.kode.upper() == kode.upper():
                return mata_uang
        return None


# ==================================================
# KOMPOSISI: DETAIL DIMILIKI OLEH TRANSAKSI
# ==================================================

class DetailTransaksi:
    def __init__(self, jumlah_asal, jumlah_hasil, kode_asal, kode_tujuan):
        self.jumlah_asal = jumlah_asal
        self.jumlah_hasil = jumlah_hasil
        self.kode_asal = kode_asal
        self.kode_tujuan = kode_tujuan

    def tampilkan_detail(self):
        print(
            f"{self.jumlah_asal:,.4f} {self.kode_asal} "
            f"= {self.jumlah_hasil:,.4f} {self.kode_tujuan}"
        )


# ==================================================
# TRANSAKSI
# ==================================================

class Transaksi:
    jumlah_transaksi = 0

    def __init__(self, id_transaksi, pengguna, mata_uang_asal,
                 mata_uang_tujuan, jumlah):
        self.id_transaksi = id_transaksi

        # Asosiasi: transaksi menggunakan pengguna dan mata uang
        self.pengguna = pengguna
        self.mata_uang_asal = mata_uang_asal
        self.mata_uang_tujuan = mata_uang_tujuan
        self.jumlah = jumlah

        # Komposisi: detail dibuat di dalam transaksi
        hasil_usd = self.mata_uang_asal.konversi_ke_usd(jumlah)
        hasil_tujuan = hasil_usd / self.mata_uang_tujuan.konversi_ke_usd(1)
        self.detail = DetailTransaksi(
            jumlah,
            hasil_tujuan,
            mata_uang_asal.kode,
            mata_uang_tujuan.kode
        )

        Transaksi.jumlah_transaksi += 1

    def tampilkan_transaksi(self):
        print("ID Transaksi :", self.id_transaksi)
        print("Pengguna     :", self.pengguna.get_nama())
        print("Konversi     :", end=" ")
        self.detail.tampilkan_detail()


# ==================================================
# DUCK TYPING
# ==================================================

class NotifikasiEmail:
    def kirim(self, pesan):
        print("Email:", pesan)


class NotifikasiSMS:
    def kirim(self, pesan):
        print("SMS  :", pesan)


def kirim_notifikasi(media, pesan):
    # Fungsi ini cukup membutuhkan objek yang memiliki method kirim()
    media.kirim(pesan)


# ==================================================
# PROGRAM UTAMA
# ==================================================

print("=" * 58)
print("       SISTEM MANAJEMEN MATA UANG DUNIA")
print("=" * 58)

print("\nBUKTI ABSTRAKSI")
print("-" * 58)
try:
    mata_uang_umum = MataUang("XXX", "Mata Uang Umum", 1)
except TypeError as error:
    print("MataUang adalah abstract class dan tidak dapat dibuat objek.")
    print("Bukti TypeError:", error)

# Kurs contoh untuk simulasi pembelajaran, bukan kurs real-time.
usd = MataUangFiat("USD", "Dolar Amerika", 1.0, "Amerika Serikat")
idr = MataUangFiat("IDR", "Rupiah Indonesia", 0.000062, "Indonesia")
eur = MataUangFiat("EUR", "Euro", 1.08, "Zona Euro")
btc = MataUangKripto("BTC", "Bitcoin", 67000.0, "Bitcoin")

katalog = KatalogMataUang([usd, idr, eur, btc])

print("\nDAFTAR MATA UANG")
print("-" * 58)
katalog.tampilkan_semua()

print("\nPOLIMORFISME MELALUI PEWARISAN")
print("-" * 58)
# Dua subclass berbeda dipanggil melalui satu loop
for mata_uang in [usd, btc]:
    print()
    mata_uang.tampilkan_info()

print("\nOPERATOR OVERLOADING")
print("-" * 58)
print("Representasi objek:", usd)
if idr < eur:
    print("Nilai 1 IDR dalam USD lebih kecil daripada nilai 1 EUR.")

pengguna = Pengguna("U001", "Meyssa")
transaksi = Transaksi("TR001", pengguna, usd, idr, 10)

print("\nDATA TRANSAKSI")
print("-" * 58)
transaksi.tampilkan_transaksi()

print("\nDUCK TYPING")
print("-" * 58)
kirim_notifikasi(NotifikasiEmail(), "Konversi mata uang berhasil.")
kirim_notifikasi(NotifikasiSMS(), "Transaksi mata uang berhasil.")

print("\nINFORMASI SISTEM")
print("-" * 58)
print("Jumlah mata uang :", MataUang.jumlah_mata_uang)
print("Jumlah pengguna  :", Pengguna.jumlah_pengguna)
print("Jumlah transaksi :", Transaksi.jumlah_transaksi)
print("\nPROGRAM SELESAI")
print("=" * 58)
