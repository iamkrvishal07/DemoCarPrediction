document.addEventListener('DOMContentLoaded', function() {
    const companySelect = document.getElementById('company');
    const carModelSelect = document.getElementById('car_model');

    function updateCarModels() {
        const selectedCompany = companySelect.value;
        
        // Clear existing options
        carModelSelect.innerHTML = '';

        if (selectedCompany && selectedCompany !== 'Select Company') {
            fetch('/get_car_models', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ company: selectedCompany })
            })
            .then(response => response.json())
            .then(data => {
                if (data.models.length > 0) {
                    data.models.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model;
                        option.textContent = model;
                        carModelSelect.appendChild(option);
                    });
                } else {
                    carModelSelect.innerHTML = '<option value="">No models available</option>';
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            carModelSelect.innerHTML = '<option value="">Select a company first</option>';
        }
    }

    companySelect.addEventListener('change', updateCarModels);

    document.getElementById('predictionForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const company = companySelect.value;
        const car_model = carModelSelect.value;
        const year = document.getElementById('year').value;
        const fuel_type = document.getElementById('fuel_type').value;
        const kilo_driven = document.getElementById('kilo_driven').value;

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                company: company,
                car_model: car_model,
                year: year,
                fuel_type: fuel_type,
                kilo_driven: kilo_driven
            })
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('predictionResult');
            if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>Predicted Price: ₹${data.prediction}</p>`;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
