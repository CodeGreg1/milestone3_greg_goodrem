document.addEventListener("DOMContentLoaded", function() {
    // sidenav initialization
    let sidenav = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sidenav);
    // datepicker initialization
    let datepicker = document.querySelectorAll(".datepicker");
    M.Datepicker.init(datepicker, {
        format: "dd mmmm, yyyy",
        i18n: {done: "Select"}
    });
    // select initialization
    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);
    // collapsible initializataion
    let collapsibles = document.querySelectorAll(".collapsible");
    M.Collapsible.init(collapsibles);
});

const btn = document.getElementById('buttonsm');

function sendReset() {
  btn.value = 'Send Email';
}

document.getElementById('form').addEventListener('submit', function(event) {
   event.preventDefault();

   btn.value = 'Sending...';

   const serviceID = 'default_service';
   const templateID = 'template_2tqnun4';

   emailjs.sendForm(serviceID, templateID, this)
    .then(() => {
      btn.value = 'Sent!'
      setTimeout(sendReset, 5000)
    }, (err) => {
      btn.value = 'Send Email';
      alert(JSON.stringify(err));
    });
});

// const gmap_canvas = document.getElementById('gmap_canvas')
// gmap_canvas.addEventListener('touchstart', onTouchStart, {passive: true});