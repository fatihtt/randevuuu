let allowable_dates = ["2023-05-13", "2023-05-14", "2023-05-15"];
writeAllowableDates();
// console.log(new Date().toISOString().substring(0, 10));

let cur_date_index = 0;
let providerId;
let selectedTime;

document.addEventListener("DOMContentLoaded", function () {

    console.log("provider col: ",  document.querySelector(".provider-col").dataset);
    providerId = document.querySelector(".provider-col").dataset.id;
    console.log("providerId: ", providerId);

    // eventListeners active service selection event
    document.querySelector("#select-active-services").addEventListener("change", function (e) {
        console.log("selected: ", e.target.value);
        if (parseInt(e.target.value) === -1) {
            document.querySelector(".button-out-1").disabled = true;
            document.querySelector(".time-selection-main").innerHTML = "Please select service and adjust date";
            selectedTime = null;
        }
        else takeAvailableTimes();
    });

    // eventListeners for date buttons 
    document.querySelector(".date-selection-previous").addEventListener("click", function() {
        cur_date_index--;
        writeDate(allowable_dates[cur_date_index]);
    });
    document.querySelector(".date-selection-next").addEventListener("click", function() {
        cur_date_index++;
        writeDate(allowable_dates[cur_date_index]);
    });

    writeDate(allowable_dates[cur_date_index]);

});

Date.prototype.addDays = function(days) {
    this.setDate(this.getDate() + parseInt(days));
    return this;
};

function writeAllowableDates () {
    m_now = new Date();
    if (m_now.getHours() < 12) z = 0;
    else z = 1;
    allowable_dates = [];
    //burdan
    for (let k = z; k < 3 + z; k++) {
        allowable_dates.push((new Date(m_now + k * 24 * 60 * 60 * 1000)));
    }
    console.log("allowable dates: ", allowable_dates);
}
function writeDate (date) {

    // Adjust previous and next button visibilities

    if ( cur_date_index > 0) document.querySelector(".date-selection-previous").classList.remove("vis-hidden");
    else document.querySelector(".date-selection-previous").classList.add("vis-hidden");

    if (cur_date_index + 1 < allowable_dates.length) document.querySelector(".date-selection-next").classList.remove("vis-hidden");
    else document.querySelector(".date-selection-next").classList.add("vis-hidden");

    // Write date
    const options = { weekday: 'long', month: 'long', day: 'numeric' };
    document.querySelector(".date-selection-date").innerHTML= (new Date(date)).toLocaleDateString("en-EN", options);

    takeAvailableTimes();
}

function takeAvailableTimes() {
    try {
        gMessage("information", "loading");
        if (!providerId) throw "No provider given.";

        const aServiceId = parseInt(document.querySelector("#select-active-services").value);

        if (aServiceId > 0) {

            console.log("sending date: ", allowable_dates[cur_date_index]);
            let fetchStatus = null;
            fetch("/get-available-times", {
                method: "POST",
                headers: {'X-CSRFToken': my_token},
                mode: 'same-origin',
                body: JSON.stringify({
                    provider_id: parseInt(providerId),
                    date: allowable_dates[cur_date_index],
                    a_service_id: aServiceId
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
                    gMessageCloseFunc();
                    showAvailableDateTime(result.available_hours);
                }
            }).catch(err => {
                console.log(err);
                gMessage("alert", `Error: ${err}`);
            });
        }
        else {
            gMessageCloseFunc();
        }
        
    } catch (err) {
        console.log("Program error. ", err);
        gMessage("alert", `Error. ${err}`)
    }
}

function showAvailableDateTime (timeArray) {
    try {
        // get duration minutes of selected service
        const serviceSelect = document.querySelector("#select-active-services");
        duration_min = serviceSelect.options[serviceSelect.selectedIndex].dataset.duration;

        // adjust html of token times
        let timesHtml = `<div class="div-time-select-main">`;
        if (timeArray.length === 0) timesHtml += "<span style='color: red'>No available time on selected date.</span>";

        for (time of timeArray) {
            times = time;
            if (time.toString().length === 1) times = "0" + time;
            timesHtml += `
                <div data-time="${times}:00" class="div-time-select-out pointer">
                    <div class="div-time-select-in">
                        ${times}:00
                    </div>
                </div>
                `;
            if (duration_min <= 30) {
                timesHtml += `
                <div data-time="${times}:30" class="div-time-select-out pointer">
                    <div class="div-time-select-in">
                        ${times}:30
                    </div>
                </div>
                `;
            }
        }
        timesHtml += "</div>"

        // write adjusted html to proper div
        document.querySelector(".time-selection-main").innerHTML = timesHtml;

        // add eventListeners for new embedded time selection elements
        addEventListenersToTimeSelectors();
    } catch (err) {
        console.log("Program Error. ", err);
        gMessage("alert", `Error. ${err}`);
    }
}
function addEventListenersToTimeSelectors () {
    // take time selection elements
    const timeElements = document.querySelectorAll(".div-time-select-out");

    // for each element define eventListener
    for (const timeElement of timeElements) {
        timeElement.addEventListener("click", function (e) {
            // collect all time selection elements and remove selection
            const m_timeElements = document.querySelectorAll(".div-time-select-out");
            for (const m_timeElement of m_timeElements) {
                m_timeElement.classList.remove("selected");
            }

            // make clicked element selected
            e.target.parentElement.classList.add("selected");

            // adjust global selectedTime variable
            selectedTime = e.target.innerText;

            // enable save button
            document.querySelector(".button-out-1").disabled = false;
            console.log("selectedTime: ", selectedTime);
        });
    }
}