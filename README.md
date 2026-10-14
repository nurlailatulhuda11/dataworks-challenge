\# DataWorks Challenge - Reservoir Production Forecasting



Ramalan pengeluaran kumulatif minyak, gas dan air bagi kes-kes reservoir.



\## Persediaan



1\. Pasang Python 3.10+ dan kebergantungan:

&#x20;  `py -m pip install -r requirements.txt`

2\. Letakkan fail asal penganjur dalam `data/reservoir\_cases/`:

&#x20;  - `02 Field Production.xlsx`

&#x20;  - `03 Train Cases 1.xlsx` hingga `08 Test Cases.xlsx`

3\. Letakkan `09 Template Deliverable.xlsx` di akar projek.



Fail data tidak disertakan dalam repository kerana saiznya besar (160-330 MB setiap fail).



\## Urutan menjalankan skrip



Jalankan semua dari akar projek.



1\. `py make\_production\_history.py` : sejarah pengeluaran medan -> `data/production\_history.csv`

2\. `py make\_case\_targets.py` : sasaran pengeluaran 100 kes -> `data/\*.csv`

3\. `py build\_quarterly.py` : ubah kepada siri suku tahunan seragam -> `data/quarterly\_\*.csv`

4\. `py build\_features.py` : ringkasan ciri reservoir setiap kes -> `data/case\_features.csv` (30-60 minit)

5\. `py train\_model.py` : latih dan nilai model Ridge

6\.  py forecast\_template.py:amalan 2008-2028 untuk Case 1-10 (kaedah trend setiap fasa), menghasilkan `outputs/Deliverable\_filled.xlsx`

py forecast\_template\_v2.py : ramalan versi 2 (jumlah cecair dan water cut), menghasilkan outputs/Deliverable\_filled\_v2.xlsx.

7\. `py predict\_test\_cases.py` : ramalan validasi dan ujian, menghasilkan `outputs/validation\_predictions.csv` dan `outputs/test\_predictions.csv`

8\. `py build\_powerbi\_data.py` : data untuk Power BI -> folder `powerbi/`



\## Kaedah



\- Pecahan data mengikut kes: latihan 1-70, validasi 71-85, ujian 86-100.

\- Hanya 5 ciri berubah antara kes; `oil\_in\_place`, `porv\_sum` dan `PERMX\_mean` digunakan.

\- Satu model Ridge bagi setiap tarikh suku tahunan, dilatih dengan kes 1-70 sahaja.

\- Ramalan 2008-2028: ekstrapolasi trend eksponen kadar pengeluaran 8 suku tahun terakhir bagi setiap kes dan fasa, kemudian kumulatif dikira daripada kamiran kadar.



\## Keputusan



Ralat peratus pada 2008-01-01 (kumulatif):



| Sasaran | Validasi | Ujian |

|---|---|---|

| Gas | 0.93% | 1.10% |

| Minyak | 0.93% | 1.11% |

| Air | 0.98% | 1.26% |



Backtest ramalan trend (data dipotong 2006-01-01, ramal 8 suku tahun): ralat median \~1.0% (gas, minyak), \~0.3% (air).



\## Andaian dan had



\- Ramalan 2008-2028 ialah ekstrapolasi trend 8 suku tahun terakhir, bukan simulasi reservoir. Backtest hanya menguji 2 tahun ke hadapan, jadi ketepatan untuk 20 tahun lebih rendah.

\- Fasa air diramal secara berasingan daripada minyak, jadi water cut hujung tempoh mungkin terlalu tinggi.

\-Air diramal melalui jumlah cecair dan water cut (dihadkan 99%). Backtest 2 tahun: ralat median v2 sedikit lebih tinggi (gas/minyak \~1.3%, air \~0.9%) berbanding kaedah lama (\~1.0% dan 0.3%), tetapi v2 dipilih kerana lebih munasabah secara fizikal untuk 20 tahun, yang tidak dapat disahkan.

\- Ralat model Ridge diukur pada hujung sejarah (2008-01-01), bukan pada tempoh ramalan.

