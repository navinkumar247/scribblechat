
$(".messages").animate({ scrollTop: $(document).height() }, "fast");

$("#profile-img").click(statusMenu);

function statusMenu() {
    $("#status-options").toggleClass("active");
    $("#profile").removeClass("expanded");
    $("#contacts").removeClass("expanded");
}

$(".expand-button").click(function() {
    $("#profile").toggleClass("expanded");
    $("#contacts").toggleClass("expanded");
    $("#status-options").removeClass("active");
    
});

$("#status-options ul li").click(function() {
    $("#profile-img").removeClass();
    $("#status-online").removeClass("active");
    $("#status-away").removeClass("active");
    $("#status-busy").removeClass("active");
    $("#status-offline").removeClass("active");
    $(this).addClass("active");
    
    if($("#status-online").hasClass("active")) {
        $("#profile-img").addClass("online");
    } else if ($("#status-away").hasClass("active")) {
        $("#profile-img").addClass("away");
    } else if ($("#status-busy").hasClass("active")) {
        $("#profile-img").addClass("busy");
    } else if ($("#status-offline").hasClass("active")) {
        $("#profile-img").addClass("offline");
    } else {
        $("#profile-img").removeClass();
    };
    
    $("#status-options").removeClass("active");
});

const addContact = $('#addcontact');
const addContactsContainer = $('.addcontacts');
addContact.click(function (){
    addContactsContainer.toggleClass('addcontacts-active');
    pendingRequestsContainer.removeClass('addcontacts-active');
})

const pendingRequests = $('#pending-requests');
const pendingRequestsContainer = $('.pendingrequests');
pendingRequests.click(function (){
    pendingRequestsContainer.toggleClass('addcontacts-active');
    addContactsContainer.removeClass('addcontacts-active');
})


var inputMsg = document.querySelector('#chat-message-input');
inputMsg.onkeyup = function(e) {
    e.preventDefault();
    console.log('works');
    if (e.keyCode === 13 && inputMsg.value != '') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};
// const addContactForm = $('#addcontact-form');

// addContactForm.submit(function (e) {
//     e.preventDefault();
//     const url = window.location.pathname;
//     console.log(url);
//     $.ajax({
//         type: "GET",
//         url: '',
//         data: {
//             "username_contains":$('#username_contains').val(),
//             'search_new_contacts':'submit',

//         },
//         success: function(response){
//             let data = JSON.parse(response.contacts);
//             for (const iterator of data) {
//                 console.log(iterator.fields.image);
//             }
//         }
//     })
// })