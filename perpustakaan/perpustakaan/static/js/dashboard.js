function animasiCounter(element, target, durasi = 1000) {
    let start = 0;
    const step = target / (durasi / 16);
    const timer = setInterval(() => {
        start += step;
        if (start >= target) {
            element.textContent = target.toLocaleString('id-ID');
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start).toLocaleString('id-ID');
        }
    }, 16);
}

document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelectorAll('.sc-num').forEach(el => {
        const angka = parseInt(el.textContent.replace(/\D/g, ''));
        if (!isNaN(angka)) animasiCounter(el, angka);
    });

    if (typeof dataTren !== 'undefined' && typeof labelTren !== 'undefined') {
        const barsContainer = document.getElementById('chartBarsContainer');
        const labelsContainer = document.getElementById('chartLabelsContainer');
        
        if (barsContainer && labelsContainer) {
            barsContainer.innerHTML = '';
            labelsContainer.innerHTML = '';

            const maxData = Math.max(...dataTren);
            const batasTinggi = maxData === 0 ? 1 : maxData;

            dataTren.forEach((nilai, index) => {
                const tanggal = labelTren[index];
                const tinggiPersen = (nilai / batasTinggi) * 100;

                const barEl = document.createElement('div');
                barEl.className = 'bar grafik-bar';
                
                if (index === dataTren.length - 1) {
                    barEl.classList.add('active');
                }

                // Logika baru: Fix 35px jika data sedikit agar ukurannya pas di tengah
                const lebarBalok = dataTren.length > 7 ? `${85 / dataTren.length}%` : '35px';
                
                barEl.style.width = lebarBalok;
                barEl.style.height = '0%'; 
                barEl.style.transition = 'height 1s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                barEl.title = `${nilai} Buku Dipinjam pada ${tanggal}`;

                barsContainer.appendChild(barEl);

                const labelEl = document.createElement('span');
                labelEl.textContent = tanggal;
                
                // Tambahan baru: Samakan lebar label dengan balok dan posisikan teks di tengah
                labelEl.style.width = lebarBalok;
                labelEl.style.textAlign = 'center';
                labelsContainer.appendChild(labelEl);

                setTimeout(() => {
                    barEl.style.height = `${tinggiPersen}%`;
                }, 100 * index);
            });
        }
    } else {
        console.error("Variabel dataTren atau labelTren tidak terbaca oleh Javascript.");
    }
});