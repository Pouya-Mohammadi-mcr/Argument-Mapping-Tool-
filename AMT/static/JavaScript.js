//Activate Bootstrap's tooltip
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
  
    /* Show the copied text */
    msg="Copied ID: " + copyText.value + " to clipboard";
    tempAlert(msg,600)
  }
  
//Show copy ID message and hide it after some time
function tempAlert(msg,duration)
{
 var el = document.createElement("h3");
 el.setAttribute("style","position:absolute;top:10%;left:1%;background-color:#DB7A93;border: 1px solid #376E70;border-radius: 5px 5px;");
 el.innerHTML = msg;
 setTimeout(function(){
  el.parentNode.removeChild(el);
 },duration);
 document.body.appendChild(el);
}

//Modal
var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})

