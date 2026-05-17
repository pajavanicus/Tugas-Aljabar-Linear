Tugas Vector Space Model (VSM) - Aljabar Linear

Program ini adalah implementasi Vector Space Model (VSM) untuk sistem temu balik informasi (Information Retrieval). Program dibuat menggunakan bahasa Python 3 dengan bantuan library NLTK untuk pemrosesan teks. Dataset dokumen teks yang digunakan di dalam program ini berbentuk artikel naratif seputar balapan Formula 1 Grand Prix Miami 2026.

1. Cara Menjalankan Program
Sebelum menjalankan program, pastikan Anda sudah menginstal Python 3 di komputer Anda.
1. Buka Terminal atau Command Prompt, lalu masuk ke dalam folder proyek `vsm`

2. Instal library NLTK yang dibutuhkan dengan menjalankan perintah berikut:
   `pip install -r requirements.txt`

3. Jalankan program utama dengan format perintah `python vsm.py <file_base> <file_query>`. Contohnya:
   `python vsm.py base.txt query1.txt`
   *(Atau gunakan `py vsm.py base.txt query1.txt` jika sistem Anda menggunakan perintah `py`)*

2. Penjelasan Singkat Algoritma
Algoritma program ini dibangun secara prosedural tingkat pemula yang dibagi menjadi 4 tahapan utama:
- Preprocessing (NLTK): Mengubah seluruh teks dokumen dan query menjadi huruf kecil (case folding). Selanjutnya, teks dipotong menjadi kata-kata (tokenisasi), dibersihkan dari tanda baca serta kata hubung logika (and, or, not), dihapus dari kata-kata umum bahasa Inggris (stopwords), dan direduksi ke bentuk kata dasarnya (stemming) menggunakan fungsi `PorterStemmer` dari library NLTK.
- Pembuatan Inverted Index: Program mengumpulkan seluruh kata unik menjadi kamus kata (vocabulary) dan menghitung frekuensi kemunculan kata (Term Frequency / TF) pada setiap dokumen.
- Pembobotan TF-IDF: Nilai bobot dihitung berdasarkan rumus TF dikali IDF.
- Perangkingan (Cosine Similarity) : Tingkat kemiripan antara vektor query dan vektor dokumen diukur menggunakan rumus Cosine Similarity. Hasil perhitungan kemiripan kemudian diurutkan dari nilai terbesar ke terkecil menggunakan algoritma sorting manual (Bubble Sort).

3. Contoh Hasil Keluaran Program
Setiap kali dijalankan, program akan memproses teks esai dan memperbarui 3 file output berikut secara otomatis:

A. File `index.txt` (Inverted Index)
Menampilkan kata unik hasil stemming yang diikuti dengan posisi nomor dokumen dan frekuensinya. Contoh:
absolut: 1,1
achiev: 1,1 2,1
across: 5,1
activ: 5,1
adapt: 5,1
admiss: 2,1
advantag: 1,1
aerodynam: 2,1
afternoon: 1,1
allow: 3,1
alreadi: 2,1
also: 1,1
amount: 5,1
antonelli: 1,5
around: 1,1
attack: 1,1
autodrom: 1,1
avail: 1,1
avoid: 2,1
barrier: 3,1 5,1
battl: 3,1 4,1 5,1
becom: 1,1
begin: 3,1
behind: 4,1
bold: 3,1
boost: 2,1
brake: 3,1

B. File weights.txt (Bobot TF-IDF)
Menampilkan daftar kata unik beserta nilai bobot desimalnya untuk masing-masing dokumen secara mendetail. Contoh:
doc1.txt: antonelli, 0.5841 norri, 0.2795 victor, 0.3979
doc2.txt: mclaren, 0.5396 norri, 0.3636

C. File response.txt (Hasil Perangkingan)
Baris pertama menunjukkan jumlah dokumen dengan nilai kemiripan > 0.001. Baris berikutnya berisi nama file dokumen dan nilai skor kemiripannya terhadap query pencarian yang sudah terurut dari yang paling relevan. Contoh:
3
doc1.txt 0.2769
doc4.txt 0.0580
doc2.txt 0.0412
