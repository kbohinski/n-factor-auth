var div = document.getElementById('drive');
var check = document.getElementById('driver-0');

var questions = div.innerHTML;
div.innerHTML = '';

check.addEventListener('change', function (e) {
    if (check.checked) {
        div.innerHTML = questions;
        div.style.visibility = 'visible';
    } else {
        div.innerHTML = '';
        div.style.visibility = 'hidden';
    }
});
