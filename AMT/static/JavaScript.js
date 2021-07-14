$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

//For default relations
function selectRadio(radioBoxID, relation) {
    const textBox = document.getElementById("relation");
    if (radioBoxID == "customRadio"){
      textBox.value = "";
      textBox.readOnly = false;              
      }
    else{
      textBox.value = relation;
      textBox.readOnly = true; 
    }
  }

function copyToClipboard(id) {
    /* Get the text field */
    var copyText = document.getElementById(id);
  
    /* Select the text field */
    copyText.select(); 
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
  
    /* Alert the copied text */
    alert("Copied ID: " + copyText.value + " to clipboard");
  }


var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})




