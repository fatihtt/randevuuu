let my_token;
let allowable_dates = ["2023-05-13", "2023-05-14", "2023-05-15"];
document.addEventListener("DOMContentLoaded", function () {
    writeDate(allowable_dates[0]);
    // eventListeners active service selection event
    document.querySelector("#select-active-services").addEventListener("change", function (e) {
        // take time_range
    });
});
function writeDate (date) {
    const options = { weekday: 'long', month: 'long', day: 'numeric' };
    document.querySelector(".date-selection-date").innerHTML= (new Date(date)).toLocaleDateString("en-EN", options);
}