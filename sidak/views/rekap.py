from django.shortcuts import render
from sidak.models import Siswa, Presensi
from calendar import monthrange
from datetime import date


def generate_pdf(request, kelas, tanggal):
    tahun = int(tanggal.split('-')[2])
    bulan = int(tanggal.split('-')[1])

    _, jumlah_hari = monthrange(tahun, bulan)

    datas = []
    data_siswa = Siswa.objects.filter(kelas__nama_kelas=kelas).all()

    total_hadir = 0
    total_sakit = 0
    total_izin = 0
    total_absen = 0

    for siswa in data_siswa:
        tmp = []
        tmp.append(siswa.nama)
        sakit = 0
        izin = 0
        hadir = 0
        absen = 0
        for tanggal in range(1, jumlah_hari+1):
            status = ' '

            prenesi_query = Presensi.objects \
                .filter(no_induk=siswa.no_induk) \
                .filter(tanggal=date(tahun, bulan, tanggal)) \
            
            if prenesi_query.count() != 0:
                status = prenesi_query.first().status
                if status == 'HADIR':
                    status = 'H'
                    hadir += 1
                elif status == 'IZIN':
                    status = 'I'
                    izin += 1
                elif status == 'SAKIT':
                    status = 'S'
                    sakit += 1
                else:
                    print('ABSENN')
                    status = 'A'
                    absen += 1
            
            tmp.append(status)
        
        tmp.append(hadir)
        tmp.append(izin)
        tmp.append(sakit)
        tmp.append(absen)

        total_hadir += hadir
        total_absen += absen
        total_sakit += sakit
        total_izin += izin
        
        datas.append(tmp)

    return render(request, 'report.html', {
        'data': datas,
        'tanggal': str(tanggal)+'-'+str(bulan)+'-'+str(tahun),
        'kelas': kelas,
        'range': range(1, len(datas[0])-4),
        'len_range': len(datas[0])-4,
        'total_hadir': total_hadir,
        'total_izin': total_izin,
        'total_sakit': total_sakit,
        'total_absen': total_absen
    })

