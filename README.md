Tugas Aljabar Linear

Program ini adalah implementasi Vector Space Model untuk sistem temu balik informasi. Program dibuat menggunakan bahasa Python murni dengan bantuan library NLTK untuk pemrosesan teks dasar.

Cara Menjalankan Program
Pastikan Anda sudah menginstal Python 3 di komputer.
1. Buka Terminal atau Command Prompt, lalu arahkan ke dalam folder proyek ini.
2. Instal library NLTK dengan menjalankan perintah:
   `pip install -r requirements.txt`
3. Jalankan program dengan format perintah `python vsm.py <file_base> <file_query>`. Contohnya:
   `python vsm.py base.txt query1.txt`

Penjelasan Singkat Algoritma
Program ini bekerja melalui 4 tahapan utama:
- Preprocessing : Teks dari setiap dokumen dan query diubah menjadi huruf kecil (case-folding). Setelah itu, teks dipotong menjadi kata-kata (tokenisasi), dibersihkan dari tanda baca dan stopwords (kata umum bahasa Inggris), lalu diubah ke kata dasarnya (stemming) menggunakan NLTK.
- Inverted Index : Program menghitung frekuensi kemunculan setiap kata (Term Frequency) di masing-masing dokumen untuk membuat kamus kata.
- Pembobotan TF-IDF : Nilai TF digabungkan dengan nilai IDF (Inverse Document Frequency) menggunakan rumus logaritma untuk mencari seberapa penting bobot sebuah kata di dalam dokumen tersebut.
- Perangkingan (Cosine Similarity) : Program mencari nilai kedekatan (kemiripan) antara vektor dokumen dan vektor query menggunakan rumus Cosine Similarity (perkalian titik dibagi panjang vektor). Dokumen kemudian diurutkan dari nilai kemiripan tertinggi ke terendah.

Contoh Hasil Keluaran
Ketika program selesai dijalankan, akan muncul 3 file output baru:

A. index.txt
Menampilkan daftar kata dan di dokumen mana saja kata itu muncul beserta frekuensinya. Contoh:
land: 1,1
mclaren: 1,1 4,1
norri: 1,1
win: 1,1

weights.txt
Menampilkan bobot kata untuk masing-masing dokumen. Contoh:
doc1.txt: land, 0.6990 mclaren, 0.3979 norri, 0.6990 win, 0.6990
doc4.txt: mclaren, 0.3979 upgrad, 0.6990 pack, 0.6990

response.txt
Menampilkan jumlah dokumen yang relevan (baris pertama), diikuti urutan dokumen dari yang paling mirip dengan query beserta nilai Cosine Similarity-nya. Contoh:
2
doc1.txt 0.5640
doc4.txt 0.1835