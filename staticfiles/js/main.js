let marbtn = document.getElementById("Marketing");
console.log(marbtn)
let opbtn = document.getElementById("Operations");
console.log(opbtn)
let sabtn = document.getElementById("Sales");
console.log(sabtn)
let mangbtn = document.getElementById("Management/Admin");
console.log(mangbtn)
let itbtn = document.getElementById("IT");
console.log(itbtn)

let depart = document.getElementById("department")
// console.log(depart.value = marbtn.value) 

cate = document.querySelector(".category")
form = document.querySelector(".wrapper")


marbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = marbtn.value
    form.classList.remove('wrapper-visibility')

})

opbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = opbtn.value
    form.classList.remove('wrapper-visibility')

})

sabtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = sabtn.value
    form.classList.remove('wrapper-visibility')

})

mangbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = mangbtn.value
    form.classList.remove('wrapper-visibility')

})

itbtn.addEventListener('click', () => {
    cate.classList.add('category-visibilty');
    depart.value = itbtn.value
    form.classList.remove('wrapper-visibility')

})


let counter = 0;

function startCounter() {
    setInterval(() => {
        counter++;
        updatePopupContent(counter);
    }, 1000);  // Update every second (1000 milliseconds)
}

function updatePopupContent(value) {
    // Update the popup content with the counter value
    document.getElementById('counter-popup').innerText = value;
}