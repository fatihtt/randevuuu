let my_token;
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#div-search-text").addEventListener("keyup", search_change);

    my_token = getCookie('csrftoken')
});
function search_change (e) {
    m_text = e.target.value;
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
                        <div class="div-result-element-no-image">
                            <span>${ result[i].name }</span>
                        </div>
                    `;
                }
                else {
                    m_inner = `
                        <img src="/static/${result[i].logo_url}" alt="${result[i].name}" class="img-result-logo">
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
                    <div class="div-result-element pointer">
                        ${m_inner}
                        <div class="div-result-element-location">
                            <span>${ result[i].district }, ${ result[i].city }</span>
                        </div>
                        <div class="div-result-element-services">
                            ${ availableServicesHtml }
                        </div>
                    </div>
                `;
            }
            // Add html to div
            document.querySelector(".div-explore-result-main").innerHTML = resultHtml;
        }).catch(err => {
            console.log("Error: ", err);
        })
        console.log(e.target.value);
    }
    else {
        document.querySelector(".div-explore-result-main").innerHTML = "";
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