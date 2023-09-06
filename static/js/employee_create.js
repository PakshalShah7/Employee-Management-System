// for employee create

let employeeForm = document.querySelectorAll("#employee-form")
let container = document.querySelector("#create_form")
let addButton = document.querySelector("#add_more")
let totalForms = document.querySelector("#id_employees-TOTAL_FORMS")

let formNum = employeeForm.length-1
let formRegex = RegExp(`employees-(\\d){1}-`,'g')

addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let newForm = employeeForm[0].cloneNode(true)

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `employees-${formNum}-`)
    container.insertBefore(newForm, addButton)
    totalForms.setAttribute('value', `${formNum+1}`)

    console.log(formNum)
}
