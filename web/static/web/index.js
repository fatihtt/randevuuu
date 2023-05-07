let my_token;
document.addEventListener("DOMContentLoaded", function () {
    // eventListener for explore
    document.querySelector("#div-search-text").addEventListener("keyup", search_change);

    // eventListener for reservations
    const reservationElements = document.querySelectorAll(".div-reservation");
    for (let i = 0; i < reservationElements.length; i++) {
        element = reservationElements[i];
        reservation_id = element.dataset.id;
        element.addEventListener("click", function (e) {
            window.location.href = `./reservation/${reservation_id}`;
        });
    }

    // eventListener for providers
    const providerElements = document.querySelectorAll(".provider");
    for (let k = 0; k < providerElements.length; k++) {
        const providerId = providerElements[k].dataset.id;
        providerElements[k].addEventListener("click", function() {
            window.location.href = `/provider/${providerId}`;
        });
    }

    my_token = getCookie('csrftoken')
});
function search_change (e) {
    m_text = e.target.value;
    const resultDiv = document.querySelector(".div-explore-result-main");
    if (m_text.length > 2) {
        fetch("explore-search", {
            method: "POST",
            headers: {'X-CSRFToken': my_token},
            mode: 'same-origin',
            body: JSON.stringify({
                text: m_text
            })
        }).then(response => {
            return response.json();
        }).then(result => {
            // API newpost result
            result = result.data;
            resultHtml = ``;
            for (let i = 0; i < result.length; i++) {
                let m_inner = ``;
                // Logo or provider name
                if (result[i].logo_url.length < 1) {
                    m_inner = `
                        <div class="div-provider-no-image">
                            <span>${ result[i].name }</span>
                        </div>
                    `;
                }
                else {
                    m_inner = `
                        <img src="/static/${result[i].logo_url}" alt="${result[i].name}" class="img-logo">
                    `;
                }
                // Service List
                let availableServicesHtml = "";
                for (let k = 0; k < result[i].available_services.length; k++) {
                    service = result[i].available_services[k].name;
                    availableServicesHtml += `
                        <div class="result-service">${service}</div>
                    `;
                }
                // Prepare html code
                resultHtml += `
                    <a class="a-search-result no-a" href="/provider/${result[i].id}">
                        <div class="div-result-element pointer">
                            ${m_inner}
                            <div class="div-result-element-location">
                                <span>${ result[i].district }, ${ result[i].city }</span>
                            </div>
                            <div class="div-result-element-services">
                                ${ availableServicesHtml }
                            </div>
                        </div>
                    </a>
                `;
            }

            // Add html to div
            resultDiv.innerHTML = resultHtml;

            // If search result empty, hide resultDiv
            if (result.length < 1 && !resultDiv.classList.contains("hidden")) resultDiv.classList.add("hidden");
            else resultDiv.classList.remove("hidden");
        }).catch(err => {
            console.log("Error: ", err);
        })
        console.log(e.target.value);
    }
    else {
        resultDiv.innerHTML = "";
        if (!resultDiv.classList.contains("hidden")) resultDiv.classList.add("hidden");
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