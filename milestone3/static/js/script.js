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

const COGS = document.querySelectorAll('.fa-cog')
const BOTTOM_CARD = document.querySelectorAll('.card-action.cog')


COGS.forEach((cog)=>{
    cog.addEventListener('click', function() {
        console.log('Cog clicked')
        BOTTOM_CARD.forEach((bot)=>{
            bot.classList.toggle('vis')})})})
        //   May need to be in own script page
const FULLNAME = document.getElementById("fullname")

FULLNAME.addEventListener('change',function(e){
  let opttext=FULLNAME.options[FULLNAME.options.selectedIndex].text;
  console.log(opttext);
  treatment_client.value = opttext
  
});

// const USERCOPY = document.getElementById("treatment_usr")

// USERCOPY.addEventListener('change',function(e){
//   let opttext=USERCOPY.options[USERCOPY.options.selectedIndex].text;
//   console.log(opttext);
//   treatment_usr.value = opttext
// });