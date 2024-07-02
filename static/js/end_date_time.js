document.addEventListener('DOMContentLoaded', (event) => {
    // Элементы формы
    const frequencySelect = document.getElementById('id_frequency');
    const endDateDiv = document.getElementById('div_id_end_date_time');

    // Функция для обновления видимости div end_date_time
    function updateEndDateVisibility() {
        const selectedFrequency = frequencySelect.value;
        endDateDiv.hidden = selectedFrequency === 'однократно';
    }

    frequencySelect.addEventListener('change', updateEndDateVisibility);
    updateEndDateVisibility();
});