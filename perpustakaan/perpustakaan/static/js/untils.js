// FORMAT RUPIAH
function formatRupiah(angka) {
    return 'Rp ' + angka.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// KONFIRMASI HAPUS dengan style custom
function konfirmasiHapus(nama) {
    return confirm(`Yakin ingin menghapus "${nama}"?\nAksi ini tidak bisa dibatalkan!`);
}

// AUTO CLOSE alert setelah 3 detik
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });
});