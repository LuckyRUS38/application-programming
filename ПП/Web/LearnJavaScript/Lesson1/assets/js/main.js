let square;

function square_clicked(){
    square.style.background = 'red';
}

function init(){
    square = document.getElementById('div1'); // По ID
    // square = document.getElementsByClassName('container'); // По классу
    square.addEventListener('click', square_clicked);
}
document.addEventListener('DOMContentLoaded', init);