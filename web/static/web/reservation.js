document.addEventListener("DOMContentLoaded", function (e) {

    // eventListener for Map Links
    const map_links = document.querySelectorAll(".link-to-map");

    for (let i = 0; i < map_links.length; i++) {
        map_links[i].addEventListener("click", goToMap);
    }

    // eventListener for home link
    document.querySelector(".link-home").addEventListener("click", function (e) {
        window.location.href = "/";
    })
});
function goToMap (e) {
    try {
        const longitude = e.target.dataset.longitude;
        const latitude = e.target.dataset.latitude;

        window.open(`https:maps.google.com/?q=${longitude},${latitude}`, "_blank");
    } catch (err) {
        console.log("Js error! ", err);
    }
}