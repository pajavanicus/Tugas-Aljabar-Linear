import sys
import os
import math
import string
import nltk

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def preprocess(teks):
    teks = teks.lower()
    
    kata_kata = word_tokenize(teks)
    
    kata_bersih = []
    for kata in kata_kata:
        if kata not in string.punctuation:
            if kata != 'and' and kata != 'or' and kata != 'not':
                kata_bersih.append(kata)
                
    daftar_stopword = stopwords.words('english')
    kata_tanpa_stopword = []
    for kata in kata_bersih:
        if kata not in daftar_stopword:
            kata_tanpa_stopword.append(kata)
            
    stemmer = PorterStemmer()
    kata_hasil = []
    for kata in kata_tanpa_stopword:
        kata_dasar = stemmer.stem(kata)
        kata_hasil.append(kata_dasar)
        
    return kata_hasil

def ambil_nilai_kemiripan(item):
    return item[1]

def main():
    if len(sys.argv) < 3:
        print("Cara pakai: python vsm.py base.txt query.txt")
        return

    file_base = sys.argv[1]
    file_query = sys.argv[2]

    if os.path.exists(file_base) == False or os.path.exists(file_query) == False:
        print("Error: File base.txt atau query.txt tidak ada!")
        return

    daftar_dokumen = []
    buka_base = open(file_base, 'r')
    for baris in buka_base:
        nama_file = baris.strip()
        if nama_file != "":
            daftar_dokumen.append(nama_file)
    buka_base.close()

    koleksi_teks = {}
    for nama_file in daftar_dokumen:
        if os.path.exists(nama_file) == True:
            buka_dokumen = open(nama_file, 'r')
            koleksi_teks[nama_file] = buka_dokumen.read()
            buka_dokumen.close()

    buka_query = open(file_query, 'r')
    teks_query = buka_query.read()
    buka_query.close()

    jumlah_semua_dokumen = len(koleksi_teks)
    frekuensi_kata_dokumen = {}
    dokumen_freq = {}
    kamus_kata = []

    for nama_dok in koleksi_teks:
        isi_teks = koleksi_teks[nama_dok]
        kata_kata = preprocess(isi_teks)
        
        frekuensi = {}
        for kata in kata_kata:
            if kata in frekuensi:
                frekuensi[kata] = frekuensi[kata] + 1
            else:
                frekuensi[kata] = 1
                
            if kata not in kamus_kata:
                kamus_kata.append(kata)
                
        frekuensi_kata_dokumen[nama_dok] = frekuensi
        
        for kata in frekuensi:
            if kata in dokumen_freq:
                dokumen_freq[kata] = dokumen_freq[kata] + 1
            else:
                dokumen_freq[kata] = 1

    kamus_kata.sort()
    bobot_dokumen = {}
    
    for nama_dok in frekuensi_kata_dokumen:
        frekuensi = frekuensi_kata_dokumen[nama_dok]
        bobot_dokumen[nama_dok] = {}
        
        for kata in kamus_kata:
            if kata in frekuensi:
                freq = frekuensi[kata]
            else:
                freq = 0
                
            if freq > 0:
                tf = 1 + math.log10(freq)
            else:
                tf = 0
                
            if kata in dokumen_freq:
                df = dokumen_freq[kata]
            else:
                df = 0
                
            if df > 0:
                idf = math.log10(jumlah_semua_dokumen / df)
            else:
                idf = 0
                
            bobot = tf * idf
            if bobot > 0:
                bobot_dokumen[nama_dok][kata] = bobot

    file_index = open('index.txt', 'w')
    for kata in kamus_kata:
        tulisan_baris = kata + ":"
        ada_isi = False
        
        nomor_dokumen = 1
        for nama_dok in daftar_dokumen:
            if nama_dok in frekuensi_kata_dokumen:
                frekuensi = frekuensi_kata_dokumen[nama_dok]
                if kata in frekuensi:
                    freq = frekuensi[kata]
                    if freq > 0:
                        tulisan_baris = tulisan_baris + " " + str(nomor_dokumen) + "," + str(freq)
                        ada_isi = True
            nomor_dokumen = nomor_dokumen + 1
            
        if ada_isi == True:
            file_index.write(tulisan_baris + "\n")
    file_index.close()

    file_weights = open('weights.txt', 'w')
    for nama_dok in daftar_dokumen:
        tulisan_baris = nama_dok + ":"
        if nama_dok in bobot_dokumen:
            for kata in bobot_dokumen[nama_dok]:
                nilai_bobot = bobot_dokumen[nama_dok][kata]
                tulisan_baris = tulisan_baris + " " + kata + ", " + "{:.4f}".format(nilai_bobot)
        file_weights.write(tulisan_baris + "\n")
    file_weights.close()

    kata_query = preprocess(teks_query)
    frekuensi_query = {}
    for kata in kata_query:
        if kata in frekuensi_query:
            frekuensi_query[kata] = frekuensi_query[kata] + 1
        else:
            frekuensi_query[kata] = 1

    bobot_query = {}
    for kata in kamus_kata:
        if kata in frekuensi_query:
            freq = frekuensi_query[kata]
        else:
            freq = 0
            
        if freq > 0:
            tf = 1 + math.log10(freq)
        else:
            tf = 0
            
        if kata in dokumen_freq:
            df = dokumen_freq[kata]
        else:
            df = 0
            
        if df > 0:
            idf = math.log10(jumlah_semua_dokumen / df)
        else:
            idf = 0
            
        bobot = tf * idf
        if bobot > 0:
            bobot_query[kata] = bobot

    hasil_ranking = []
    
    panjang_query = 0
    for kata in bobot_query:
        panjang_query = panjang_query + (bobot_query[kata] * bobot_query[kata])
    panjang_query = math.sqrt(panjang_query)

    for nama_dok in daftar_dokumen:
        if nama_dok not in bobot_dokumen:
            continue
            
        panjang_dokumen = 0
        for kata in bobot_dokumen[nama_dok]:
            panjang_dokumen = panjang_dokumen + (bobot_dokumen[nama_dok][kata] * bobot_dokumen[nama_dok][kata])
        panjang_dokumen = math.sqrt(panjang_dokumen)
        
        dot_product = 0
        for kata in kamus_kata:
            if kata in bobot_dokumen[nama_dok] and kata in bobot_query:
                dot_product = dot_product + (bobot_dokumen[nama_dok][kata] * bobot_query[kata])
                
        if panjang_query == 0 or panjang_dokumen == 0:
            kemiripan = 0
        else:
            kemiripan = dot_product / (panjang_dokumen * panjang_query)
            
        if kemiripan > 0.001:
            hasil_ranking.append([nama_dok, kemiripan])

    hasil_ranking.sort(key=ambil_nilai_kemiripan, reverse=True)

    file_response = open('response.txt', 'w')
    file_response.write(str(len(hasil_ranking)) + "\n")
    for item in hasil_ranking:
        nama_dok = item[0]
        kemiripan = item[1]
        file_response.write(nama_dok + " " + "{:.4f}".format(kemiripan) + "\n")
    file_response.close()

if __name__ == "__main__":
    main()