// get modal element
var modal = document.getElementById('my_modal');
//get open modal button
var modalBtn = document.getElementById('modalBtn');

// get close button
var closeBtn = document.getElementsByClassName('closeBtn') [0];

//listen for a click (open)
modalBtn.addEventListener('click', openModal);

//listen for close click
closeBtn.addEventListener('click', closeModal);

//function to open modal
function openModal (){
    modal.style.display ='block';
}

//function to close modal
function closeModal (){
    modal.style.display ='none';
    document.location.reload();
}