var dropdownTitle = document.getElementById('dropdownMenuButton');
var items = document.getElementsByClassName('dropdown-item');

function showN() {
    n.innerHTML = '<label class="control-label" for="n">n</label><div class="controls"><input id="n" name="n" placeholder="20" class="form-control input-md" required="" type="text"></div>';
    n.style.visibility = 'visible';
}

function showNumbers() {
    numbers.innerHTML = '<label class="control-label" for="numbers">numbers (enter seperated by comma)</label><div class="controls"><input id="numbers" name="numbers" placeholder="ex: \'1234567890,6094753287\'" class="form-control input-md" required="" type="textarea"></div>';
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

var n = document.getElementById('n');
var numbers = document.getElementById('numbers');

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