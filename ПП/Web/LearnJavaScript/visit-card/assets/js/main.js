let button;
let organization_input;
let name_input;
let position_input;
let address_input;
let email_input;
let telephone_input;
let organization_text;
let name_text;
let position_text;
let email_text;
let telephone_text;
let address_text;

function apply_pressed(){
    organization_text.innerText = organization_input.value;
    name_text.innerText = name_input.value;
    position_text.innerText = position_input.value;
    email_text.innerText = email_input.value;
    telephone_text.innerText = telephone_input.value;
    address_text.innerText = address_input.value;
}

function init() {
    button = document.getElementById('apply');
    organization_input = document.getElementById('organization');
    name_input = document.getElementById('name');
    position_input = document.getElementById('position');
    email_input = document.getElementById('email');
    telephone_input = document.getElementById('telephone');
    address_input = document.getElementById('address')
    organization_text = document.getElementById('organization_text');
    name_text = document.getElementById('name_text');
    address_text = document.getElementById('address_text');
    telephone_text = document.getElementById('telephone_text');
    email_text = document.getElementById('email_text')
    position_text = document.getElementById('position_text');('name_text');
    button.addEventListener('click', apply_pressed);
    apply_pressed();
}

document.addEventListener('DOMContentLoaded', init);