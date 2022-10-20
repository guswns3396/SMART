// function to validate number of levels
function validNumlvls() {
    let numlvls = document.querySelector("#numlvls").value;

    // check if null
    if (!numlvls) {
        return false;
    }

    // convert string to number
    numlvls = Number(numlvls);

    // check if positive integer
    let isInt = parseInt(numlvls) == numlvls && !isNaN(parseInt(numlvls, 10));
    let isPos = numlvls > 0;

    return isInt && isPos;
}

// function to validate p
function validP() {
    // get p
    let p = document.querySelector("#prob").value;
    // check if p is null
    if (!p) {
        return false;
    }
    p = Number(p);
    // check p
    return p >= 0 && p <= 1;
}

// function to error check numlvls on change
// and create as many form elements needed
document.querySelector("#numlvls").onchange = function() {

    // see if valid
    let isValid = validNumlvls();

    if (!isValid) {
        // clear value
        document.querySelector("#numlvls").value = "";
        // display hidden
        document.querySelector("#numlvl-error").style.visibility = "visible";
        // remove previously added scenarios
        let elements = document.getElementsByClassName('scn');
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }
    }
    else {
        // hide error
        document.querySelector("#numlvl-error").style.visibility = "hidden";
        // get form
        let form = document.querySelector("#param-form");
        // remove previously added scenarios
        let elements = document.getElementsByClassName('scn');
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }
        // add scenarios
        let numlvls = Number(document.querySelector("#numlvls").value);
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
}

// function to error check p on change
document.querySelector("#prob").onchange = function() {
    // see if valid
    let isValid = validP();

    if (isValid) {
        // hide error
        document.querySelector("#p-error").style.visibility = "hidden";
    }
    else {
        // show error
        document.querySelector("#p-error").style.visibility = "visible";
        // clear p
        document.querySelector("#prob").value = "";
    }
}

// function to validate input
// and confirm submission
document.querySelector("#param-form").onsubmit = function(event) {
    // stop submission to double check
    event.preventDefault();

    // check numlvls positive integer
    let isPosInt = validNumlvls();
    // check probability is a number between [0,1]
    let isValidP = validP();

    // check all valid
    let isValid = isPosInt && isValidP;

    if (isValid) {
        if (confirm('Submit?')) {
            document.querySelector("#param-form").submit();
        }
    }
    else {
        alert('Please check your inputs');
    }
}