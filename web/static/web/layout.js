let gMessageElement;
let my_token;

// Global message function
function gMessage(type, message, returnOnClose) {
    // Define a new div element
    gMessageElement = document.createElement("div");
    gMessageElement.classList.add("g-message");

    // Add extra style to element for message type
    switch (type) {
        case "info":
            gMessageElement.classList.add("message-info");
            break;
        case "warning":
            gMessageElement.classList.add("message-warning");
            break;
        case "alert":
            gMessageElement.classList.add("message-alert");
            break;
        default:
            gMessageElement.classList.add("message-info");
            break;
    }

    // Add message closing function and its eventListener
    const gMessageClose = document.createElement("div");
    gMessageClose.classList.add("g-message-close");
    gMessageClose.innerHTML = `
        <span class="material-icons pointer">
        close
        </span>
    `;

    // If message says go when message close, add a hint for CloseFunc
    if (returnOnClose) {
        gMessageElement.dataset.go = returnOnClose;
    }

    gMessageClose.addEventListener("click", gMessageCloseFunc);
    gMessageElement.appendChild(gMessageClose);

    // Define and append message text element
    const gMessageIn = document.createElement("div");
    gMessageIn.classList.add("g-message-in");
    gMessageIn.innerHTML = `
        <div class="div-message-logo">randevuuu</div>
        <div class="div-message">${message}</div>
    `;
    gMessageElement.appendChild(gMessageIn);

    // Append message element to body
    document.body.appendChild(gMessageElement);
}

// Global message close function
function gMessageCloseFunc (e) {
    const gMessageElements = document.querySelectorAll(".g-message");

    for (let i = 0; i < gMessageElements.length; i++) {
        if (gMessageElements[i].dataset.go) window.location.href = gMessageElements[i].dataset.go;
        else gMessageElements[i].remove();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    my_token = getCookie('csrftoken');
});

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