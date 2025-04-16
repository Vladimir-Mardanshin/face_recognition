async function uploadImage() {
  const input = document.getElementById('imageInput');
  const spinner = document.getElementById('spinner');
  const result = document.getElementById('result');

  if (!input.files.length) return;

  const formData = new FormData();
  formData.append('image', input.files[0]);

  result.innerHTML = '';
  spinner.style.display = 'block';

  try {
    const res = await fetch('http://localhost:5001/search-image', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    spinner.style.display = 'none';

    const timestamp = Date.now();
    const uploadedFileUrl = `http://localhost:5001/uploads/${input.files[0].name}?t=${timestamp}`;

    if (data.recognized && Array.isArray(data.recognized) && data.recognized.length > 0) {
      // Генерация карточек с результатами
      const cards = data.recognized.map(person => `
        <div class="col-md-4">
          <div class="card h-100 shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">${person.name}</h5>
              <p class="card-text">Совпадение: ${Math.round(person.score * 100)}%</p>
              <img src="http://localhost:5001/static/${person.name}.jpg?t=${timestamp}" class="preview-image rounded" alt="${person.name}">
            </div>
          </div>
        </div>
      `).join('');

      result.innerHTML = `
        <div class="mb-4">
          <h5>Загруженное фото:</h5>
          <img src="${uploadedFileUrl}" class="preview-image rounded" alt="Загруженное изображение">
        </div>
        <div class="mb-3"><h5>Найденные совпадения:</h5></div>
        <div class="row g-4">
          ${cards}
        </div>
      `;
    } else {
      result.innerHTML = `
        <div class="mb-4">
          <h5>Загруженное фото:</h5>
          <img src="${uploadedFileUrl}" class="preview-image rounded" alt="Загруженное изображение">
        </div>
        <div class="alert alert-warning" role="alert">
          Похожих людей не найдено.
        </div>
      `;
    }
  } catch (error) {
    spinner.style.display = 'none';
    result.innerHTML = `
      <div class="alert alert-danger" role="alert">
        Ошибка: ${error.message}
      </div>
    `;
  }
}
