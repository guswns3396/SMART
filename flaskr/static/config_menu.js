// function to create as many form elements needed for specified
// number of levels
document.querySelector("#numlvls").onchange = function() {
    let numlvls = document.querySelector("#numlvls").value;

    // TODO: verify numlvls is valid

    let form = document.querySelector("#param-form");
    // remove previously added scenarios
    let elements = document.getElementsByClassName('scn');
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
    // add scenarios
    for (let i = 0; i < numlvls; i++) {
        // template
        let template = `
                <legend>
                    <h3>Level ${i+1}</h3>
                </legend>
                <div class="row">
                    <label class="col-6">Scenario 1</label>
                    <label class="col-6">Scenario 2</label>
                </div>
                <div class="row">
                    <input class="col-6" type="text-area" name="scn-a">
                    <input class="col-6" type="text-area" name="scn-b">
                </div><br>
        `;
        // create node & fill it with template
        const newNode = document.createElement('div');
        newNode.setAttribute('class', 'scn');
        newNode.innerHTML = template;
        // insert node to the form
        form.insertBefore(newNode, form.lastElementChild);
    }
}

// function to validate input
// and confirm submission
document.querySelector("#param-form").onsubmit = function(event) {
    // stop submission to double check
    event.preventDefault();

    // TODO: validate input

    if (confirm('Submit?')) {
        document.querySelector("#param-form").submit();
    }
}