

function is_mobile() {
    if (navigator.userAgentData.mobile) {
        toastr.options = {
            "closeButton": false,
            "newestOnTop": true,
            "progressBar": false,
            "positionClass": "toast-top-right",
            "preventDuplicates": true,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "3000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        }
        return true;
    } else {
        toastr.options = {
            "closeButton": false,
            "newestOnTop": true,
            "progressBar": false,
            "positionClass": "toast-bottom-full-width",
            "preventDuplicates": true,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "3000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        }
        return false;
    }
}

function resetProfile() {
    document.querySelector('.profile-card').innerHTML=`
    <img class="tempimg"src="https://static.vecteezy.com/system/resources/previews/005/129/844/non_2x/profile-user-icon-isolated-on-white-background-eps10-free-vector.jpg" alt="Profile Picture" style="opacity:0.5;" class="profile-picture"><br>
    <button id="action-button" style="visibility: hidden;" class="action-button"></button>
    </div>`;
    resetPass();
}
function resetPass() {
    try {
        const passDetails = document.querySelector('.pass-details');
        const passIdElement = passDetails.querySelector('p:nth-child(2)');
        const accessElement = passDetails.querySelector('p:nth-child(3)');
        const checkinElement = passDetails.querySelector('p:nth-child(4)');
        const entryTimeElement = passDetails.querySelector('p:nth-child(5)');
        const checkoutElement = passDetails.querySelector('p:nth-child(6)');
        const exitTimeElement = passDetails.querySelector('p:nth-child(7)');
        passIdElement.textContent = `Pass ID: `;
        accessElement.textContent = `Access: `;
        checkinElement.textContent = `Check-in: `;
        entryTimeElement.textContent = `Entry Time: `;
        checkoutElement.textContent = `Check-out: `;
        exitTimeElement.textContent = `Exit Time: `;
    } catch (error) {
        
    }
    document.getElementById('profile-card').style.backgroundColor = '#FFFFFF'
    try {
        const actionButton = document.getElementById('action-button')
        actionButton.style.visibility = 'hidden';
        actionButton.innerHTML = ``;
        actionButton.style.setProperty('priority', 'important');
        actionButton.onclick = function()  {}
    } catch (error) {
    }     
    }

var timeouts = [];
function updateProfile(data) {
    // document.querySelector('.profile-card').innerHTML=`
    // <img class="image" id="user_picture" src="" alt="Student Picture">
    // <div class="profile-details">
    //     <h2></h2>
    //     <p><strong>Registration Number:</strong> </p>
    //     <p><strong>Hostel:</strong></p>
    //     <p><strong>Room Number:</strong> </p>
    //     <p><strong>In Hostel:</strong> </p>
    //     <p><strong>Hostel Check-in Time:</strong> </p>
    //     <p><strong>Hostel Check-out Time:</strong> </p>
    //     <p><strong>Last Check-out Time:</strong> </p>
    //     <p><strong>Has Booked:</strong> </p>
    // </div>`;

    document.querySelector('.profile-card').innerHTML=`
    <h2></h2>
    <p><strong>Roll Number:</strong> </p>
    <img class="tempimg" id="user_picture" src="" alt="Student Picture"><br>
    <button id="action-button" style="visibility: hidden;" class="action-button"></button>
    </div>
`;


    const profileDetails = document.querySelector('.profile-card');
    const nameElement = profileDetails.querySelector('h2');
    const regNumberElement = profileDetails.querySelector('p');


    // const profileDetails = document.querySelector('.profile-details');
    // const nameElement = profileDetails.querySelector('h2');
    // const regNumberElement = profileDetails.querySelector('p:nth-child(2)');
    // const hostelElement = profileDetails.querySelector('p:nth-child(3)');
    // const roomNumberElement = profileDetails.querySelector('p:nth-child(4)');
    // const inHostelElement = profileDetails.querySelector('p:nth-child(5)');
    // const hostelCheckinElement = profileDetails.querySelector('p:nth-child(6)');
    // const hostelCheckoutElement = profileDetails.querySelector('p:nth-child(7)');
    // const lastCheckoutElement = profileDetails.querySelector('p:nth-child(8)');
    // const hasBookedElement = profileDetails.querySelector('p:nth-child(9)');
    // const options = { hour: '2-digit', minute: '2-digit', hour12: true, month: 'long', day: '2-digit' };
    // const checkinTime = new Date(data.hostel_checkin_time).toLocaleString('en-US', options);
    // const checkoutTime = new Date(data.hostel_checkout_time).toLocaleString('en-US', options);
    // const lastCheckoutTime = new Date(data.last_checkout_time).toLocaleString('en-US', options);
    document.getElementById('user_picture').src = data.picture;
    nameElement.textContent = data.name;
    regNumberElement.textContent = `Registration Number: ${data.registration_number}`;
    // hostelElement.textContent = `Hostel: ${data.hostel}`;
    // roomNumberElement.textContent = `Room Number: ${data.room_number}`;
    // inHostelElement.textContent = `In Hostel: ${data.is_checked_in ? 'Yes' : 'No'}`;
    // hostelCheckinElement.textContent = `Hostel Check-in Time: ${checkinTime}`;
    // hostelCheckoutElement.textContent = `Hostel Check-out Time: ${checkoutTime}`;
    // lastCheckoutElement.textContent = `Last Check-out Time: ${lastCheckoutTime}`;
    // hasBookedElement.textContent = `Has Booked: ${data.has_booked ? 'Yes' : 'No'}`;
    for (var i = 0; i < timeouts.length; i++) {
        clearTimeout(timeouts[i]);
    }
    timeouts.push(setTimeout(function(){resetProfile();}, 7000));
}

// Function to update the user pass section with data
function updateUserPass(data,user_data, task, request_user_location, message) {
    const actionButton = document.getElementById('action-button')
    try{
    const passDetails = document.querySelector('.pass-details');
    const passIdElement = passDetails.querySelector('p:nth-child(2)');
    const accessElement = passDetails.querySelector('p:nth-child(3)');
    const checkinElement = passDetails.querySelector('p:nth-child(4)');
    const entryTimeElement = passDetails.querySelector('p:nth-child(5)');
    const checkoutElement = passDetails.querySelector('p:nth-child(6)');
    const exitTimeElement = passDetails.querySelector('p:nth-child(7)');
    passIdElement.textContent = `Pass ID: ${data.pass_id}`;
    accessElement.textContent = `Access: ${data.campus_resource}`;
    checkinElement.textContent = `Check-in: ${data.check_in}`;
    entryTimeElement.textContent = `Entry Time: ${data.check_in_time}`;
    checkoutElement.textContent = `Check-out: ${data.check_out}`;
    exitTimeElement.textContent = `Exit Time: ${data.check_out_time}`;
    } catch (error) {}

    if (!data.pass_id) {
        document.getElementById('profile-card').style.backgroundColor = '#FF7F7F';
        toastr.error(message);
    } else {

    if (task['check_out']) {
        if (request_user_location == 'campus_resource') {
            if (is_mobile()){
                actionButton.style.visibility = 'visible';
                actionButton.innerHTML = `Check Out`;
                document.getElementById('profile-card').style.backgroundColor = '#F0E68C';
                actionButton.onclick = function()  {checkOut(user_data.registration_number);}
            } else {
                checkOut(user_data.registration_number);
                // document.getElementById('profile-card').style.backgroundColor = '#F0E68C';
            }            
        } else {
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check Out`;
            document.getElementById('profile-card').style.backgroundColor = '#90EE90'
            actionButton.onclick = function()  {checkOut(user_data.registration_number);}}
    } else if (task['check_in']) {
        if (request_user_location == 'campus_resource') {
            if (is_mobile()){
                actionButton.style.visibility = 'visible';
                actionButton.innerHTML = `Check In`;
                document.getElementById('profile-card').style.backgroundColor = '#90EE90';
                actionButton.onclick = function()  {checkIn(user_data.registration_number);}
            } else {
                checkIn(user_data.registration_number);
                document.getElementById('profile-card').style.backgroundColor = '#90EE90';    
            }
        } else {
            document.getElementById('profile-card').style.backgroundColor = '#F0E68C';
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check In`;
            actionButton.onclick = function(){checkIn(user_data.registration_number);}}
    } else {
        document.getElementById('profile-card').style.backgroundColor = '#FF7F7F';
    }
}}

function updateStats(data) {
    document.getElementById('total_count').innerHTML = 'Booking: ' + data.total_count;
    document.getElementById('check_in_count').innerHTML = 'Checked In: ' + data.check_in_count;
}

function fetch_data(dump) {
    urls = ""
    $.ajax({
    method: "POST",
    url: urls,
    data:dump,
    dataType: "json",
    timeout: 12000,
    success: function (response) {
        let res = response.status;
        if (res) {
            updateProfile(response.user);
            updateUserPass(response.user_pass, response.user, response.task, response.request_user_location, response.message);
        }
        else {
            toastr.error(response.message);
        }
    },
    error: function (xhr, textStatus, errorThrown) {
        toastr.error("Something went wrong, please try again later");
    }
});
}


function checkIn(registration_number) {
    urls = "checkin/"
    $.ajax({
    method: "POST",
    url: urls,
    data:{'registration_number':registration_number},
    dataType: "json",
    timeout: 120000,
    success: function (response) {
        if (!is_mobile()) {document.getElementById('roll_num').focus();}
        let res = response.status;
        if (res) {
            if (response.student_stats) {updateStats(response.student_stats);}
            toastr.success(response.message);
            for (var i = 0; i < timeouts.length; i++) {
                clearTimeout(timeouts[i]);
            }
            timeouts.push(setTimeout(function(){ resetProfile(); }, 5000));

        }
        else {
            toastr.error(response.message);
        }
    },
    error: function (xhr, textStatus, errorThrown) {
        toastr.error("Something went wrong, please try again later");
    }
});
}

function checkOut(registration_number) {
    urls = "checkout/"
    $.ajax({
    method: "POST",
    url: urls,
    data:{'registration_number':registration_number},
    dataType: "json",
    timeout: 120000,
    success: function (response) {
        if (!is_mobile()) {document.getElementById('roll_num').focus();}
        let res = response.status;
        if (res) {
            if (response.student_stats) {updateStats(response.student_stats);}
            document.getElementById('profile-card').style.backgroundColor = '#F0E68C';
            toastr.success(response.message);
            for (var i = 0; i < timeouts.length; i++) {
                clearTimeout(timeouts[i]);
            }
            timeouts.push(setTimeout(function(){ resetProfile(); }, 7000));
        }
        else {
            if (response.repeated) {updateStats(response.student_stats); document.getElementById('profile-card').style.backgroundColor = '#90EE90';}
            toastr.error(response.message);
        }
    },
    error: function (xhr, textStatus, errorThrown) {
        toastr.error("Something went wrong, please try again later");
    }
});
}


let enteredIntegers = 0;
function checkInput() {
    const inputElement = document.getElementById('roll_num');

    if (inputElement.value.length >= 0 && inputElement.value.length == 9) {
        enteredIntegers = inputElement.value.length;
        if (enteredIntegers === 9) {
            fetch_data({'registration_number':inputElement.value})
            var audio = new Audio('../static/beep.mp3');
            audio.play();
            inputElement.value = '';
            enteredIntegers = 0;
        } 
    } 
}

setInterval(function () {
    checkInput()
}, 300);