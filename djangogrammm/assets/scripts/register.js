import '../styles/styles.scss'
import $ from 'jquery';

window.addEventListener('DOMContentLoaded', (event) => {
    const imgInp = document.getElementById('avatar');
    const previewImg = document.getElementById('blah');

    imgInp.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                previewImg.style.width = '300px';
                previewImg.style.height = '300px';
                previewImg.style.border = '2px solid #ccc';
                previewImg.style.padding = '5px';
            }
            reader.readAsDataURL(file);
        }
    });
});
