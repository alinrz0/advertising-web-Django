// create_ad.js
document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('images');
    const imagePreview = document.getElementById('image-preview');

    imageInput.addEventListener('change', function(e) {
        const files = imageInput.files;
        const fileList = [];

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const reader = new FileReader();

            reader.onload = function(event) {
                const imageUrl = event.target.result;
                const imageElement = document.createElement('img');
                imageElement.src = imageUrl;
                imageElement.width = 100; // adjust the width as needed
                imageElement.height = 100; // adjust the height as needed
                imagePreview.appendChild(imageElement);
            };

            reader.readAsDataURL(file);
        }
    });
});