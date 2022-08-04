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
let additional_phone_btn;
let additional_phone;
let additional_phone_shown = false;
let remove_additional_phone_btn;
let telephone_dop_text;
let telephone_dop_input;
let right_align_name_btn;
let left_align_name_btn;
let center_aling_name_btn;

function apply_pressed(){
    organization_text.innerText = organization_input.value;
    name_text.innerText = name_input.value;
    position_text.innerText = position_input.value;
    email_text.innerText = email_input.value;
    telephone_text.innerText = telephone_input.value;
    address_text.innerText = address_input.value;
    telephone_dop_text.innerText = telephone_dop_input.value;
}

function additionalPhoneHandler(){
    if(!additional_phone_shown){
        additional_phone_shown = true;
        additional_phone.classList.remove('hidden');
        telephone_dop_text.classList.remove('hidden');
        additional_phone_btn.classList.add('hidden');
    }
    else{
        additional_phone_shown = false;
        additional_phone.classList.add('hidden');
        telephone_dop_text.classList.add('hidden');
        additional_phone_btn.classList.remove('hidden');
    }
}

function alignNameHandler(action){
    right_align_name_btn.classList.remove('pressed');
    center_aling_name_btn.classList.remove('pressed');
    left_align_name_btn.classList.remove('pressed');

    if (action.target.localName === 'img'){
        action.target.parentElement.classList.add('pressed')
        clas = action.target.parentElement.classList;
    }
    else{
        action.target.classList.add('pressed');
        clas = action.target.classList;
    }
    if (clas.contains('left')){
        name_text.style.textAlign = 'left';
    }
    if (clas.contains('center')){
        name_text.style.textAlign = 'center';
    }
    if (clas.contains('right')){
        name_text.style.textAlign = 'right';
    }
}

function getElements(){
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
    email_text = document.getElementById('email_text');
    position_text = document.getElementById('position_text');
    additional_phone = document.getElementById('additional_phone');
    telephone_dop_input = document.getElementById('telephone_dop');
    additional_phone_btn = document.getElementById('additional_phone_btn');
    telephone_dop_text = document.getElementById('telephone_dop_text');
    remove_additional_phone_btn = document.getElementById('remove_additional_phone_btn');
    right_align_name_btn = document.getElementById('right_align_name_btn');
    left_align_name_btn = document.getElementById('left_align_name_btn');
    center_aling_name_btn = document.getElementById('center_align_name_btn');
}

function init() {
    getElements();
    button.addEventListener('click', apply_pressed);
    additional_phone_btn.addEventListener('click', additionalPhoneHandler);
    remove_additional_phone_btn.addEventListener('click', additionalPhoneHandler);
    right_align_name_btn.addEventListener('click', alignNameHandler);
    center_aling_name_btn.addEventListener('click', alignNameHandler);
    left_align_name_btn.addEventListener('click', alignNameHandler);
    apply_pressed();
}

document.addEventListener('DOMContentLoaded', init);