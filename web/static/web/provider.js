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