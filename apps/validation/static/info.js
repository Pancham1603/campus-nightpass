function resetProfile() {
    document.querySelector('.profile-card').innerHTML=`
    <img class="tempimg"src="https://static.vecteezy.com/system/resources/previews/005/129/844/non_2x/profile-user-icon-isolated-on-white-background-eps10-free-vector.jpg" alt="Profile Picture" class="profile-picture">
    </div>`;
    resetPass();
}
function resetPass() {
    const passDetails = document.querySelector('.pass-details');
    const passIdElement = passDetails.querySelector('p:nth-child(2)');
    const accessElement = passDetails.querySelector('p:nth-child(3)');
    const checkinElement = passDetails.querySelector('p:nth-child(4)');
    const entryTimeElement = passDetails.querySelector('p:nth-child(5)');
    const checkoutElement = passDetails.querySelector('p:nth-child(6)');
    const exitTimeElement = passDetails.querySelector('p:nth-child(7)');
    const actionButton = document.getElementById('action-button')
    document.getElementById('pass-card').style.backgroundColor = '#FFFFFF'
    passIdElement.textContent = `Pass ID: `;
    accessElement.textContent = `Access: `;
    checkinElement.textContent = `Check-in: `;
    entryTimeElement.textContent = `Entry Time: `;
    checkoutElement.textContent = `Check-out: `;
    exitTimeElement.textContent = `Exit Time: `;

            actionButton.style.visibility = 'hidden';
            actionButton.innerHTML = ``;
            actionButton.style.setProperty('priority', 'important');
            actionButton.onclick = function()  {}

    }

function updateProfile(data) {
    document.querySelector('.profile-card').innerHTML=`
    <img class="image" id="user_picture" src="" alt="Student Picture">
    <div class="profile-details">
        <h2></h2>
        <p><strong>Registration Number:</strong> </p>
        <p><strong>Hostel:</strong></p>
        <p><strong>Room Number:</strong> </p>
        <p><strong>In Hostel:</strong> </p>
        <p><strong>Hostel Check-in Time:</strong> </p>
        <p><strong>Hostel Check-out Time:</strong> </p>
        <p><strong>Last Check-out Time:</strong> </p>
        <p><strong>Has Booked:</strong> </p>
    </div>`;
    const profileDetails = document.querySelector('.profile-details');
    const nameElement = profileDetails.querySelector('h2');
    const regNumberElement = profileDetails.querySelector('p:nth-child(2)');
    const hostelElement = profileDetails.querySelector('p:nth-child(3)');
    const roomNumberElement = profileDetails.querySelector('p:nth-child(4)');
    const inHostelElement = profileDetails.querySelector('p:nth-child(5)');
    const hostelCheckinElement = profileDetails.querySelector('p:nth-child(6)');
    const hostelCheckoutElement = profileDetails.querySelector('p:nth-child(7)');
    const lastCheckoutElement = profileDetails.querySelector('p:nth-child(8)');
    const hasBookedElement = profileDetails.querySelector('p:nth-child(9)');
    const options = { hour: '2-digit', minute: '2-digit', hour12: true, month: 'long', day: '2-digit' };
    const checkinTime = new Date(data.hostel_checkin_time).toLocaleString('en-US', options);
    const checkoutTime = new Date(data.hostel_checkout_time).toLocaleString('en-US', options);
    const lastCheckoutTime = new Date(data.last_checkout_time).toLocaleString('en-US', options);
    document.getElementById('user_picture').src = data.picture;
    nameElement.textContent = data.name;
    regNumberElement.textContent = `Registration Number: ${data.registration_number}`;
    hostelElement.textContent = `Hostel: ${data.hostel}`;
    roomNumberElement.textContent = `Room Number: ${data.room_number}`;
    inHostelElement.textContent = `In Hostel: ${data.is_checked_in ? 'Yes' : 'No'}`;
    hostelCheckinElement.textContent = `Hostel Check-in Time: ${checkinTime}`;
    hostelCheckoutElement.textContent = `Hostel Check-out Time: ${checkoutTime}`;
    lastCheckoutElement.textContent = `Last Check-out Time: ${lastCheckoutTime}`;
    hasBookedElement.textContent = `Has Booked: ${data.has_booked ? 'Yes' : 'No'}`;
    setTimeout(function(){resetProfile();}, 10000);
}

// Function to update the user pass section with data
function updateUserPass(data,user_data, task, request_user_location) {
    const passDetails = document.querySelector('.pass-details');
    const passIdElement = passDetails.querySelector('p:nth-child(2)');
    const accessElement = passDetails.querySelector('p:nth-child(3)');
    const checkinElement = passDetails.querySelector('p:nth-child(4)');
    const entryTimeElement = passDetails.querySelector('p:nth-child(5)');
    const checkoutElement = passDetails.querySelector('p:nth-child(6)');
    const exitTimeElement = passDetails.querySelector('p:nth-child(7)');
    const actionButton = document.getElementById('action-button')

    passIdElement.textContent = `Pass ID: ${data.pass_id}`;
    accessElement.textContent = `Access: ${data.campus_resource}`;
    checkinElement.textContent = `Check-in: ${data.check_in}`;
    entryTimeElement.textContent = `Entry Time: ${data.check_in_time}`;
    checkoutElement.textContent = `Check-out: ${data.check_out}`;
    exitTimeElement.textContent = `Exit Time: ${data.check_out_time}`;
    
    if (task['check_out']) {
        if (request_user_location == 'campus_resource') {
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check Out`;
            // checkOut(user_data.registration_number);
            document.getElementById('pass-card').style.backgroundColor = '#F0E68C';
            actionButton.onclick = function()  {checkOut(user_data.registration_number);}
        } else {
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check Out`;
            document.getElementById('pass-card').style.backgroundColor = '#90EE90'
            actionButton.onclick = function()  {checkOut(user_data.registration_number);}}
    } else if (task['check_in']) {
        if (request_user_location == 'campus_resource') {
            // checkIn(user_data.registration_number);
            document.getElementById('pass-card').style.backgroundColor = '#90EE90';
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check In`;
            actionButton.onclick = function(){checkIn(user_data.registration_number);}
        } else {
            document.getElementById('pass-card').style.backgroundColor = '#F0E68C';
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check In`;
            actionButton.onclick = function(){checkIn(user_data.registration_number);}}
    } else {
        document.getElementById('pass-card').style.backgroundColor = '#FF7F7F';
    }
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
            console.log(response.request_user_location)
            updateProfile(response.user);
            updateUserPass(response.user_pass, response.user, response.task, response.request_user_location);
            if (response.user_pass.pass_id) {
            } else [
            document.getElementById('pass-card').style.backgroundColor = '#FF7F7F'
            ]
            toastr.success(response.message);
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
        document.getElementById('roll_no').focus();
        let res = response.status;
        if (res) {
           // resetProfile();
            // updateProfile(response.user);
            // updateUserPass(response.user_pass, response.user);
            toastr.success(response.message);
            setTimeout(function(){ resetProfile(); }, 7000);

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
        document.getElementById('roll_no').focus();
        let res = response.status;
        if (res) {
            
            // updateProfile(response.user);
            // updateUserPass(response.user_pass, response.user);
            toastr.success(response.message);
            setTimeout(function(){ resetProfile(); }, 7000);
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
}, 1000);