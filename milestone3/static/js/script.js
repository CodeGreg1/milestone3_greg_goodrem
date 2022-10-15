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

// FULLNAME.addEventListener('change',function(e){
//   let opttext=FULLNAME.options[FULLNAME.options.selectedIndex].text;
//   console.log(opttext);
//   treatment_client.value = opttext
  
// });
// document.querySelector("#full_name_input")

// #full_name_input
// /html/body/div[1]/div/div/div/div[2]/div/div/form/div/fieldset[1]/div[1]/div[2]/input

//*[@id="full_name_input"]

// const CONFIRM_BUTTON = document.querySelector(".confirm-button-enter-done")
// const user_fullname = document.querySelector("#user_fullname")
// const user_email = document.querySelector("#user_email")
// const full_name_input = document.querySelector("#full_name_input")
// const email_input = document.querySelector("#email_input")

// const BUTTON = document.getElementsByTagName("button")

// document.getElementById("full_name_input").onload = function(){ 
//     full_name_input.value = user_fullname.textContent;
// }

// CONFIRM_BUTTON.addEventListener("onmousemove", ()=> {
//     console.log("confirm button pressed")
//     email_input.value = user_email.textContent
// })

// const USERCOPY = document.getElementById("treatment_usr")

// USERCOPY.addEventListener('change',function(e){
//   let opttext=USERCOPY.options[USERCOPY.options.selectedIndex].text;
//   console.log(opttext);
//   treatment_usr.value = opttext
// });