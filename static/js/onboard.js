var dropdownTitle = document.getElementById('dropdownMenuButton');
var items = document.getElementsByClassName('dropdown-item');

var n = document.getElementById('n');
var numbers = document.getElementById('numbers');

var nHtml = n.innerHTML;
var numbersHtml = numbers.innerHTML;

function showN() {
    n.innerHTML = nHtml;
    n.style.visibility = 'visible';
}

function showNumbers() {
    numbers.innerHTML = numbersHtml;
    numbers.style.visibility = 'visible';
}

function hideN() {
    n.innerHTML = '';
    n.style.visibility = 'hidden';
}

function hideNumbers() {
    numbers.innerHTML = '';
    numbers.style.visibility = 'hidden';
}

hideN();
hideNumbers();

for (var i = 0; i < items.length; i++) {
    items[i].addEventListener('click', function (e) {
        dropdownTitle.innerHTML = e.target.innerHTML;

        hideN();
        hideNumbers();

        if (dropdownTitle.innerHTML === 'Send me <i>N</i> verification codes') {
            showN();
        } else if (dropdownTitle.innerHTML === 'Team-based authentication') {
            showNumbers();
        }
    }, false);
}