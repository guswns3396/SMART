// function to validate input
// and confirm submission
document.querySelector("#submit-form").onsubmit = function(event) {
    // stop submission to double check
    event.preventDefault();

    // make sure primary question has been answered
    let radios = document.getElementsByName("prim_q");
    let isValid = false;
    let i = 0;
    while (!isValid && i < radios.length) {
        if (radios[i].checked) isValid = true;
        i++;
    }

    // continue to submit if valid
    if (isValid) {
        if (confirm('Submit?')) {
            document.querySelector("#submit-form").submit();
        }
    }
    else {
        alert('Please answer the primary question');
    }
}