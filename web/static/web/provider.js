let my_token;
document.addEventListener("DOMContentLoaded", function() {

    // eventListeners for rating stars
    starIcons = document.querySelectorAll(".span-rating-icon");
    starIconParent = document.querySelector(".div-rate-stars");
    if (starIconParent) starIconParent.addEventListener("mouseout", function (e) {
        p_starIcons = e.target.querySelectorAll(".span-rating-icon");
        for (let k = 0; k < p_starIcons.length; k++) {
            p_starIcons[k].innerText = "star_outline";
        }
    })
    for (let i = 0; i < starIcons.length; i++) {
        starIcons[i].addEventListener("mouseover", showRating);
        starIcons[i].addEventListener("click", giveRating);
    }

    my_token = getCookie('csrftoken');

    // subscription eventListener

    const subsButton = document.querySelector(".button-subs");

    if (subsButton) {
        subsButton.addEventListener("click", function (e) {
            subscribe(e.target.dataset.id);
        })
    }
});
function showRating (e) {
    const starIndex = Array.from(e.target.parentElement.children).indexOf(e.target);

    for (let i = 0; i < 5; i++) {
        if (i < starIndex + 1) e.target.parentElement.children[i].innerText = "star";
        else e.target.parentElement.children[i].innerText = "star_outline";
    }
}
function giveRating (e) {
    console.log("give rating")
}
function subscribe (providerId) {
    try {
        if (!providerId) throw "Could not detect provider."

        let fetchStatus = null;
        fetch("/subscribe", {
            method: "POST",
            headers: {'X-CSRFToken': my_token},
            mode: 'same-origin',
            body: JSON.stringify({
                provider_id: parseInt(providerId)
            })
        }).then(response => {
            fetchStatus = response.status;
            return response.json();
        }).then(result => {
            if (fetchStatus != 201) {
                throw result.message
            }
            else {
                // subscription succeeeded
                console.log("fetch succeeded");
                console.log("result: ", result.data);
                window.location.href = "";
            }
        }).catch(err => {
            console.log(err);
            gMessage("alert", `Error: ${err}`);
        })

    }
    catch (err) {
        console.log(err);
        gMessage("alert", `Error: ${err}`);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}