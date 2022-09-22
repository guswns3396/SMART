// function to validate input
// and confirm submission
document.querySelector("#submit-form").onsubmit = function(event) {
    // stop submission to double check
    event.preventDefault();

    // TODO: validate input

    if (confirm('Submit?')) {
        document.querySelector("#submit-form").submit();
    }
}