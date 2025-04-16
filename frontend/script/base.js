async function fetchImages() {
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = '';

    try {
        const res = await fetch('http://localhost:5001/all-images');
        const data = await res.json();

        if (data.images && data.images.length > 0) {
            data.images.forEach(image => {
                const col = document.createElement('div');
                col.className = 'col-sm-6 col-md-4 col-lg-3';

                col.innerHTML = `
            <div class="card shadow-sm h-100">
              <img src="http://localhost:5001/static/${encodeURIComponent(image)}" class="card-img-top preview-image" alt="${image}">
              <div class="card-body">
                <p class="card-text text-center">${image.replace(/\.[^/.]+$/, "")}</p>
              </div>
            </div>
          `;

                gallery.appendChild(col);
            });
        } else {
            gallery.innerHTML = `<div class="alert alert-warning">Фото не найдены.</div>`;
        }
    } catch (error) {
        gallery.innerHTML = `<div class="alert alert-danger">Ошибка загрузки изображений: ${error.message}</div>`;
    }
}

function addPhoto() {
    const modal = new bootstrap.Modal(document.getElementById('addPhotoModal'));
    document.getElementById('addPhotoForm').reset();
    document.getElementById('addPhotoAlert').classList.add('d-none');
    document.getElementById('addPhotoSpinner').classList.add('d-none');
    modal.show();
}

document.getElementById('addPhotoForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nameInput = document.getElementById('personName');
    const imageInput = document.getElementById('personImage');
    const alertBox = document.getElementById('addPhotoAlert');
    const spinner = document.getElementById('addPhotoSpinner');

    const name = nameInput.value.trim();
    const file = imageInput.files[0];

    if (!name || !file) {
        alertBox.textContent = "Укажите имя и выберите изображение.";
        alertBox.classList.remove('d-none');
        return;
    }

    const renamedFile = new File(
        [file],
        `${name}${file.name.slice(file.name.lastIndexOf('.'))}`,
        { type: file.type }
    );

    const formData = new FormData();
    formData.append('image', renamedFile);

    spinner.classList.remove('d-none');
    alertBox.classList.add('d-none');

    try {
        const res = await fetch('http://localhost:5001/add-image', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        spinner.classList.add('d-none');

        if (data.message) {
            bootstrap.Modal.getInstance(document.getElementById('addPhotoModal')).hide();
            fetchImages();
        } else {
            alertBox.textContent = data.error || "Не удалось загрузить фото.";
            alertBox.classList.remove('d-none');
        }
    } catch (err) {
        spinner.classList.add('d-none');
        alertBox.textContent = "Ошибка: " + err.message;
        alertBox.classList.remove('d-none');
    }
});

fetchImages();