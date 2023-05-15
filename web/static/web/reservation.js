
document.addEventListener("DOMContentLoaded", function (e) {


    // eventListener for Map Links
    const map_links = document.querySelectorAll(".link-to-map");

    for (let i = 0; i < map_links.length; i++) {
        map_links[i].addEventListener("click", goToMap);
    }

    // eventListener for home link
    document.querySelector(".link-home").addEventListener("click", function (e) {
        window.location.href = "/";
    });

    // eventLister for cancel reservation
    const cancelReservationButton = document.querySelector(".button-cancel-reservation");

    if (cancelReservationButton) {
        cancelReservationButton.addEventListener("click", function (e) {
            console.log("event listener id", e.target.dataset.id);
            cancelReservation(e.target.dataset.id);
        });
    }
    
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

function cancelReservation(reservationId) {
    try {
        if (!reservationId) throw "No reservation ID";

        let fetchStatus = null;
        fetch("/cancel-reservation", {
            method: "POST",
            headers: {'X-CSRFToken': my_token},
            mode: 'same-origin',
            body: JSON.stringify({
                reservation_id: parseInt(reservationId)
            })
        }).then(response => {
            fetchStatus = response.status;
            return response.json();
        }).then(result => {
            if (fetchStatus != 201) {
                throw result.message
            }
            else {
                // reservation cancelation succeeded
                console.log("canceled reservation");
                console.log("result: ", result.data);
                window.location.href = "/";
            }
        }).catch(err => {
            console.log(err);
            gMessage("alert", `Error: ${err}`);
        });
        
    } catch (err) {
        console.log("Program error. ", err);
        gMessage("alert", `Error. ${err}`)
    }
}